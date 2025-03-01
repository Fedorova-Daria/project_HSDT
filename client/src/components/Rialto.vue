<template>
  <div>
    <header
      class="flex items-center justify-between px-8 py-4 border border-border"
    >
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1 class="font-display text-fiol text-3xl">ВШЦТ</h1>
      </div>
      <!-- Навигация -->
      <nav class="flex items-center gap-10">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.link"
          class="relative text-lg font-medium transition-colors duration-300 group text-white hover:text-purple-400"
          :class="{ 'text-purple-400': $route.path === item.link }"
        >
          {{ item.name }}
          <span
            class="absolute left-1/2 bottom-[-5px] h-[3px] bg-purple-400 rounded-full transition-all duration-300 w-0 group-hover:w-full group-hover:left-0"
            :class="{ 'w-2/3 left-1/6': $route.path === item.link }"
          ></span>
        </router-link>

        <!-- Уведомления -->
        <button class="relative">
          <img src="/notificate.svg" alt="notification" class="w-6" />
        </button>

        <!-- Аватарка -->
        <div class="relative w-12 h-12">
          <img
            @click="goToProfile"
            src=""
            alt="User Avatar"
            class="w-full h-full rounded-full border-2 border-zinc-700 hover:border-purple-400 transition-all duration-300 cursor-pointer"
          />
        </div>
      </nav>
    </header>

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
        v-if="role === 'заказчик'"
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
      <IdeaCard v-for="idea in ideas" :key="idea.id" :idea="idea" />
    </div>
    <!-- Всплывающее окно -->
    <IdeaModal v-if="isModalOpen" @close="closeModal" />
    <router-view />
  </div>
</template>

<script>
import IdeaCard from "@/components/RialtoCard1.vue"; // Проверьте правильность пути
import IdeaModal from "@/components/IdeaModal.vue"; // Импортируем модальное окно
export default {
  components: { IdeaCard, IdeaModal },
  data() {
    return {
      // Примерная роль пользователя
      role: "заказчик", // Реальная роль из хранилища данных
      ideas: [
        {
          id: 1,
          title: 'Создание сайта для конкурса "Педагог года"',
          description:
            "Разработка веб-приложения для анкет преподавателей и голосования.",
          author: "Екатерина Сердюкова",
          technologies: ["C#", "Vue.js"],
          status: "Набор открыт",
        },
      ],
      menuItems: [
        { name: "Биржа", link: "/rialto" },
        { name: "Команды", link: "/teams" },
        { name: "Идеи", link: "/ideas" },
      ],
      isModalOpen: false, // Состояние модального окна
    };
  },
  methods: {
    goToProfile() {
      this.$router.push("/profile");
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
