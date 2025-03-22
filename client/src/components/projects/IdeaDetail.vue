<template>
  <div>
    <Header />
    <div class="flex w-4/5 mx-auto mt-10 gap-4 text-white">
      <!-- Левый блок (Название и кнопки для функций идей) -->
      <div class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <strong class="mt-5 text-3xl">{{ idea?.name }}</strong>
        <!-- Отображение имени идеи -->
        <div class="mt-3 h-0.5 w-full m-auto bg-white"></div>
        <h1 class="text-xl mt-3">Инициатор:</h1>
        <h2 class="text-xl mt-1 font-bold">{{ idea.initiator_info.name }}</h2>
        <!-- Инициатор -->
        <div class="flex gap-3 mt-3">
          <button
            class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
          >
            <svg
              class="me-1 -ms-1 w-5 h-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>

          <img
            :src="liked ? '/liked.svg' : '/like.svg'"
            alt="Like"
            class="w-6 h-6 mr-2 mt-1 duration-300 cursor-pointer"
            :class="{ 'animate-like': isAnimating }"
            @click.stop="toggleLike"
            @animationend="isAnimating = false"
          />

          <button
            class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
          >
            Редактировать
          </button>
          <button
            class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
          >
            Удалить
          </button>
        </div>
      </div>
      <!-- Правый блок (вся информация о идее) -->
      <div class="w-3/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <strong class="mt-5 text-3xl"> Информация об идее</strong>
        <div class="mt-3 h-0.5 w-full m-auto bg-white"></div>
        <h1 class="text-xl mt-3">
          {{ idea?.description }}
          <!-- Отображение описания идеи -->
        </h1>
      </div>
    </div>
  </div>
  <!--<div class="text-white" v-else>
    <p>Загрузка...</p>
  </div>-->
</template>

<script>
import axios from "axios";
import Header from "@/components/header.vue";

export default {
  components: { Header },
  data() {
    return {
      idea: null, // Здесь будем хранить данные о выбранной идее
    };
  },
  async created() {
    // Получаем id из URL
    const ideaId = this.$route.params.id;
    await this.fetchIdeaDetail(ideaId); // Загружаем информацию о идее по id
  },
  methods: {
    async fetchIdeaDetail(id) {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/ideas/${id}/`
        );
        this.idea = response.data; // Сохраняем данные о идее в переменную idea
      } catch (error) {
        console.error("Ошибка при загрузке информации о идее:", error);
      }
    },
  },
};
</script>
