<template>
  <div
    class="idea-card border border-zinc-700 bg-cards rounded-xl p-5 shadow-lg cursor-pointer"
    @click="openIdea"
  >
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.name }}</h1>
      <img
        :src="liked ? '/liked1.svg' : '/like.svg'"
        alt="Like"
        class="w-6 h-6 mr-4 mb-5 duration-300 cursor-pointer"
        :class="{ 'animate-like': isAnimating }"
        @click.stop="toggleLike"
        @animationend="isAnimating = false"
      />
    </div>

    <p class="text-gray-300 mb-3">
      {{ idea.short_Description || "Описание отсутствует" }}
    </p>

    <div class="mt-auto">
      <h3 class="text-xl text-white mb-3">
        Инициатор: {{ idea.initiator_info || "Неизвестный автор" }}
      </h3>

      <div class="flex flex-wrap gap-1 mb-5">
        <span
          v-for="tech in technologies"
          :key="tech"
          class="text-m font-medium me-2 px-2.5 py-0.5 rounded-sm border-1"
          :class="getTechStyle(tech)"
        >
          {{ tech }}
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
    getTechStyle(tech) {
      return (
        this.stackStyles[tech] || {
          bg: "bg-gray-100",
          text: "text-gray-800",
          border: "border-gray-400",
        }
      );
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
