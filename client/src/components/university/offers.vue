<template>
  <div>
    <Header @institute-changed="onInstituteChanged" />

    <div class="flex w-4/5 m-auto mt-5">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          v-model="searchQuery"
          class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none border-zinc-400 duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <button
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-white"
        :style="{ backgroundColor: currentBgColor }"
  @mouseover="currentBgColor = instituteStyle.buttonOnColor"
  @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
        
      >
        Создать предложение
      </button>
    </div>

    <!-- Отображение карточек идей -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-4/5 m-auto mt-10">
      <OfferCard
        v-for="offer in filteredoffers"
        :key="offer.id"
        :offer="offer"
        @like-toggled="updateofferLikes"
      />
    </div>

    <OfferModal v-if="isModalOpen" @close="closeModal" @submit="addNewoffer" />
  </div>
</template>

<script>
import OfferCard from "@/components/university/offerCard.vue";
import OfferModal from "@/components/university/offerModal.vue";
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import UserService from "@/composables/storage.js";
import api from "@/composables/auth";

export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  components: { OfferCard, OfferModal, Header },
  data() {
    return {
      userRole: null,
      currentBgColor: "", // Исходный цвет
      offers: [], // Идеи проектов
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
    this.userRole = UserService.getUserRole(); // Устанавливаем значение из Cookies
    // Загружаем идеи при загрузке компонента
    this.fetchCustomeroffers();
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
    filteredoffers() {
      if (!this.searchQuery) return this.offers;
      return this.offers.filter((offer) =>
        offer.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    // Метод загрузки идей с сервера
    async fetchCustomeroffers() {
      try {
        const response = await api.get("/offers/");
        this.offers = response.data;
        console.log("Идеи загружены:", this.offers);
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    // Обновление лайков идеи
    updateofferLikes(updatedoffer) {
      const index = this.offers.findIndex((offer) => offer.id === updatedoffer.id);
      if (index !== -1) {
        this.offers[index] = { ...updatedoffer };
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
    addNewoffer(newoffer) {
      console.log("Новая идея:", newoffer);
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