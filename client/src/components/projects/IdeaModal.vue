<template>
  <div
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm"
  >
    <!-- Main modal -->
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative rounded-lg shadow-sm bg-card">
        <!-- Modal header -->
        <div
          class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-zinc-600"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Создать новый проект
          </h3>
          <button
            @click="closeModal"
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-toggle="crud-modal"
          >
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 14"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
              />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <!-- Modal body -->
        <form @submit.prevent="submitIdea" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label
                for="name"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Название проекта</label
              >
              <input
                v-model="ideaTitle"
                type="text"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-zinc-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Какой вы придумали проект? Удивите нас!"
                required
              />
            </div>
            <div class="col-span-2 sm:col-span-1">
      <div class="flex items-start text-white">
        <div class="flex items-center h-5">
          <input
            id="needDevHelp"
            type="checkbox"
            v-model="needHelp"
            class="w-4 h-4 border border-gray-300 rounded-sm bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
          />
        </div>
        <label for="needDevHelp" class="ms-2 text-sm font-medium">
          Вам нужна помощь программиста?
        </label>
      </div>
    </div>

    <!-- Стек технологий (показывается только если выбран чекбокс) -->
    <div v-if="needHelp" class="col-span-2 sm:col-span-1">
      <label
        for="category"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        Стек технологий
      </label>
      <div class="relative">
        <!-- Кнопка для открытия выпадающего списка -->
        <button
          @click="toggleDropdown"
          class="flex justify-between text-white bg-blue-700 hover:bg-blue-800 w-45 font-medium rounded-lg text-sm px-2 py-3 text-left items-center dark:bg-zinc-600 dark:hover:bg-zinc-700"
          type="button"
        >
          Выбрать стек
          <svg
            class="w-4 h-4 ml-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
        <!-- Выпадающее меню с прокруткой -->
        <div
          v-if="isDropdownOpen"
          class="absolute z-10 w-48 bg-zinc-700 divide-y divide-zinc-600 rounded-lg shadow-sm"
          style="top: 100%; left: 0; max-height: 200px; overflow-y: auto;"
        >
          <ul class="p-3 space-y-3 text-sm text-gray-700 dark:text-gray-200">
            <li v-for="(stack, index) in stacks" :key="index">
              <div class="flex items-center">
                <input
                  :id="'checkbox-item-' + index"
                  type="checkbox"
                  v-model="selectedStacks"
                  :value="stack"
                  class="w-4 h-4 text-purple-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-purple-600 dark:focus:ring-purple-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                />
                <label :for="'checkbox-item-' + index" class="ms-2 text-sm font-medium text-gray-300">
                  {{ stack }}
                </label>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Выбранные технологии -->
      <div class="mt-2 flex flex-wrap gap-2">
        <span
          v-for="tech in selectedStacks"
          :key="tech"
          class="px-2 py-1 bg-purple-600 text-white rounded"
        >
          {{ tech }}
        </span>
      </div>
    </div>

            <div class="col-span-2">
              <label
                for="description"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Расскажите о том, что нужно сделать</label
              >
              <textarea
                v-model="description"
                id="description"
                rows="4"
                class="block mt-3 p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-zinc-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Напишите подробное описание проекта здесь"
                required
              ></textarea>
            </div>
          </div>
          <div class="flex justify-between gap-4">
  <button
    @click="submitIdea('open')"
    type="button"
    class="text-white inline-flex items-center bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-800"
  >
    <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
    </svg>
    Добавить новый проект
  </button>

  <button
    @click="submitIdea('draft')"
    type="button"
    class="text-white inline-flex items-center bg-gray-500 hover:bg-gray-600 focus:ring-4 focus:outline-none focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
  >
    <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
    </svg>
    Отложить проект
  </button>
</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { fetchAccessToken } from "@/utils/auth.js"; // Импортируем утилиту для получения актуального токена

export default {
  data() {
    return {
      needHelp: false, // Следим за чекбоксом "Нужна помощь"
      isDropdownOpen: false, // Флаг для управления состоянием выпадающего списка
      selectedStacks: [], // Массив для выбранных технологий
      ideaTitle: "", // Название проекта
      description: "", // Описание проекта
      stacks: [
        "Vue",
        "React",
        "Angular",
        "Svelte",
        "Python",
        "Node.js",
        "Django",
      ], // Массив стеков
    };
  },
  methods: {
    closeModal() {
      this.$emit("close"); // Сообщаем родителю закрыть окно
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    async submitIdea(status) {
  try {
    // Получаем токен, обновляя его при необходимости
    const token = await fetchAccessToken();

    if (!token) {
      console.error("Ошибка: токен отсутствует.");
      return;
    }

    // Преобразуем выбранные технологии в ID
    const technologyIds = this.selectedStacks.map(stack => {
      return this.stacks.findIndex(item => item === stack) + 1; // Здесь предполагается, что ID = индексу + 1
    });

    // Формируем данные
    const ideaData = {
      name: this.ideaTitle,
      description: this.description,
      technologies: technologyIds, // Технологии
      status: status, // Указываем переданный статус ("open" или "draft")
    };

    // Отправляем запрос
    const response = await axios.post(
      "http://127.0.0.1:8000/api/projects/create/", 
      ideaData, 
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }
    );

    console.log(`Идея со статусом "${status}" создана успешно:`, response.data);
    this.closeModal(); // Закрываем модальное окно после успешного создания

  } catch (error) {
    console.error("Ошибка при создании идеи:", error.response?.data || error.message);
  }
}
  },
    };
</script>

<style scoped>
/* Немного мягче фон */
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
</style>
