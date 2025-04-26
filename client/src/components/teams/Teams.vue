<template>
  <div>
    <!-- Размытый фон, который следует за курсором -->
    <div class="blurred-bg" :style="bgStyle"></div>

    <Header />
    <div class="p-6 w-4/5 mx-auto relative z-10">
      <!-- Кнопка "Создать команду" -->
      <button
        class=" button mt-4 px-6 py-2 rounded-md transition-all transform hover:button:hover text-white"
        @click="openCreateModal"
        v-if="userRole === 'ST'"
      >
      Создать команду
      </button>
      <!-- Таблица команд --> 
      <TeamTable :teams="teams" :availableTechStack="availableTechStack"  :globalState="globalState"/>
      <!-- Компонент для создания команды -->
      <TeamCreate
  :isCreateModalOpen="isCreateModalOpen"
  :availableTechStack="availableTechStack"
  @close-create-modal="closeCreateModal"
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
      availableTechStack: {
        "Программирование": ["Python", "Vue", "Django", "Node.js", "React"],
        "Дизайн": ["3D-моделирование", "Figma", "Photoshop"],
        "Маркетинг": ["SEO", "SMM", "Контент-маркетинг"],
      },
      currentBgColor: "",
      teams: [],
      isCreateModalOpen: false,
      bgPosition: { x: 0, y: 0 },
      targetPosition: { x: 0, y: 0 },
      lerpFactor: 0.1, // Коэффициент плавности анимации
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
    /**
     * Загружает список команд с использованием настроенного axios-инстанса.
     */
      async fetchTeams() {
      try {
        // При выполнении запроса через "api" интерсептор гарантирует, что передается корректный token.
        const response = await api.get("/teams/");
        this.teams = response.data;
        console.log("Команды успешно загружены:", response.data);
      } catch (error) {
        console.error("Ошибка загрузки команд:", error);
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
  mounted() {
    window.addEventListener("mousemove", this.updateBackgroundPosition);
    this.lerpBackgroundPosition();
    this.fetchTeams();
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
