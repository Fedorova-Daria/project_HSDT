<template>
  <div
    class="idea-card bg-card rounded-2xl p-5 shadow-lg cursor-pointer h-full flex flex-col justify-between"
  >
    <!-- Верхняя часть -->
    <div>
      <div class="flex justify-between items-center mb-3">
        <h1 class="text-2xl font-semibold text-dynamic">
          {{ idea.title }}
        </h1>
      </div>
    </div>

    <!-- Нижняя часть -->
    <div class="mt-auto">
      <div class="flex flex-wrap gap-2 mt-2 mb-4">
    <!-- Выводим первые 10 технологий -->
    <span
      v-for="tech in idea.skills_required.slice(0, 10)"
      :key="tech.id"
      class="bg-gray-200 text-sl text-gray-700 px-2 py-1 rounded-full"
    >
      {{ tech.name }}
    </span>

    <!-- Если технологий больше 10, показываем +N -->
    <span
      v-if="idea.skills_required.length > 10"
      class="bg-gray-300 text-sm text-gray-700 px-2 py-1 rounded-full cursor-default"
    >
      +{{ idea.skills_required.length - 10 }}
    </span>
  </div>

      <h3 class="text-lg text-dynamic mb-1">
        Инициатор: {{ idea.initiator || "Неизвестный автор" }}
      </h3>

      <div
        v-if="userRole === 'EX' || userRole === 'CU'"
        class="text-sl text-dynamic"
      >
        Голосов экспертов: {{ idea.expert_likes.length }}
      </div>
    </div>
  </div>
</template>

<script>
import { fetchOwnerName, toggleLike } from "@/services/projects.js";
import Cookies from "js-cookie";
import UserService from "@/composables/storage.js";
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
    this.userRole = UserService.getUserRole(); // Устанавливаем значение из Cookies
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
        this.$router.push({ path: `/${institute}/project/${idea.id}` });
      } else {
        console.error("Институт не выбран");
      }
    },
    async loadOwnerName() {
      try {
        // Передаем текущую идею и ID владельца в функцию из утилит
        await fetchOwnerName(this.idea, this.idea.owner.id);
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
    },
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
