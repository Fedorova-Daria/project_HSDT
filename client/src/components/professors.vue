<template>
  <div>
    <!-- Размытый фон, который следует за курсором -->
    <div class="blurred-bg" :style="bgStyle"></div>

    <Header />
    <div class="p-6 w-4/5 mx-auto relative mt-10">
      <h1 class="font-display text-5xl font-bold mb-6">
        Студенты
      </h1>
      <hr class="divider" />

      <!-- Фильтры и сортировка -->
      <div class="flex flex-wrap items-center gap-4 mb-6 mt-5">
        <!-- Фильтр по институту -->
        <div class="relative">
          <button
            @click="toggleInstituteDropdown"
            class="flex items-center px-4 py-2 rounded-md transition-all duration-500 border border-zinc-400 bg-card hover:shadow-md h-10"
          >
            {{ selectedInstituteFilter || "Выберите институт" }}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
          <ul
            v-if="showInstituteDropdown"
            class="absolute left-0 w-48 mt-1 bg-input text-dynamic rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
          >
            <li
              v-for="institute in institutes"
              :key="institute"
              @click="selectInstitute(institute)"
              class="py-2 px-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors"
            >
              {{ institute }}
            </li>
          </ul>
        </div>

        <!-- Фильтр по группе -->
        <div class="relative" v-if="selectedInstituteFilter">
          <button
            @click="toggleGroupDropdown"
            class="flex items-center px-4 py-2 rounded-md transition-all duration-500 border border-zinc-400 hover:shadow-md h-10 bg-card"
          >
            {{ selectedGroupFilter || "Выберите группу" }}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
          <ul
            v-if="showGroupDropdown"
            class="absolute left-0 w-48 mt-1 bg-input text-dynamic rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
          >
            <li
              v-for="group in filteredGroups"
              :key="group"
              @click="selectGroup(group)"
              class="py-2 px-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors"
            >
              {{ group }}
            </li>
          </ul>
        </div>

        <!-- Сортировка -->
        <div class="relative">
          <button
            @click="toggleSortDropdown"
            class="flex items-center px-4 py-2 rounded-md transition-all duration-500 border border-zinc-400 hover:shadow-md h-10 bg-card"
            >
            {{ sortOptions.find((opt) => opt.value === currentSort).label }}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
          <ul
            v-if="showSortDropdown"
            class="absolute left-0 w-48 mt-1 bg-input rounded-lg shadow-lg z-50"
          >
            <li
              v-for="option in sortOptions"
              :key="option.value"
              @click="selectSort(option.value)"
              class="py-2 px-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors"
            >
              {{ option.label }}
            </li>
          </ul>
        </div>

        <!-- Кнопка сброса фильтров -->
        <button
          @click="resetFilters"
          class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
          :style="{ backgroundColor: currentBgColorBtnReset }"
          @mouseover="currentBgColorBtnReset = instituteStyle.buttonOnColor"
          @mouseleave="currentBgColorBtnReset = instituteStyle.buttonOffColor"
        >
          Сбросить фильтры
        </button>
      </div>

      <!-- Таблица студентов -->
      <div class="overflow-x-auto rounded-lg shadow-lg">
        <table class="min-w-full bg-card">
          <thead class="bg-input">
            <tr>
              <th class="py-3 px-6 text-left">Имя студента</th>
              <th class="py-3 px-6 text-left">Почта студента</th>
              <th class="py-3 px-6 text-left">Команда</th>
              <th class="py-3 px-6 text-left">Идея</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr
              v-for="(student, index) in filteredStudents"
              :key="index"
              class="hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-300"
            >
              <td class="py-4 px-6">
                <div class="flex items-center">
                  <div
                    class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden mr-4"
                  >
                    <img
                      v-if="student.avatar"
                      :src="student.avatar"
                      alt="Avatar"
                      class="object-cover w-full h-full"
                    />
                    <div
                      v-else
                      class="w-full h-full flex items-center justify-center bg-gray-300 dark:bg-gray-600"
                    >
                      <span class="font-semibold">{{
                        getInitials(student.name)
                      }}</span>
                    </div>
                  </div>
                  <div>
                    <div class="font-medium">{{ student.name }}</div>
                  </div>
                </div>
              </td>
              <td class="py-4 px-6">{{ student.email }}</td>
              <td class="py-4 px-6">
                <div class="flex items-center">
                  <div
                    v-if="student.team"
                    class="bg-input px-3 py-1 rounded-full"
                  >
                    {{ student.team }}
                  </div>
                  <span v-else class="text-gray-500 dark:text-gray-400"
                    >Не состоит</span
                  >
                </div>
              </td>
              <td class="py-4 px-6">
                <div v-if="student.idea" class="flex items-center">
                  <div
                    class="bg-input px-3 py-1 rounded-full"
                  >
                    {{ student.idea }}
                  </div>
                </div>
                <span v-else class="text-gray-500 dark:text-gray-400"
                  >Не работает</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth";

