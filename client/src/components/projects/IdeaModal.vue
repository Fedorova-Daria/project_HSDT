<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm z-100">
    <!-- Main modal -->
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative rounded-lg shadow-sm bg-card">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-zinc-600">
          <h3 class="text-lg font-semibold">
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
                class="block mb-2 text-sm font-medium"
                >Название проекта</label
              >
              <input
                v-model="form.title"
                type="text"
                name="name"
                id="name"
                class="bg-input border-dynamic text-sm rounded-lg block w-full p-2.5 focus:outline-none focus:ring-0 focus:border-none"
                placeholder="Какой вы придумали проект? Удивите нас!"
                required
              />
            </div>
            <div class="col-span-2">
    <label
      for="technologies"
      class="block mb-2 text-sm font-medium"
    >
      Выберите технологии
    </label>
    <div class="relative">
    <!-- Кнопка для открытия списка -->
    <div
      class="w-full border-dynamic rounded-md py-2 px-3 bg-input text-black cursor-pointer flex justify-between items-center transition-colors"
      @click="dropdownOpen = !dropdownOpen"
    >
      <span>Выберите технологии</span>
      <span :class="{ 'rotate-180': dropdownOpen }" class="transition-transform">
        &#9660;
      </span>
    </div>

    <!-- Выпадающий список -->
    <div
      v-if="dropdownOpen"
      class="flex flex-col absolute left-0 w-full bg-input rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-50 transition-colors"
    >
      <!-- Поле поиска -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск..."
        class="w-full px-3 py-2 border-b border-fiol outline-none transition-colors"
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
    <div class="flex flex-wrap gap-2 mb-2">
  <span
    v-for="id in selectedTechnologies"
    :key="id"
    class="px-2 py-1 text-sm bg-gray-200 rounded-full"
  >
    {{ technologies.find(t => t.id === id)?.name }}
  </span>
