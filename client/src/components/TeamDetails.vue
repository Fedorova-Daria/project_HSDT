<template>
  <div>
    <!-- Шапка -->
    <Header />
    <div class="p-6 w-4/5 mx-auto">
      <!-- Кнопка "Назад" -->
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors mb-6"
        @click="goBack"
      >
        Назад
      </button>

      <!-- Блоки -->
      <div class="space-y-6">
        <!-- Первый  -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-bold mb-4">Блок 1</h2>
          <p>Тут типо всякая инфа о команде</p>
        </div>

        <!-- Второй  -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-bold mb-4">Блок 2</h2>
          <p>Тут тоже</p>
        </div>

        <!-- Третий  -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-bold mb-4">Блок 3</h2>
          <p>Ну и тут</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue"; // Импортируем шапку

export default {
  components: {
    Header,
  },
  methods: {
    goBack() {
      this.$router.go(-1); // Возврат на предыдущую страницу
    },
  },
};
</script>

<style scoped>
/* Дополнительные стили, если нужно */
</style>
