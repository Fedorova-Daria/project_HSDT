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
import { instituteStyles } from "@/assets/instituteStyles.js";
import TeamTable from "@/components/teams/TeamsTable.vue";
import api from '@/api/axiosInstance.js'; // Путь к вашему axios instance
export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  components: {
    Header,
    TeamCreate,
    TeamTable
  },
  data() {
    return {
      availableTechStack: {
        "Программирование": ["Python", "Vue", "Django", "Node.js", "React"],
        "Дизайн": ["3D-моделирование", "Figma", "Photoshop"],
        "Маркетинг": ["SEO", "SMM", "Контент-маркетинг"]
      },
      currentBgColor: "", // Исходный цвет
      isFavorite: false,
      teams: [],
      isCreateModalOpen: false,
      bgPosition: { x: 0, y: 0 }, // Позиция фона
      targetPosition: { x: 0, y: 0 }, // Целевая позиция фона
      lerpFactor: 0.1, // Коэффициент интерполяции (0.1 = плавное движение)
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute]; // Используем глобальное состояние
      return style ? style : { buttonOffColor: "#ccc" };
    },
    sortedTeams() {
    return Array.isArray(this.teams) ? [...this.teams].sort((a, b) => b.isFavorite - a.isFavorite) : [];
    },
    // Стили для фона
    bgStyle() {
      return {
        backgroundImage: "url('/bob.svg')",
        backgroundPosition: `${this.bgPosition.x}px ${this.bgPosition.y}px`,
      };
    },
  },
  methods: {
    async fetchTeams() {
  try {
    const response = await api.get('teams/'); // Используем api для запроса
    this.teams = response.data; // Обрабатываем полученные данные
  } catch (error) {
    console.error("Ошибка загрузки команд:", error);
  }
},
    isTeamNameUnique(name) {
      return !this.teams.some((team) => team.name === name);
    },
    
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
    },
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
    markTeamForDeletion(team) {
      team.status = "Проверяем";
      team.markedForDeletion = true;
    },
    toggleFavorite(team) {
      team.isFavorite = !team.isFavorite;
    },
    // Обновление позиции фона
    updateBackgroundPosition(event) {
      const x = (event.clientX / window.innerWidth - 0.5) * 50; // Смещение по X
      const y = (event.clientY / window.innerHeight - 0.5) * 50; // Смещение по Y
      this.targetPosition = { x, y };
    },
    // Интерполяция позиции фона
    lerpBackgroundPosition() {
      this.bgPosition.x +=
        (this.targetPosition.x - this.bgPosition.x) * this.lerpFactor;
      this.bgPosition.y +=
        (this.targetPosition.y - this.bgPosition.y) * this.lerpFactor;
      requestAnimationFrame(this.lerpBackgroundPosition);
    },
  },
  mounted() {
    window.addEventListener("mousemove", this.updateBackgroundPosition); // Следим за движением курсора
    this.lerpBackgroundPosition(); // Запускаем интерполяцию
    this.fetchTeams();
    
  },
  beforeDestroy() {
    window.removeEventListener("mousemove", this.updateBackgroundPosition); // Удаляем обработчик
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true, // Устанавливаем цвет сразу при загрузке
    },
    selectedInstitute(newValue) {
      console.log("Глобальное состояние института обновлено:", newValue);
    },
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
