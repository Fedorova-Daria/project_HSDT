<template>
  <div>
    <Header />

    <h1 class="font-display w-4/5 m-auto mt-20 text-white text-5xl">
      Биржа проектов ВШЦТ
    </h1>

    <div class="flex w-4/5 m-auto mt-5">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
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

      <!-- Кнопка "Создать идею", отображается только если роль пользователя - "заказчик" -->
      <!-- Кнопка "Создать идею" теперь открывает модальное окно -->
      <button
        @click="openModal"
        class="bg-purple-600 text-white rounded-md px-4 py-2 hover:bg-purple-700 transition ml-5 h-10"
      >
        Создать идею
      </button>
    </div>

    <!-- Контейнер для карточек идей -->
    <div
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-4/5 m-auto mt-10"
    >
      <IdeaCard
        v-for="idea in ideas"
        :key="idea.id"
        :idea="idea"
        @click="goToIdea(idea.id)"
      />
    </div>

    <!-- Всплывающее окно -->
    <IdeaModal v-if="isModalOpen" @close="closeModal" @submit="addNewIdea" />
  </div>
</template>

<script>
import axios from "axios";
import IdeaCard from "@/components/RialtoCard1.vue"; // Проверьте правильность пути
import IdeaModal from "@/components/projects/IdeaModal.vue"; // Импортируем модальное окно
import Header from "@/components/header.vue";
export default {
  components: { IdeaCard, IdeaModal, Header },
  data() {
    return {
      ideas: [],
      isModalOpen: false, // Состояние модального окна
    };
  },
  async created() {
    await this.fetchCustomerIdeas();
  },
  methods: {
    async fetchCustomerIdeas() {
      try {
        const response = await axios.get("http://localhost:8000/api/ideas/", {
          params: { role: "CU" }, // Фильтрация по роли заказчика
        });
        this.ideas = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке идей заказчиков:", error);
      }
    },
    goToIdea(id) {
      this.$router.push(`/idea/${id}`);
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
};
</script>

<style scoped>
/* Добавьте свои стили, если необходимо */
</style>
