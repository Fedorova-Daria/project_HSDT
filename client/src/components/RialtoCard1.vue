<template>
  <div
    class="idea-card border border-zinc-700 bg-card rounded-xl p-5 shadow-lg cursor-pointer"
    @click="openIdea"
  >
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.name }}</h1>
      <img
        :src="liked ? '/liked.svg' : '/like.svg'"
        alt="Like"
        class="w-6 h-6 mr-2 duration-300 cursor-pointer"
        :class="{ 'animate-like': isAnimating }"
        @click.stop="toggleLike"
        @animationend="isAnimating = false"
      />
    </div>

    <p class="text-gray-300 mb-3">
      {{ idea.short_description || "Описание отсутствует" }}
    </p>

    <div class="mt-auto">
      <h3 class="text-xl text-white mb-3">
        Инициатор: {{ idea.initiator_info.name || "Неизвестный автор" }}
      </h3>

      <div class="flex flex-wrap gap-2">
        <!-- Проверяем, сколько стека технологий -->
        <span
          v-for="(tech, index) in idea.technologies_info.slice(0, 3)"
          :key="index"
          class="px-2 py-1 bg-purple-600 text-white rounded"
        >
          {{ tech.name }}
        </span>

        <!-- Если стека технологий больше 3, показываем "+X" -->
        <span
          v-if="idea.technologies_info.length > 3"
          class="text-xs text-white"
        >
          +{{ item.technologies_info.length - 3 }}
        </span>
      </div>
      <div class="flex justify-between">
        <span
          class="px-4 py-2 rounded-3xl text-white text-sm border-2 bg-zinc-700"
          :class="
            idea.status === 'Набор открыт'
              ? 'border-blue-500'
              : 'border-red-500'
          "
        >
          {{ status || 0 }}
        </span>
        <h3
          class="px-4 py-2 rounded-3xl text-white text-sm border-2 bg-zinc-700"
        >
          Команда из {{ participantsCount || 0 }} человек
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import { stackStyles } from "@/utils/stackStyles";

export default {
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      stackStyles,
      liked: false,
      isAnimating: false,
    };
  },
  methods: {
    openIdea() {
      this.$router.push(`/ideas/${this.idea.id}`);
    },
    toggleLike(event) {
      event.stopPropagation();
      this.liked = !this.liked;
      this.isAnimating = true;
    },
  },
};
</script>

<style scoped>
.idea-card {
  transition: transform 0.3s ease;
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
