<template>
  <div>
    <!-- Размытый фон, который следует за курсором -->
    <!-- <div class="blurred-bg" :style="bgStyle"></div> -->

    <Header />
    <div class="p-6 w-4/5 mx-auto relative">
      <!-- Кнопка "Создать команду" -->
      <button
        class=" button mt-4 px-6 py-2 rounded-md transition-all text-always-white transform hover:button:hover"
        @click="openCreateModal"
      >
      Создать команду
      </button>
      <!-- Фильтры с анимацией -->
<div class="flex justify-center space-x-6 relative mt-3">
  <button
    v-for="(filter, index) in filters"
    :key="index"
    @click="setFilter(filter.value)"
    class="relative pb-1 text-lg font-medium transition-colors duration-300"
    :class="{
      'text-white': activeFilter === filter.value,
      'text-zinc-200 opacity-70 hover:text-white': activeFilter !== filter.value,
    }"
  >
    {{ filter.label }}
    <!-- Анимированная полоска -->
    <span
      class="absolute bottom-0 h-0.5 transition-all duration-300 rounded-lg"
      :style="{
        backgroundColor: currentBgColor,
        left: activeFilter === filter.value ? '0' : '50%',
        width: activeFilter === filter.value ? '100%' : '0',
        transform: activeFilter === filter.value ? 'translateX(0)' : 'translateX(-50%)'
      }"
    >
    </span>
  </button>
</div>

    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      <span class="ml-2">Загрузка команд...</span>
    </div>

    <!-- Таблица команд -->
    <div v-else>
      <!-- Таблица команд --> 
      <TeamTable :teams="teams"  :globalState="globalState"/>
    </div>
      <!-- Компонент для создания команды -->
      <TeamCreate
  :isCreateModalOpen="isCreateModalOpen"
  @close="closeCreateModal"
  @create-team="createTeam"
/>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import TeamCreate from "@/components/teams/TeamCreate.vue";
import TeamTable from "@/components/teams/TeamsTable.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth"; // Настроенный axios-инстанс
import UserService from "@/composables/storage.js"; // Экземпляр для работы с токенами и данными

