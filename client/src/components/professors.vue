<template>
  <div>
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
            :disabled="isLoadingGroups"
            class="flex items-center px-4 py-2 rounded-md transition-all duration-500 border border-zinc-400 hover:shadow-md h-10 bg-card disabled:opacity-50"
          >
            {{ selectedGroupFilter || (isLoadingGroups ? "Загрузка..." : "Выберите группу") }}
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
          
          <div
            v-if="showGroupDropdown"
            class="absolute left-0 w-64 mt-1 bg-input text-dynamic rounded-lg shadow-lg z-50"
          >
            <!-- Поиск по группам -->
            <div class="p-3 border-b border-gray-200 dark:border-gray-600">
              <input
                v-model="groupSearchQuery"
                @input="filterGroups"
                placeholder="Поиск группы..."
                class="w-full px-3 py-2 bg-card border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <!-- Список групп -->
            <ul class="max-h-48 overflow-y-auto">
              <li
                v-for="group in safeFilteredGroups"
                :key="group.id"
                @click="selectGroup(group)"
                class="py-2 px-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors"
              >
                {{ group.name }}
              </li>
              <li v-if="safeFilteredGroups.length === 0" class="py-2 px-4 text-gray-500">
                Группы не найдены
              </li>
            </ul>
          </div>
        </div>

        <!-- Кнопка загрузки студентов -->
        <button
          @click="loadStudentsData"
          :disabled="!canLoadStudents || isLoading"
          :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
          class="px-6 py-2 disabled:bg-gray-400 disabled:cursor-not-allowed text-always-white rounded-md transition-colors h-10"
        >
          {{ isLoading ? 'Загрузка...' : 'Показать студентов' }}
        </button>

        <!-- Кнопка сброса фильтров -->
        <button
          v-if="selectedInstituteFilter || selectedGroupFilter"
          @click="resetFilters"
          class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-always-white rounded-md transition-colors h-10"
        >
          Сбросить
        </button>
      </div>

      <!-- Сообщение о необходимости выбора фильтров -->
      <div v-if="!canLoadStudents && !isLoading" class="text-center py-12">
        <div class="text-gray-500 dark:text-gray-400">
          <svg class="mx-auto h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <h3 class="text-lg font-medium mb-2">Выберите институт и группу</h3>
          <p>Для просмотра списка студентов необходимо выбрать институт и группу</p>
        </div>
      </div>

      <!-- Таблица студентов -->
      <div v-if="canLoadStudents">
        <div class="overflow-x-auto rounded-lg shadow-lg">
          <table class="min-w-full bg-card">
            <thead class="bg-input">
              <tr>
                <th class="py-3 px-6 text-left">Имя студента</th>
                <th class="py-3 px-6 text-left">Почта студента</th>
                <th class="py-3 px-6 text-left">Группа</th>
                <th class="py-3 px-6 text-left">Команда</th>
                <th class="py-3 px-6 text-left">Проекты/Идеи</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr
                v-for="student in safeFlatStudents"
                :key="`${student.id}-${student.team_id || 'no-team'}`"
                class="hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-300"
              >
                <td class="py-4 px-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden mr-4">
                      <img
                        v-if="student.avatar"
                        :src="student.avatar ? `http://127.0.0.1:8000/${student.avatar}` : null"
                        alt="Avatar"
                        class="object-cover w-full h-full"
                        
                      />
                      <div
                        v-else
                        class="w-full h-full flex items-center justify-center bg-input"
                      >
                        <span class="font-semibold">{{ getInitials(student.full_name) }}</span>
                      </div>
                    </div>
                    <div>
                      <div class="font-medium cursor-pointer hover:underline" @click="goToUserProfile(student.id)">{{ student.full_name }}</div>
                    </div>
                  </div>
                </td>
                <td class="py-4 px-6">{{ student.email }}</td>
                <td class="py-4 px-6">
                  <div class="bg-input px-3 py-1 rounded-full text-sm">
                    {{ student.group_name }}
                  </div>
                </td>
                <td class="py-4 px-6">
                  <div v-if="student.team_name" class="flex items-center text-sm">
                    <div class="bg-input px-3 py-1 rounded-full cursor-pointer hover:underline" @click="goToTeam(student.team_id)">
                      {{ student.team_name }}
                    </div>
                  </div>
                  <span v-else class="text-gray-500 dark:text-gray-400">Не состоит</span>
                </td>
                <td class="py-4 px-6">
                  <div v-if="student.projects_ideas && student.projects_ideas.length > 0" class="space-y-1">
                    <div
                      v-for="item in student.projects_ideas"
                      :key="`${item.type}-${item.id}`"
                      class="flex items-center"
                    >
                      <span 
                        class="px-2 py-1 rounded-full font-medium text-sm cursor-pointer hover:underline"
                        :class="item.type === 'project' 
                          ? 'bg-blue-100 ' 
                          : 'bg-green-100 '"
                          @click="goToProjectOrIdea(item.type, item.id)"
                      >
                        {{ item.type === 'project' ? '📋' : '💡' }} {{ item.title }}
                      </span>
                    </div>
                  </div>
                  <span v-else class="text-gray-500 dark:text-gray-400">Не работает</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Показываем сообщение если нет данных -->
        <div v-if="!isLoading && safeFlatStudents.length === 0" class="text-center py-8">
          <p class="text-gray-500 dark:text-gray-400">Студенты не найдены</p>
        </div>

        <!-- Индикатор загрузки -->
        <div v-if="isLoading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          <p class="mt-2 text-gray-500">Загрузка данных...</p>
        </div>

        <!-- Статистика -->
        <div class="mt-6 bg-card rounded-lg p-4">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div>
              <div class="text-2xl font-bold text-blue-600">{{ totalStudents }}</div>
              <div class="text-sm text-gray-500">Всего студентов</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-green-600">{{ studentsWithTeams }}</div>
              <div class="text-sm text-gray-500">В командах</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-purple-600">{{ totalTeams }}</div>
              <div class="text-sm text-gray-500">Команд</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-orange-600">{{ totalProjects }}</div>
              <div class="text-sm text-gray-500">Проектов/Идей</div>
            </div>
          </div>
        </div>
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
      // Фильтры
      institutes: ["ВШЦТ", "АРХИД", "ИПТИ", "СТРОИН"],
      selectedInstituteFilter: '',
      selectedGroupFilter: '',
      
      // Группы
      allGroups: [],
      filteredGroups: [],
      groupSearchQuery: '',
      
      // Состояние UI
      showInstituteDropdown: false,
      showGroupDropdown: false,
      isLoadingGroups: false,
      isLoading: false,
      
      // Данные студентов
      flatStudents: [],
      
      // ✅ ДОБАВЛЕНО: Отсутствующая переменная
      currentBgColorBtnReset: "#ccc"
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
    canLoadStudents() {
      return this.selectedInstituteFilter && this.selectedGroupFilter
    },
    
    // Маппинг названий институтов к кодам
    instituteCodeMap() {
      return {
        'ВШЦТ': 'HSDT',
        'АРХИД': 'ARHID', 
        'ИПТИ': 'IPTI',
        'СТРОИН': 'STROIN'
      }
    },
    
    selectedInstituteCode() {
      return this.instituteCodeMap[this.selectedInstituteFilter] || ''
    },
    // Статистические computed свойства
  totalStudents() {
    return this.safeFlatStudents.length
  },
  
  studentsWithTeams() {
    return this.safeFlatStudents.filter(s => s.team_name).length
  },
  
  totalTeams() {
    const uniqueTeams = new Set(
      this.safeFlatStudents
        .filter(s => s.team_name)
        .map(s => s.team_name)
    )
    return uniqueTeams.size
  },
  
  totalProjects() {
    return this.safeFlatStudents.reduce((total, student) => {
      const projectsCount = student.projects_ideas ? student.projects_ideas.length : 0
      return total + projectsCount
    }, 0)
  },
    // ✅ ДОБАВЛЕНО: Безопасные computed свойства
    safeAllGroups() {
      return Array.isArray(this.allGroups) ? this.allGroups : []
    },
    
    safeFilteredGroups() {
      return Array.isArray(this.filteredGroups) ? this.filteredGroups : []
    },
    
    safeFlatStudents() {
      return Array.isArray(this.flatStudents) ? this.flatStudents : []
    }
  },
  
  mounted() {
    // Закрытие dropdown при клике вне
    document.addEventListener('click', this.handleClickOutside)
  },
  
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  
  methods: {
    /**
   * Переход на профиль пользователя
   */
  goToUserProfile(userId) {
    try {
      const route = `/${this.selectedInstitute}/profile/${userId}`;
      console.log('Переход на профиль пользователя:', route);
      this.$router.push(route);
    } catch (error) {
      console.error('Ошибка навигации к профилю:', error);
    }
  },
  
  /**
   * Переход на страницу команды
   */
  goToTeam(teamId) {
    if (!teamId) {
      console.warn('ID команды не указан');
      return;
    }
    
    try {
      const route = `/${this.selectedInstitute}/team/${teamId}`;
      console.log('Переход на страницу команды:', route);
      this.$router.push(route);
    } catch (error) {
      console.error('Ошибка навигации к команде:', error);
    }
  },
  
  /**
   * Переход на страницу проекта или идеи
   */
  goToProjectOrIdea(type, itemId) {
    if (!itemId) {
      console.warn('ID проекта/идеи не указан');
      return;
    }
    
    try {
      let route;
      
      if (type === 'project') {
        route = `/${this.selectedInstitute}/project/${itemId}`;
      } else if (type === 'idea') {
        route = `/${this.selectedInstitute}/idea/${itemId}`;
      } else {
        console.warn('Неизвестный тип элемента:', type);
        return;
      }
      
      console.log(`Переход на страницу ${type}:`, route);
      this.$router.push(route);
    } catch (error) {
      console.error(`Ошибка навигации к ${type}:`, error);
    }
  },
    // === Управление институтами ===
    toggleInstituteDropdown() {
      this.showInstituteDropdown = !this.showInstituteDropdown
      this.showGroupDropdown = false
    },
    
    async selectInstitute(institute) {
      this.selectedInstituteFilter = institute
      this.selectedGroupFilter = '' // Сбрасываем выбор группы
      this.showInstituteDropdown = false
      this.flatStudents = [] // Очищаем данные студентов
      
      // Загружаем группы для выбранного института
      await this.loadGroupsForInstitute()
    },
    
    // === Управление группами ===
    async loadGroupsForInstitute() {
      if (!this.selectedInstituteCode) return
      
      this.isLoadingGroups = true
      try {
        const response = await api.get('/core/university-groups/')
        
        console.log('Все группы:', response.data)
        console.log('Выбранный институт код:', this.selectedInstituteCode)
        
        // ✅ ИСПРАВЛЕНО: Добавлена проверка на массив
        const groups = Array.isArray(response.data) ? response.data : []
        
        // Фильтруем группы по выбранному институту
        this.allGroups = groups.filter(group => {
          console.log(`Группа ${group.name}: ${group.institute} === ${this.selectedInstituteCode}?`, group.institute === this.selectedInstituteCode)
          return group.institute === this.selectedInstituteCode
        })
        
        console.log('Отфильтрованные группы:', this.allGroups)
        this.filteredGroups = [...this.allGroups]
        
      } catch (error) {
        console.error('Ошибка загрузки групп:', error)
        this.allGroups = []
        this.filteredGroups = []
      } finally {
        this.isLoadingGroups = false
      }
    },
    
    toggleGroupDropdown() {
      if (this.isLoadingGroups) return
      this.showGroupDropdown = !this.showGroupDropdown
      this.showInstituteDropdown = false
    },
    
    selectGroup(group) {
      this.selectedGroupFilter = group.name
      this.showGroupDropdown = false
      this.groupSearchQuery = ''
      this.filteredGroups = [...this.allGroups]
      this.flatStudents = [] // Очищаем данные студентов
    },
    
    // === Поиск по группам ===
    filterGroups() {
      const query = this.groupSearchQuery.toLowerCase()
      // ✅ ИСПРАВЛЕНО: Добавлена проверка массива
      this.filteredGroups = this.safeAllGroups.filter(group =>
        group.name && group.name.toLowerCase().includes(query)
      )
    },
    
    // === Загрузка данных студентов ===
    async loadStudentsData() {
      if (!this.canLoadStudents) {
        alert('Выберите институт и группу')
        return
      }
      
      this.isLoading = true
      
      try {
        const response = await api.get('/core/university-groups/students_table/')
        
        if (response.data && response.data.success) {
          const allStudents = this.convertToFlatStructure(response.data.institutes || [])
          
          // Фильтруем по коду института
          this.flatStudents = allStudents.filter(student => 
            student.institute_code === this.selectedInstituteCode &&
            student.group_name === this.selectedGroupFilter
          )
          
        } else {
          console.error('Ошибка загрузки данных:', response.data?.error)
          this.flatStudents = []
        }
      } catch (error) {
        console.error('Ошибка API:', error)
        this.flatStudents = []
      } finally {
        this.isLoading = false
      }
    },
    
    // ✅ ИСПРАВЛЕНО: Добавлены проверки на существование массивов
    convertToFlatStructure(institutes) {
  const flatStudents = []
  
  if (!Array.isArray(institutes)) {
    console.warn('institutes не является массивом:', institutes)
    return flatStudents
  }
  
  institutes.forEach(institute => {
    if (!institute || !Array.isArray(institute.groups)) {
      console.warn('institute.groups не является массивом:', institute)
      return
    }
    
    institute.groups.forEach(group => {
      if (!group || !Array.isArray(group.users)) {
        console.warn('group.users не является массивом:', group)
        return
      }
      
      group.users.forEach(user => {
        if (!user) return
        
        const userTeams = Array.isArray(user.teams) ? user.teams : []
        
        if (userTeams.length > 0) {
          userTeams.forEach(team => {
            flatStudents.push({
              id: user.id,
              full_name: user.full_name || '',
              email: user.email || '',
              institute_name: institute.institute_name || '',
              institute_code: institute.institute_code || '',
              avatar: user.avatar || null, 
              group_name: group.group_name || '',
              team_id: team.id,
              team_name: team.name || '',
              projects_ideas: Array.isArray(team.projects_or_ideas) ? team.projects_or_ideas : []
            })
          })
        } else {
          flatStudents.push({
            id: user.id,
            full_name: user.full_name || '',
            email: user.email || '',
            institute_name: institute.institute_name || '',
            institute_code: institute.institute_code || '',
            avatar: user.avatar || null,
            group_name: group.group_name || '',
            team_id: null,
            team_name: null,
            projects_ideas: []
          })
        }
      })
    })
  })
  
  console.log('🔍 Созданные студенты:', flatStudents)
  return flatStudents
},
    
    // === Сброс фильтров ===
    resetFilters() {
      this.selectedInstituteFilter = ''
      this.selectedGroupFilter = ''
      this.allGroups = []
      this.filteredGroups = []
      this.groupSearchQuery = ''
      this.flatStudents = []
      this.showInstituteDropdown = false
      this.showGroupDropdown = false
    },
    
    // === Обработка кликов вне dropdown ===
    handleClickOutside(event) {
      if (!this.$el || !this.$el.contains(event.target)) {
        this.showInstituteDropdown = false
        this.showGroupDropdown = false
      }
    },
    
    getInitials(fullName) {
      if (!fullName || typeof fullName !== 'string') return '??'
      
      const names = fullName.trim().split(' ')
      if (names.length >= 2) {
        return `${names[0][0]}${names[1][0]}`.toUpperCase()
      }
      return fullName.substring(0, 2).toUpperCase()
    }
  },
  
  watch: {
    instituteStyle: {
      handler(newStyle) {
        // ✅ ИСПРАВЛЕНО: Проверка на существование newStyle
        this.currentBgColorBtnReset = newStyle?.buttonOffColor || "#ccc";
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
