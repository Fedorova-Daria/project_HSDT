<!-- src/components/Rialto.vue -->
<template>
  <div>
    <button @click="goToIdeaMaker">Создать идею</button>
  </div>
</template>

<script>
export default {
  name: "Rialto",
  methods: {
    goToIdeaMaker() {
      // Переход к странице создания идеи
      this.$router.push({ name: "IdeaMaker" });
    },
  },
};
</script>

<style scoped>
/* Стили для кнопки или компонента */
</style>