</div>
  </div>
  </div>
    <div class="dropdown" @click="toggleDropdownSem" tabindex="0" @blur="closeDropdownSem">
    <div class="dropdown-selected">
      {{ selectedLabel || 'Выберите семестр' }}
      <span class="arrow">{{ dropdownOpenSem ? '▲' : '▼' }}</span>
    </div>

    <div v-if="dropdownOpenSem" class="dropdown-menu">
      <ul>
        <li v-for="year in years" :key="year" class="dropdown-year">
          <div @click.stop="toggleYear(year)">
            {{ year }}
            <span>{{ openedYear === year ? '-' : '+' }}</span>
          </div>

          <ul v-if="openedYear === year" class="dropdown-semesters">
            <li 
              v-for="semester in semestersByYear[year]" 
              :key="semester.id" 
              @click.stop="selectSemester(semester)"
              :class="{ selected: semester.id === selectedSemesterId }"
            >
              {{ semesterDisplay(semester.semester) }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
<div class="col-span-2">
<!-- Кнопка для открытия списка институтов -->
<div
  class="w-full border-dynamic rounded-md py-2 px-3 bg-input text-black cursor-pointer flex justify-between items-center transition-colors"
  @click="instituteDropdownOpen = !instituteDropdownOpen"
>
  <span>Выберите институты</span>
  <span :class="{ 'rotate-180': instituteDropdownOpen }" class="transition-transform">
    &#9660;
  </span>
</div>

<!-- Выпадающий список институтов -->
<div
  v-if="instituteDropdownOpen"
  class="flex flex-col absolute left-0 w-full bg-input rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-50 transition-colors"
>
  <!-- Поле поиска -->
  <input
    v-model="instituteSearchQuery"
    type="text"
    placeholder="Поиск..."
    class="w-full px-3 py-2 border-b border-fiol outline-none transition-colors"
  />

  <!-- Список институтов -->
  <div
    v-for="(name, code) in filteredInstitutes"
    :key="code"
    @click="toggleInstitute(code)"
    class="p-2 cursor-pointer hover:bg-gray-200 transition-colors duration-300"
  >
    <input
      type="checkbox"
      :id="code"
      :value="code"
      v-model="selectedInstitutes"
      class="mr-2"
    />
    {{ name }}
  </div>
</div>

<!-- Отображение выбранных институтов -->
<div class="flex flex-wrap gap-2 mt-2">
  <span
    v-for="code in selectedInstitutes"
    :key="code"
    class="px-2 py-1 text-sm bg-gray-200 rounded-full"
  >
    {{ instituteNames[code] }}
  </span>
</div>
</div>

            <div class="col-span-2">
              <label
                for="description"
                class="block mb-2 text-sm font-medium"
                >Расскажите о том, что нужно сделать</label
              >
              <textarea
                v-model="form.description"
                id="description"
                rows="4"
                class="block mt-3 p-2.5 w-full text-sm bg-input rounded-lg border border-dynamic focus:outline-none focus:ring-0 focus:border-none"
                placeholder="Напишите подробное описание проекта здесь"
                required
              ></textarea>
            </div>
          </div>
          <div class="flex justify-between gap-4">
            <button
              @click="submitIdea(userRole === 'CU' || userRole === 'EX' ? 'new' : userRole === 'ST' ? 'open' : 'default')"
                        :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
              type="button"
              class="text-always-white inline-flex items-center focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
              </svg>
              Добавить новый проект
            </button>

            <button
              @click="submitIdea('draft')"
              type="button"
              class=" text-always-white inline-flex items-center bg-gray-400 hover:bg-gray-500 focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
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
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth";

export default {
  inject: ["globalState"],
  data() {
    return {
      userRole: null,
      instituteDropdownOpen: false,
    instituteSearchQuery: "",
    selectedInstitutes: [],
    instituteNames: {
      HSDT: "ВШЦТ",
      ARCHID: "АРХИД",
      IPTI: "ИПТИ",
      STROIN: "СТРОИН",
      TYIU: "ТИУ",
    },
      currentBgColor: "",
      form: {
        title: '',
        description: '',
        technologies: [], // Массив для выбранных технологий
        semester: null, 
        institutes: [],
      },
      dropdownOpen: false,
      searchQuery: "",
      selectedTechnologies: [], // Массив для выбранных технологий
      technologies: [], // Массив всех технологий
      filteredTechnologies: [], // Отфильтрованные технологии
      semesters: [],          // Все семестры с API
      dropdownOpenSem: false,
      selectedYear: null,
      openedYear: null,           // Какой год раскрыт
      selectedSemesterId: null, // Выбранный семестр (ID)
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute]; // Используем глобальное состояние
      return style || { buttonOffColor: "#ccc" }; // Дефолтный стиль
    },
    years() {
      return [...new Set(this.semesters.map(s => s.year))].sort((a,b) => b - a);
    },
    semestersByYear() {
      return this.semesters.reduce((acc, s) => {
        if (!acc[s.year]) acc[s.year] = [];
        acc[s.year].push(s);
        return acc;
      }, {});
    },
    selectedLabel() {
    if (!this.selectedSemesterId || !this.semesters.length) return null;
    const semester = this.semesters.find(s => s.id === this.selectedSemesterId);
    return semester ? `${semester.year} год, ${this.semesterDisplay(semester.semester)}` : null;
  },
  filteredInstitutes() {
      const query = this.instituteSearchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.instituteNames).filter(([code, name]) =>
          name.toLowerCase().includes(query)
        )
      );
    },
  },
  methods: {
    toggleInstitute(code) {
      const index = this.selectedInstitutes.indexOf(code);
      if (index === -1) {
        this.selectedInstitutes.push(code);
      } else {
        this.selectedInstitutes.splice(index, 1);
      }
    },
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
    async fetchSemesters() {
      try {
        const response = await api.get('/core/semesters/');
        this.semesters = response.data;
      } catch (e) {
        console.error(e);
      }
    },
    toggleDropdownSem() {
      this.dropdownOpenSem = !this.dropdownOpenSem;
      if (!this.dropdownOpenSem) {
        this.openedYear = null;
      }
    },
    closeDropdownSem() {
      this.dropdownOpenSem = false;
      this.openedYear = null;
    },
    toggleYear(year) {
      this.openedYear = this.openedYear === year ? null : year;
    },
    selectSemester(semester) {
  this.selectedSemesterId = semester.id;
  this.dropdownOpenSem = false;
  this.openedYear = null;
  // Можно обновить form.semester сразу
  this.form.semester = semester.id;
  // Или оставить в submitIdea
},
    semesterDisplay(code) {
      return code === 'spring' ? 'Весенний' : 'Зимний';
    },
async submitIdea(status) {
  const validStatuses = ['draft', 'open', 'review', 'new'];
  if (!validStatuses.includes(status)) {
    console.error(`Невалидный статус: ${status}`);
    return;
  }

  // Обновляем form.technologies перед отправкой
  this.form.technologies = this.selectedTechnologies;
  this.form.semester = this.selectedSemesterId;
  this.form.institutes = this.selectedInstitutes;

  const data = {
    ...this.form,
    status,
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
    this.fetchSemesters();
    const technologiesData = await fetchTechnologies(); // Загружаем данные
    if (technologiesData) {
      this.technologies = technologiesData; // Обновляем массив технологий
      this.filteredTechnologies = technologiesData; // Изначально показываем все технологии
    }
  },
  created() {
  const userDataStr = localStorage.getItem('userData');
  if (userDataStr) {
    try {
      const userData = JSON.parse(userDataStr);
      this.userRole = userData.role;
    } catch (e) {
      console.error('Ошибка парсинга userData из localStorage', e);
    }
  }
},
  watch: {
    technologies(newTechs) {
      this.filteredTechnologies = newTechs;
    },
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.dropdown {
  position: relative;
  width: 250px;
  user-select: none;
  border: 1px solid #aaa;
  border-radius: 4px;
  cursor: pointer;
}
.dropdown-selected {
  padding: 8px 12px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #aaa;
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
}
.dropdown-year > div {
  padding: 8px 12px;
  background: #f0f0f0;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
}
.dropdown-semesters {
  list-style: none;
  padding-left: 16px;
  margin: 0;
  background: #fafafa;
}
.dropdown-semesters li {
  padding: 6px 12px;
}
.dropdown-semesters li.selected {
  background-color: #d3eaff;
  font-weight: 600;
}
.dropdown-semesters li:hover {
  background-color: #e0f0ff;
}
/* Немного мягче фон */
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
input::placeholder {
  color: var(--text-colorinput);
  opacity: 1; /* Сделать непрозрачным */
}
</style>