<!-- src/components/Rialto.vue -->
<!-- src/components/IdeaMaker.vue -->
<template>
  <div>
    <button
      @click="openModal"
      class="bg-purple-600 text-white px-4 py-2 rounded"
    >
      Создать идею
    </button>
    <IdeaModal :isOpen="isModalOpen" @close="closeModal" />
  </div>
</template>

<script>
import IdeaModal from "./IdeaModal.vue";

export default {
  components: { IdeaModal },
  data() {
    return {
      isModalOpen: false,
    };
  },
  methods: {
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
/* Стили для кнопки или компонента */
</style>
