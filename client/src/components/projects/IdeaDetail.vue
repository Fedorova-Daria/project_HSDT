<template>
  <div
    class="fixed top-0 right-0 w-1/2 h-full bg-zinc-800 bg-opacity-75 rounded-lg p-4 modal"
    @click.self="closeModal"
  >
    <div class="w-full h-full bg-card rounded-lg p-6 overflow-auto">
      <h2 class="text-2xl font-semibold mb-4">{{ idea.name }}</h2>
      <p class="mb-4">{{ idea.description }}</p>
      <p><strong>Инициатор:</strong> {{ idea.initiator_name }}</p>
      <p><strong>Роль:</strong> {{ idea.initiator_role }}</p>
      <p><strong>Дата создания:</strong> {{ idea.created_at }}</p>
      <button
        @click="closeModal"
        class="bg-red-500 text-white py-2 px-4 rounded-md mt-4 hover:bg-red-600"
      >
        Закрыть
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    ideaId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      idea: {},
    };
  },
  watch: {
    ideaId(newId) {
      if (newId) {
        this.fetchIdeaDetails(newId);
      }
    }
  },
  methods: {
    async fetchIdeaDetails(id) {
      try {
        const response = await axios.get(`http://localhost:8000/api/ideas/${id}/`);
        this.idea = response.data;
      } catch (error) {
        console.error('Ошибка при получении информации об идее:', error);
      }
    },
    closeModal() {
      this.$emit('close');
    }
  },
  created() {
    if (this.ideaId) {
      this.fetchIdeaDetails(this.ideaId);
    }
  }
};
</script>

<style scoped>
@keyframes slideInFromRight {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(0);
  }
}

@keyframes slideOutToRight {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(100%);
  }
}

.modal {
  position: fixed;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.5);
  z-index: 9999;
  transform: translateX(100%); /* Начальная позиция */
  transition: transform 0.5s ease-in-out; /* Плавный переход */
}
</style>