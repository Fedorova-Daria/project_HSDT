<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm">
    <!-- Main modal -->
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative rounded-lg shadow-sm bg-card">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-zinc-600">
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
                v-model="form.title"
                type="text"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-zinc-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Какой вы придумали проект? Удивите нас!"
                required
              />
            </div>

            <div class="col-span-2">
    <label
      for="technologies"
      class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
    >
      Выберите технологии
    </label>
    <div class="relative">
    <!-- Кнопка для открытия списка -->
    <div
      class="w-full border border-fiol rounded-md py-2 px-3 bg-white text-black cursor-pointer flex justify-between items-center transition-colors hover:border-purple-500 focus:border-purple-600"
      @click="dropdownOpen = !dropdownOpen"
    >
      <span>{{ selectedTechnologies.length ? selectedTechnologies.join(", ") : "Выберите технологии" }}</span>
      <span :class="{ 'rotate-180': dropdownOpen }" class="transition-transform">
        &#9660;
      </span>
    </div>

    <!-- Выпадающий список -->
    <div
      v-if="dropdownOpen"
      class="flex flex-col absolute left-0 w-full bg-white border-3 border-solid border-fiol rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-50 transition-colors hover:border-purple-500"
    >
      <!-- Поле поиска -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск..."
        class="w-full px-3 py-2 border-b border-fiol outline-none transition-colors hover:border-purple-500 focus:border-purple-600"
        @input="filterTechnologies"
      />

      <!-- Список технологий -->
      <div
        v-for="tech in filteredTechnologies"
        :key="tech.id"
        @click="toggleTechnology(tech)"
        class="p-2 cursor-pointer hover:bg-gray-200 transition-colors duration-300"
      >
        <input
          type="checkbox"
          :id="tech.id"
          :value="tech.id"
          v-model="selectedTechnologies"
          class="mr-2"
        />
        {{ tech.name }}
      </div>
    </div>
  </div>
  </div>

            <div class="col-span-2">
              <label
                for="description"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Расскажите о том, что нужно сделать</label
              >
              <textarea
                v-model="form.description"
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
import { ref, onMounted } from 'vue';
import { createIdeaOrProject } from "@/services/create"; // Импортируем метод создания
import { fetchTechnologies } from "@/services/technologies.js";

export default {
  data() {
    return {
      form: {
        title: '',
        description: '',
        technologies: [], // Массив для выбранных технологий
      },
      dropdownOpen: false,
      searchQuery: "",
      selectedTechnologies: [], // Массив для выбранных технологий
      technologies: [], // Массив всех технологий
      filteredTechnologies: [], // Отфильтрованные технологии
    };
  },
  methods: {
    toggleTechnology(tech) {
      const index = this.selectedTechnologies.indexOf(tech.id);
      if (index > -1) {
        this.selectedTechnologies.splice(index, 1);
      } else {
        this.selectedTechnologies.push(tech.id);
      }
    },
    filterTechnologies() {
      const query = this.searchQuery.toLowerCase();
      this.filteredTechnologies = this.technologies.filter((tech) =>
        tech.name.toLowerCase().includes(query)
      );
    },
    async submitIdea(status) {
  // Проверка, что статус один из допустимых
  const validStatuses = ['draft', 'open', 'under_review'];
  if (!validStatuses.includes(status)) {
    console.error(`Невалидный статус: ${status}`);
    return;
  }

  const data = {
    ...this.form,
    status, // передаем статус без кавычек
  };
  try {
    const response = await createIdeaOrProject(data);
    console.log("Создано:", response);
  } catch (error) {
    console.error("Ошибка при создании:", error);
  }
},
    closeModal() {
      this.$emit("close");
    },
  },
  async mounted() {
    const technologiesData = await fetchTechnologies(); // Загружаем данные
    if (technologiesData) {
      this.technologies = technologiesData; // Обновляем массив технологий
      this.filteredTechnologies = technologiesData; // Изначально показываем все технологии
    }
  },
  watch: {
    technologies(newTechs) {
      this.filteredTechnologies = newTechs;
    },
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