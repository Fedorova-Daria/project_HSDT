<template>
  <div>
    <Header @institute-changed="onInstituteChanged" />

    <h1 class="font-display w-4/5 m-auto mt-20 text-white text-5xl">
      Биржа проектов {{ instituteName }}
    </h1>

    <div class="flex w-4/5 m-auto mt-5">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          v-model="searchQuery"
          class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none focus:border-purple-400 duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>

      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все стеки технологий</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>

      <button
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-white"
        :style="{ backgroundColor: currentBgColor }"
  @mouseover="currentBgColor = instituteStyle.buttonOnColor"
  @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
        
      >
        Создать идею
      </button>
    </div>

    <!-- Отображение карточек идей -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-4/5 m-auto mt-10">
      <IdeaCard
        v-for="idea in filteredIdeas"
        :key="idea.id"
        :idea="idea"
        @like-toggled="updateIdeaLikes"
      />
    </div>

    <IdeaModal v-if="isModalOpen" @close="closeModal" @submit="addNewIdea" />
  </div>
</template>

<script>
import axios from "axios";
import IdeaCard from "@/components/RialtoCard1.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue";
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";

export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  components: { IdeaCard, IdeaModal, Header },
  data() {
    return {
      currentBgColor: "", // Исходный цвет
      ideas: [], // Идеи проектов
      searchQuery: "", // Поле для поиска
      isModalOpen: false, // Флаг открытия модального окна
      hover: false, // Флаг состояния кнопки
      instituteNames: {
        HSDT: "ВШЦТ",
        ARCHID: "АРХИД",
        IPTI: "ИПТИ",
        STROIN: "СТРОИН",
        TYIU: "ТИУ",
      },
    };
  },
  created() {
    // Загружаем идеи при загрузке компонента
    this.fetchCustomerIdeas();
    console.log("Текущий институт (глобальное состояние):", this.globalState.institute);
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute]; // Используем глобальное состояние
      return style || { buttonOffColor: "#ccc" }; // Дефолтный стиль
    },
    instituteName() {
      return this.instituteNames[this.selectedInstitute] || "Неизвестный институт";
    },
    filteredIdeas() {
      if (!this.searchQuery) return this.ideas;
      return this.ideas.filter((idea) =>
        idea.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    // Метод загрузки идей с сервера
    async fetchCustomerIdeas() {
      try {
        const response = await axios.get("http://localhost:8000/api/projects/");
        this.ideas = response.data;
        console.log("Идеи загружены:", this.ideas);
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    // Обновление лайков идеи
    updateIdeaLikes(updatedIdea) {
      const index = this.ideas.findIndex((idea) => idea.id === updatedIdea.id);
      if (index !== -1) {
        this.ideas[index] = { ...updatedIdea };
      }
    },
    // Открытие модального окна
    openModal() {
      this.isModalOpen = true;
    },
    // Закрытие модального окна
    closeModal() {
      this.isModalOpen = false;
    },
    // Добавление новой идеи
    addNewIdea(newIdea) {
      console.log("Новая идея:", newIdea);
      this.isModalOpen = false;
    },
    // Обработка изменения института
    onInstituteChanged(newInstitute) {
      this.globalState.institute = newInstitute; // Синхронизация с глобальным состоянием
      console.log("Институт изменён на:", newInstitute);
    },
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true, // Устанавливаем цвет сразу при загрузке
    },
    // Отслеживаем изменения глобального состояния института
    selectedInstitute(newValue) {
      console.log("Глобальное состояние института обновлено:", newValue);
    },
  },
};
</script>

<style scoped>
.hover\:bg-opacity-80:hover {
  opacity: 0.8;
}
</style>