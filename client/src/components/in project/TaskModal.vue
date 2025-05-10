<template>
    <transition name="slide">
      <div v-if="localTask" class="fixed right-0 top-0 h-full w-96 bg-white dark:bg-gray-700 shadow-lg z-50 p-6 overflow-y-auto">
        <!-- Заголовок -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
            <input
              v-model="localTask.title"
              class="w-full px-2 py-1 text-lg font-semibold bg-white dark:bg-gray-600 rounded border border-gray-300 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
            ✖
          </button>
        </div>
  
        <!-- Описание задачи -->
        <textarea
          v-model="localTask.message"
          class="w-full h-40 p-2 border rounded resize-none bg-gray-100 dark:bg-gray-600 text-gray-900 dark:text-gray-100"
          placeholder="Введите описание задачи..."
        ></textarea>
  
        <!-- Выбор исполнителя -->
        <div class="mt-4">
          <label class="block text-gray-700 dark:text-gray-300 font-medium mb-2">Назначить исполнителя:</label>
          <select v-model="localTask.assigned_to" class="w-full p-2 border rounded bg-gray-100 dark:bg-gray-600">
            <option v-for="member in teamMembers" :key="member.id" :value="member.id">
              {{ member.full_name }}
            </option>
          </select>
        </div>
  
        <!-- Отображение списка участников -->
        <div class="mt-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Участники команды:</h3>
          <ul class="mt-2">
            <li v-for="member in teamMembers" :key="member.id" class="text-gray-700 dark:text-gray-300">
              {{ member.full_name }}
            </li>
          </ul>
        </div>
  
        <!-- Кнопки -->
        <div class="flex justify-end space-x-3 mt-4">
          <button @click="saveTask" class="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">
            Сохранить
          </button>
          <button @click="closeModal" class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400">
            Закрыть
          </button>
        </div>
      </div>
    </transition>
  </template>
  
  <script>
  import api from "@/composables/auth.js";  
  
  export default {
    props: {
      task: Object, // Получаем задачу
      teamMembers: Array, // Получаем список участников команды
    },
    data() {
      return {
        localTask: null, // Локальная копия задачи
      };
    },
    watch: {
      task: {
        immediate: true,
        handler(newTask) {
          this.localTask = JSON.parse(JSON.stringify(newTask)); // Создаем глубокую копию задачи
        },
      },
    },
    methods: {
      getMemberFullName(memberId) {
        const member = this.teamMembers?.find((m) => m.id === memberId);
        return member ? member.full_name : "Неизвестный";
      },
      async saveTask() {
        try {
          await api.patch(`/kanban/tasks/${this.localTask.id}/`, {
            title: this.localTask.title,
            message: this.localTask.message,
            assigned_to: this.localTask.assigned_to,
          });
  
          console.log("✅ Задача обновлена:", this.localTask);
  
          // Обновляем `task` напрямую
          Object.assign(this.task, this.localTask);
  
          this.closeModal();
        } catch (error) {
          console.error("❌ Ошибка при обновлении задачи:", error);
        }
      },
      closeModal() {
        this.localTask = null; // Закрываем модальное окно
      },
    },
  };
  </script>
  
  <style scoped>
  .slide-enter-active, .slide-leave-active {
    transition: transform 0.3s ease-in-out;
  }
  .slide-enter, .slide-leave-to {
    transform: translateX(100%);
  }
  </style>
  