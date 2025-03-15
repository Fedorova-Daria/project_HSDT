<template>
  <div
    class="idea-card border border-zinc-700 bg-cards rounded-xl p-5 shadow-lg cursor-pointer"
    @click="openIdea"
  >
    <!-- Заголовок и иконка лайка -->
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.title }}</h1>
      <img
        :src="liked ? '/liked1.svg' : '/like.svg'"
        alt="Like"
        class="w-6 h-6 mr-4 mb-5 duration-300 cursor-pointer"
        :class="{ 'animate-like': isAnimating }"
        @click.stop="toggleLike"
        @animationend="isAnimating = false"
      />
    </div>

    <!-- Описание -->
    <p class="text-gray-300 mb-3">{{ idea.description }}</p>

    <!-- Контент, который будет внизу карточки -->
    <div class="mt-auto">
      <!-- Инициатор -->
      <h3 class="text-xl text-white mb-3">Инициатор: {{ idea.author }}</h3>

      <!-- Стек технологий -->
      <div class="flex flex-wrap gap-1 mb-5">
        <span
          v-for="tech in idea.technologies"
          :key="tech"
          class="text-m font-medium me-2 px-2.5 py-0.5 rounded-sm border-1"
          :class="[
            stackStyles[tech]?.bg || 'bg-gray-100',
            stackStyles[tech]?.text || 'text-gray-800',
            stackStyles[tech]?.border || 'border-gray-400',
            stackStyles[tech]?.darkBg || 'dark:bg-gray-700',
            stackStyles[tech]?.darkText || 'dark:text-gray-400',
          ]"
        >
          {{ tech }}
        </span>
      </div>

      <!-- Статус идеи -->
      <div class="flex justify-between">
        <span
          class="px-4 py-2 rounded-3xl text-white text-sm border-2 bg-zinc-700"
          :class="
            idea.status === 'Набор открыт'
              ? 'border-blue-500'
              : 'border-red-500'
          "
        >
          {{ idea.status }}
        </span>
        <h3
          class="px-4 py-2 rounded-3xl text-white text-sm border-2 bg-zinc-700"
        >
          Команда из {{ idea.participantsCount }} человек
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import { stackStyles } from "@/utils/stackStyles"; // Импортируем объект
export default {
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      stackStyles, // Используем импортированный объект
      liked: false, // Состояние лайка
      isAnimating: false,
    };
  },
  methods: {
    openIdea() {
      this.$router.push(`/idea/${this.idea.id}`); // Переход на страницу идеи
    },
    toggleLike(event) {
      event.stopPropagation(); // Предотвращаем всплытие события
      this.liked = !this.liked; // Переключаем состояние лайка
      this.isAnimating = true;
    },
  },
};
</script>

<style scoped>
.idea-card {
  transition: transform 0.3s ease, border-color 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%; /* Чтобы карточка была одинаковой высоты */
}
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