export default {
  name: "Teams",
  inject: ["globalState"], // Глобальное состояние (например, выбранный институт)
  components: {
    Header,
    TeamCreate,
    TeamTable,
  },
  data() {
    return {
      userRole: null, // Роль текущего пользователя
      currentUserId: null,
      currentBgColor: "",
      isLoading: false,
      activeFilter: 'all',
      teams: [],
      isCreateModalOpen: false,
      bgPosition: { x: 0, y: 0 },
      targetPosition: { x: 0, y: 0 },
      lerpFactor: 0.1, // Коэффициент плавности анимации
      filters: [
        { label: 'Все', value: 'all' },
        { label: 'Мои', value: 'owned' },
        { label: 'Участвую', value: 'member' }
      ]
    };
  },
  computed: {
    /**
     * Глобально выбранный институт из глобального состояния
     */
    selectedInstitute() {
      return this.globalState.institute;
    },
    /**
     * Выбирает стиль института из предопределённого набора стилей.
     * Если стиль не найден, возвращается дефолтный объект.
     */
    instituteStyle() {
      return instituteStyles[this.selectedInstitute] || { buttonOffColor: "#ccc" };
    },
    /**
     * Возвращает команды, отсортированные по флагу isFavorite.
     * Сортировка идёт в порядке убывания (сначала избранные).
     */
    sortedTeams() {
      if (!Array.isArray(this.teams)) return [];
      return [...this.teams].sort(
        (a, b) => Number(b.isFavorite) - Number(a.isFavorite)
      );
    },
    /**
     * Динамически вычисляемый стиль для фонового изображения.
     */
    bgStyle() {
      return {
        backgroundImage: "url('/bob.svg')",
        backgroundPosition: `${this.bgPosition.x}px ${this.bgPosition.y}px`,
      };
    },
  },
  methods: {
    // Инициализация данных пользователя
    initializeUser() {
      const userDataStr = localStorage.getItem('userData');
      if (userDataStr) {
        try {
          const userData = JSON.parse(userDataStr);
          this.currentUserId = userData.id;
        } catch (e) {
          console.error('Ошибка парсинга userData из localStorage', e);
        }
      }
    },

    // Установка активного фильтра
    async setFilter(filterValue) {
      this.activeFilter = filterValue;
      await this.fetchTeams();
    },

    // Загрузка команд с учетом фильтра
    async fetchTeams() {
      if (!this.currentUserId) {
        console.error('ID пользователя не найден');
        return;
      }

      this.isLoading = true;
      
      try {
        let url = '/teams/';
        const params = new URLSearchParams();
        
        // Исключаем команды со статусом "over" для всех фильтров
        params.append('status', 'open,private,in_progress');
        
        // Применяем фильтры в зависимости от выбранного типа
        switch (this.activeFilter) {
          case 'owned':
            // Команды, где пользователь является владельцем
            params.append('owner', this.currentUserId);
            break;
            
          case 'member':
            // Команды, где пользователь является участником
            params.append('members_ids', this.currentUserId);
            break;
            
          case 'all':
          default:
            // Все команды (без дополнительных фильтров, кроме статуса)
            break;
        }
        
        // Добавляем параметры к URL
        if (params.toString()) {
          url += '?' + params.toString();
        }
        
        console.log('Запрос команд с URL:', url);
        
        const response = await api.get(url);
        this.teams = response.data;
        
        console.log(`Команды успешно загружены (${this.activeFilter}):`, response.data);
        
      } catch (error) {
        console.error('Ошибка загрузки команд:', error);
        this.teams = [];
      } finally {
        this.isLoading = false;
      }
    },

    // Получение количества команд для каждого фильтра (опционально)
    async getFilterCounts() {
      try {
        const [allResponse, ownedResponse, memberResponse] = await Promise.all([
          api.get('/teams/?status=open,private,in_progress'),
          api.get(`/teams/?owner=${this.currentUserId}&status=open,private,in_progress`),
          api.get(`/teams/?members_ids=${this.currentUserId}&status=open,private,in_progress`)
        ]);

        // Обновляем фильтры с количеством
        this.filters = [
          { label: `Все (${allResponse.data.length})`, value: 'all' },
          { label: `Мои (${ownedResponse.data.length})`, value: 'owned' },
          { label: `Участвую (${memberResponse.data.length})`, value: 'member' }
        ];
        
      } catch (error) {
        console.error('Ошибка получения количества команд:', error);
      }
    },
    async fetchTeams() {
  this.isLoading = true;
  
  try {
    let url;
    
    switch (this.activeFilter) {
      case 'owned':
        url = `/teams/?owner=${this.currentUserId}`;
        break;
      case 'member':
        url = `/teams/?members_ids=${this.currentUserId}`;
        break;
      case 'all':
      default:
        url = `/teams/?status=open,private,in_progress`;
        break;
    }
    
    const response = await api.get(url);
    this.teams = response.data;
    
  } catch (error) {
    console.error('Ошибка загрузки команд:', error);
    this.teams = [];
  } finally {
    this.isLoading = false;
  }
},
    /**
     * Проверяет, что имя команды является уникальным.
     * @param {string} name - Имя команды, которое нужно проверить.
     * @returns {boolean}
     */
    isTeamNameUnique(name) {
      return !this.teams.some((team) => team.name === name);
    },
    /**
     * Открывает модальное окно создания команды.
     */
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    /**
     * Закрывает модальное окно создания команды.
     */
    closeCreateModal() {
      this.isCreateModalOpen = false;
    },
    /**
     * Создаёт новую команду. Если количество участников < 1 или имя не уникально,
     * операция отклоняется.
     * @param {Object} newTeam - Объект с данными новой команды.
     */
    createTeam(newTeam) {
      if (newTeam.members < 1) {
        return;
      }
      if (!this.isTeamNameUnique(newTeam.name)) {
        alert("Команда с таким именем уже существует!");
        return;
      }
      this.teams.push({ ...newTeam, isFavorite: false });
      this.closeCreateModal();
    },
    /**
     * Помечает команду для удаления, устанавливая статус "Проверяем".
     * @param {Object} team - Команда, которую нужно пометить.
     */
    markTeamForDeletion(team) {
      team.status = "Проверяем";
      team.markedForDeletion = true;
    },
    /**
     * Переключает состояние избранного для команды.
     * @param {Object} team - Команда, для которой меняется состояние.
     */
    toggleFavorite(team) {
      team.isFavorite = !team.isFavorite;
    },
    /**
     * Обновляет целевую позицию фона в ответ на движение мыши.
     * @param {MouseEvent} event
     */
    updateBackgroundPosition(event) {
      const x = (event.clientX / window.innerWidth - 0.5) * 50;
      const y = (event.clientY / window.innerHeight - 0.5) * 50;
      this.targetPosition = { x, y };
    },
    /**
     * Плавно интерполирует позицию фона к целевой позиции.
     */
    lerpBackgroundPosition() {
      this.bgPosition.x += (this.targetPosition.x - this.bgPosition.x) * this.lerpFactor;
      this.bgPosition.y += (this.targetPosition.y - this.bgPosition.y) * this.lerpFactor;
      requestAnimationFrame(() => this.lerpBackgroundPosition());
    },
  },
  async mounted() {
    window.addEventListener("mousemove", this.updateBackgroundPosition);
    this.lerpBackgroundPosition();
    this.initializeUser();
    await this.fetchTeams();
  },
  beforeDestroy() {
    window.removeEventListener("mousemove", this.updateBackgroundPosition);
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
    selectedInstitute(newValue) {
      console.log("Глобальное состояние института обновлено:", newValue);
    },
  },
  created() {
    // Получаем роль пользователя через UserService
    this.userRole = UserService.getUserRole();
  },
};
</script>

<style scoped>

/* Стили для размытого фона */
.blurred-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-repeat: no-repeat;
  filter: blur(10px); /* Размытие фона */
  z-index: -1; /* Фон будет под основным содержимым */
  pointer-events: none; /* Фон не блокирует взаимодействие */
}

/* Затемняющий слой */
.blurred-bg::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(
    0,
    0,
    0,
    0.5
  ); /* Затемнение (0.5 = 50% прозрачности) */
  z-index: 1;
}
.relative.z-10 {
  position: relative;
  z-index: 10;
}
/* Остальные стили */
.bg-cards {
  background-color: #292929;
}

.bg-cards:hover {
  background-color: #222222;
}

.bg-zinc-800 {
  background-color: #1f2937;
}

.border-zinc-600 {
  border-color: #4b5563;
}

.bg-marked-for-deletion {
  background-color: #483d8b;
}

.bg-favorite {
  background-color: #2c3e50;
}

.btn {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:active {
  transform: scale(0.95);
}
.button {
  transition: background-color 0.3s, transform 0.2s;
  background-color: v-bind("instituteStyle.buttonOffColor");
}
.button:hover {
  background-color: v-bind("instituteStyle.buttonOnColor");
  transform: scale(1.05);
}
</style>