export default {
  name: "Professors",
  inject: ["globalState"],
  components: {
    Header,
  },
  data() {
    return {
      students: [],
      filteredStudents: [],
      bgPosition: { x: 0, y: 0 },
      targetPosition: { x: 0, y: 0 },
      lerpFactor: 0.1,
      currentBgColorBtnReset: "",

      // Фильтры
      institutes: ["ВШЦТ", "АРХИД", "ИПТИ", "СТРОИН", "ТИУ"],
      groups: {
        ВШЦТ: ["ЦТ-21", "ЦТ-22", "ЦТ-23", "ЦТ-24"],
        АРХИД: ["АД-31", "АД-32", "АД-33"],
        ИПТИ: ["ИТ-41", "ИТ-42", "ИТ-43"],
        СТРОИН: ["СТ-51", "СТ-52"],
        ТИУ: ["ТУ-61", "ТУ-62", "ТУ-63"],
      },
      selectedInstituteFilter: null,
      selectedGroupFilter: null,
      showInstituteDropdown: false,
      showGroupDropdown: false,

      // Сортировка
      sortOptions: [
        { label: "По алфавиту (А-Я)", value: "name_asc" },
        { label: "По алфавиту (Я-А)", value: "name_desc" },
        { label: "По командам (А-Я)", value: "team_asc" },
        { label: "По командам (Я-А)", value: "team_desc" },
      ],
      currentSort: "name_asc",
      showSortDropdown: false,
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      return (
        instituteStyles[this.selectedInstitute] || { buttonOffColor: "#ccc" }
      );
    },
    bgStyle() {
      return {
        backgroundImage: "url('/bob.svg')",
        backgroundPosition: `${this.bgPosition.x}px ${this.bgPosition.y}px`,
      };
    },
    filteredGroups() {
      if (!this.selectedInstituteFilter) return [];
      return this.groups[this.selectedInstituteFilter] || [];
    },
  },
  methods: {
    async fetchStudents() {
      try {
        // Здесь должен быть реальный API-запрос
        // const response = await api.get("/students/");

        // Временно используем мок-данные
        this.students = [
          {
            id: 1,
            name: "Иванов Иван Иванович",
            email: "ivanov@example.com",
            faculty: "ВШЦТ",
            group: "ЦТ-21",
            team: "Команда А",
            idea: "Образовательная платформа",
            avatar: null,
          },
          {
            id: 2,
            name: "Петрова Анна Сергеевна",
            email: "petrova@example.com",
            faculty: "АРХИД",
            group: "АД-31",
            team: "Команда Б",
            idea: "Дизайн городской среды",
            avatar: "/path/to/avatar.jpg",
          },
          {
            id: 3,
            name: "Сидоров Алексей Дмитриевич",
            email: "sidorov@example.com",
            faculty: "ИПТИ",
            group: "ИТ-42",
            team: null,
            idea: null,
            avatar: null,
          },
          {
            id: 4,
            name: "Кузнецова Екатерина Викторовна",
            email: "kuznetsova@example.com",
            faculty: "СТРОИН",
            group: "СТ-51",
            team: "Команда В",
            idea: "Строительные инновации",
            avatar: null,
          },
          {
            id: 5,
            name: "Николаев Денис Олегович",
            email: "nikolaev@example.com",
            faculty: "ТИУ",
            group: "ТУ-62",
            team: "Команда Г",
            idea: "Технологии будущего",
            avatar: null,
          },
          {
            id: 6,
            name: "Алексеев Михаил Петрович",
            email: "alekseev@example.com",
            faculty: "ВШЦТ",
            group: "ЦТ-22",
            team: "Команда Д",
            idea: "Мобильное приложение",
            avatar: null,
          },
          {
            id: 7,
            name: "Васильева Ольга Игоревна",
            email: "vasilyeva@example.com",
            faculty: "АРХИД",
            group: "АД-32",
            team: "Команда Е",
            idea: "Архитектурный проект",
            avatar: null,
          },
          {
            id: 8,
            name: "Григорьев Павел Сергеевич",
            email: "grigoriev@example.com",
            faculty: "ИПТИ",
            group: "ИТ-41",
            team: "Команда Ж",
            idea: "Веб-платформа",
            avatar: null,
          },
        ];

        // Инициализируем отфильтрованный список
        this.filteredStudents = [...this.students];
      } catch (error) {
        console.error("Ошибка загрузки студентов:", error);
        this.students = [];
        this.filteredStudents = [];
      }
    },
    getInitials(name) {
      if (!name) return "";
      const parts = name.split(" ");
      if (parts.length >= 2) {
        return `${parts[0].charAt(0)}${parts[1].charAt(0)}`;
      }
      return name.substring(0, 2);
    },
    updateBackgroundPosition(event) {
      const x = (event.clientX / window.innerWidth - 0.5) * 50;
      const y = (event.clientY / window.innerHeight - 0.5) * 50;
      this.targetPosition = { x, y };
    },
    lerpBackgroundPosition() {
      this.bgPosition.x +=
        (this.targetPosition.x - this.bgPosition.x) * this.lerpFactor;
      this.bgPosition.y +=
        (this.targetPosition.y - this.bgPosition.y) * this.lerpFactor;
      requestAnimationFrame(() => this.lerpBackgroundPosition());
    },

    // Методы для фильтрации
    toggleInstituteDropdown() {
      this.showInstituteDropdown = !this.showInstituteDropdown;
      this.showGroupDropdown = false;
      this.showSortDropdown = false;
    },
    toggleGroupDropdown() {
      if (this.selectedInstituteFilter) {
        this.showGroupDropdown = !this.showGroupDropdown;
      }
      this.showInstituteDropdown = false;
      this.showSortDropdown = false;
    },
    toggleSortDropdown() {
      this.showSortDropdown = !this.showSortDropdown;
      this.showInstituteDropdown = false;
      this.showGroupDropdown = false;
    },
    selectInstitute(institute) {
      this.selectedInstituteFilter = institute;
      this.selectedGroupFilter = null;
      this.showInstituteDropdown = false;
      this.applyFilters();
    },
    selectGroup(group) {
      this.selectedGroupFilter = group;
      this.showGroupDropdown = false;
      this.applyFilters();
    },
    selectSort(sortOption) {
      this.currentSort = sortOption;
      this.showSortDropdown = false;
      this.applyFilters();
    },
    resetFilters() {
      this.selectedInstituteFilter = null;
      this.selectedGroupFilter = null;
      this.currentSort = "name_asc";
      this.applyFilters();
    },
    applyFilters() {
      let result = [...this.students];

      // Фильтрация по институту
      if (this.selectedInstituteFilter) {
        result = result.filter(
          (student) => student.faculty === this.selectedInstituteFilter
        );
      }

      // Фильтрация по группе
      if (this.selectedGroupFilter) {
        result = result.filter(
          (student) => student.group === this.selectedGroupFilter
        );
      }

      // Сортировка
      switch (this.currentSort) {
        case "name_asc":
          result.sort((a, b) => a.name.localeCompare(b.name));
          break;
        case "name_desc":
          result.sort((a, b) => b.name.localeCompare(a.name));
          break;
        case "team_asc":
          result.sort((a, b) => {
            const teamA = a.team || "ЯЯЯЯЯ";
            const teamB = b.team || "ЯЯЯЯЯ";
            return teamA.localeCompare(teamB);
          });
          break;
        case "team_desc":
          result.sort((a, b) => {
            const teamA = a.team || "ААААА";
            const teamB = b.team || "ААААА";
            return teamB.localeCompare(teamA);
          });
          break;
      }

      this.filteredStudents = result;
    },
  },
  mounted() {
    this.fetchStudents();
    window.addEventListener("mousemove", this.updateBackgroundPosition);
    this.lerpBackgroundPosition();
    this.currentBgColorBtnReset = this.instituteStyle.buttonOffColor;
  },
  beforeDestroy() {
    window.removeEventListener("mousemove", this.updateBackgroundPosition);
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColorBtnReset = newStyle.buttonOffColor;
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
/* Стили для размытого фона */

/* Стили таблицы */
table {
  border-collapse: separate;
  border-spacing: 0;
}

th {
  background-color: rgba(255, 255, 255, 0.03);
}

th,
td {
  padding: 12px 15px;
  text-align: left;
}

tbody tr:nth-child(even) {
  background-color: rgba(0, 0, 0, 0.03);
}

.dark tbody tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.03);
}

tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.dark tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.text-dynamic {
  color: var(--text-color);
}

/* Стили для выпадающих списков */
ul {
  scrollbar-width: thin;
  scrollbar-color: #888 transparent;
}

ul::-webkit-scrollbar {
  width: 6px;
}

ul::-webkit-scrollbar-track {
  background: transparent;
}

ul::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 3px;
}

/* Новые стили из страницы проектов */
.divider {
  border: none;
  height: 1px;
  background-color: #5f5f5f;
  margin: 1rem 0;
  opacity: 0.8;
}

.border-zinc-400 {
  border-color: rgba(161, 161, 170, 0.5);
}
</style>
