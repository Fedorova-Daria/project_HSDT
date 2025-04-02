<template>
  <div>
    <Header />
    <div class="p-6 w-4/5 mx-auto">
      <!-- Кнопка "Назад" -->
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors mb-6 btn cursor-pointer"
        @click="goBack"
      >
        Назад
      </button>

      <!-- Форма редактирования -->
      <div v-if="isEditing">
        <h2 class="text-white text-xl mb-4">Редактирование команды</h2>
        <form @submit.prevent="saveChanges">
          <div class="mb-4">
            <label class="block text-white mb-2">Название команды</label>
            <input
              v-model="editedTeam.name"
              type="text"
              class="w-full p-2 rounded bg-zinc-700 text-white"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-white mb-2">Статус</label>
            <select
              v-model="editedTeam.status"
              class="w-full p-2 rounded bg-zinc-700 text-white"
            >
              <option value="В работе">В работе</option>
              <option value="В поисках">В поисках</option>
              <option value="Неактивна">Неактивна</option>
              <option value="Проверяем">Проверяем</option>
              <option value="Забанена">Забанена</option>
            </select>
          </div>
          <div class="flex justify-end">
            <button
              type="button"
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2 btn cursor-pointer"
              @click="cancelEditing"
            >
              Отмена
            </button>
            <button
              type="submit"
              class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors btn cursor-pointer"
            >
              Сохранить
            </button>
          </div>
        </form>
      </div>

      <!-- Отображение информации о команде -->
      <div v-else class="space-y-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-bold mb-4">Название команды</h2>
          <p>{{ team.name }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-bold mb-4">Статус</h2>
          <p>{{ team.status }}</p>
        </div>

        <!-- Кнопка "Редактировать" -->
        <button
          class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors btn cursor-pointer"
          @click="startEditing"
        >
          Редактировать
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";

export default {
  components: {
    Header,
  },
  props: ['institute', 'teamId'],
  data() {
    return {
      team: null,
      isEditing: false, // Режим редактирования
      team: {
        name: "Команда 1",
        status: "В работе",
      },
      editedTeam: {}, // Копия команды для редактирования
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    startEditing() {
      // Включаем режим редактирования и копируем данные
      this.isEditing = true;
      this.editedTeam = { ...this.team };
    },
    cancelEditing() {
      // Отключаем режим редактирования
      this.isEditing = false;
    },
    saveChanges() {
      // Сохраняем изменения и отключаем режим редактирования
      this.team = { ...this.editedTeam };
      this.isEditing = false;
      console.log("Изменения сохранены:", this.team);
    },
  },
};
</script>

<style scoped>
/* Дополнительные стили, если нужно */
</style>
