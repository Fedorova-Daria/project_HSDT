<template>
  <div
    class="idea-card border border-zinc-700 bg-cards rounded-xl p-5 shadow-lg hover:border-purple-500 duration-300 cursor-pointer"
    @click="openIdea"
  >
    <!-- Заголовок и иконка лайка -->
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.title }}</h1>
      <img
        :src="liked ? '/liked-filled.svg' : '/liked.svg'"
        alt="Like"
        class="w-8 h-8 opacity-80 hover:opacity-100 duration-300 cursor-pointer"
        @click.stop="toggleLike"
      />
    </div>

    <!-- Описание -->
    <p class="text-gray-300 mb-3">{{ idea.description }}</p>

    <!-- Контент, который будет внизу карточки -->
    <div class="mt-auto">
      <!-- Инициатор -->
      <h3 class="text-xl text-white mb-3">Инициатор: {{ idea.author }}</h3>

      <!-- Стек технологий -->
      <div class="flex flex-wrap gap-2 mb-5">
        <span
          v-for="tech in idea.technologies"
          :key="tech"
          class="px-3 py-1 bg-green-500 text-white rounded-md"
        >
          {{ tech }}
        </span>
      </div>

      <!-- Статус идеи -->
      <div>
        <span
          class="px-4 py-2 rounded-md text-white"
          :class="idea.status === 'Набор открыт' ? 'bg-blue-500' : 'bg-red-500'"
        >
          {{ idea.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      liked: false, // Состояние лайка
    };
  },
  methods: {
    openIdea() {
      this.$router.push(`/idea/${this.idea.id}`); // Переход на страницу идеи
    },
    toggleLike(event) {
      event.stopPropagation(); // Предотвращаем всплытие события
      this.liked = !this.liked; // Переключаем состояние лайка
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
</style>
