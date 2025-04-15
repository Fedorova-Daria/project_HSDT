<template>
  <div
    class="idea-card border border-zinc-700 bg-card rounded-xl p-5 shadow-lg cursor-pointer"
    @click="openIdea(idea)"
  >
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.name }}</h1>
      <div class="flex items-center">
        <img
  :src="liked ? '/liked.svg' : '/like.svg'"
  alt="Like"
  class="w-6 h-6 mr-2 duration-300 cursor-pointer"
  :class="{ 'animate-like': isAnimating }"
  @click.stop="updateLike"
/>
        <span class="text-white">{{ idea.likes_count }}</span> 
      </div>
    </div>

    <p class="text-gray-300 mb-3 truncate-text">
  {{ idea.description || "Описание отсутствует" }}
</p>
<p class="text-gray-300 truncate-text">
  {{ idea.status }}
</p>
    <div class="mt-auto">
      <h3 class="text-xl text-white mb-3">
        Инициатор: {{ idea.initiator || "Неизвестный автор" }}
      </h3>
    </div>

    <div v-if="userRole === 'EX' && 'CU'" class="text-white mt-2">
      Голосов экспертов: {{ idea.experts_voted_count }}
    </div>
  </div>
</template>

<script>
import { fetchOwnerName, toggleLike } from "@/api/ideaHelpers.js";
import Cookies from "js-cookie";
import { getUserRoleFromCookies } from "@/api/storage.js";
export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isAnimating: false, // Для анимации лайка
      userRole: null, // Здесь инициализируем userRole
    };
  },
  created() {
    this.userRole = getUserRoleFromCookies(); // Устанавливаем значение из Cookies
  },
  computed: {
    liked() {
    if (!this.idea || !this.idea.likes) return false;
    const userData = JSON.parse(Cookies.get("userData") || "{}");
    return this.idea.likes.includes(userData.id);
    },
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    expertsVotesCount() {
      // Реактивно вычисляем количество голосов экспертов
      return this.idea.experts_voted_count || 0;
    },
  },
  mounted() {
    this.loadOwnerName(); // Загружаем инициатора на этапе монтирования
  },
  methods: {
    openIdea(idea) {
  const institute = this.selectedInstitute; // Используем selectedInstitute из data()
  if (institute) {
    this.$router.push({ path: `/${institute}/ideas/${idea.id}` });
  } else {
    console.error("Институт не выбран");
  }
  },
    async loadOwnerName() {
      try {
        // Передаем текущую идею и ID владельца в функцию из утилит
        await fetchOwnerName(this.idea, this.idea.owner);
      } catch (error) {
        console.error("Ошибка при загрузке имени владельца:", error);
      }
    },
    async updateLike(event) {
  try {
    await toggleLike(
      this.idea,
      event,
      this.liked,
      (state) => (this.isAnimating = state),
      () => JSON.parse(Cookies.get("userData") || "{}")?.id
    );

    // Прямое обновление свойства
    if (this.userRole === "EX") {
      this.idea.experts_voted_count = this.idea.experts_voted_count || 0; // Обновляем количество голосов
    }
  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);
  }
}
  },
};
</script>

<style scoped>
.truncate-text {
  display: -webkit-box; /* Используем flex-контейнер */
  -webkit-line-clamp: 2; /* Ограничиваем текст двумя строками */
  -webkit-box-orient: vertical; /* Задаём направление контейнера */
  overflow: hidden; /* Скрываем выходящий текст */
  text-overflow: ellipsis; /* Добавляем "..." для обрезанного текста */
  word-wrap: break-word; /* Перенос слов при необходимости */
}
/* Анимация лайка */
@keyframes likeJump {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.4);
  }
  100% {
    transform: scale(1);
  }
}

.animate-like {
  animation: likeJump 0.3s ease-in-out;
}
</style>
