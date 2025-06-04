<template>
  <div class="relative min-h-screen overflow-hidden">
    <div class="min-h-screen flex flex-col relative z-10">
      <!-- Хедер -->
      <Header />

      <!-- Основной контейнер профиля -->
      <div class="flex w-4/5 mx-auto mt-10 gap-6">
        <!-- Левый блок (Информация о пользователе) -->
        <div
          class="w-1/4 bg-card p-6 rounded-2xl shadow-lg backdrop-blur-sm"
        >
          <div class="text-center">
            <img
            v-if="userData"
              class="w-32 h-32 rounded-full border-4 mx-auto cursor-pointer transition-colors"
              :src="userData.avatar ? `http://127.0.0.1:8000/${userData.avatar}` : null"
              alt="Аватар пользователя"
              @click="showAvatarModal = true"
            />
            <h1
  v-if="userData && userData.first_name && userData.last_name"
  class="text-2xl font-semibold mt-4"
>
  {{ userData.first_name }} {{ userData.last_name }}
</h1>
            <div class="mt-2">
              <span 
              :style="{ backgroundColor: currentBgColor }"
                    @mouseover="currentBgColor = instituteStyle.buttonOnColor"
                    @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
              class="px-3 py-1 text-always-white rounded-full text-sm">
                {{ userData.role || "Роль не указана" }}
              </span>
            </div>
          </div>

          <div class="mt-5 text-dynamic">
            <p class="text-sm flex justify-between">
              <strong>Почта:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-sm rounded-lg p-2.5 border border-zinc-600 font-medium"
            >
              {{ userData.email || "Не указано" }}
            </div>
            <p class="text-sm mt-2 flex justify-between">
              <strong>Группа:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-sm rounded-lg p-2.5 border border-zinc-600 font-medium"
            >
              {{ userData.university_group || "Не указано" }}
            </div>
          </div>

          <!-- Блок биографии -->
          <div class="mt-5">
            <p class="text-sm flex justify-between text-dynamic">
              <strong>Биография:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-dynamic text-sm rounded-lg p-2.5 border border-zinc-600 min-h-[100px] font-medium"
            >
              {{ userData.bio || "Пока ничего не рассказал о себе" }}
            </div>
          </div>
        </div>

        <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
        <div
          class="w-3/4 bg-card p-6 rounded-2xl shadow-lg backdrop-blur-sm"
        >
          <h2 class="text-2xl font-semibold mb-4">Информация о пользователе</h2>

          <div class="flex gap-10">
            <!-- Проекты -->
            <div class="w-1/2">
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">Проекты</h3>
              <div class="mt-2">
                <div
                  v-for="(project, index) in userProjects"
                  :key="index"
                  class="mb-4 p-4 bg-input rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ project.title }}</h4>
                    <span
                      :class="{
                        'bg-green-500': project.status === 'Завершен',
                        'bg-blue-500': project.status === 'В работе',
                        'bg-yellow-500': project.status === 'Заморожен',
                      }"
                      class="px-2 py-1 rounded-full text-xs"
                    >
                      {{ project.status }}
                    </span>
                  </div>
                  <p class="text-sm mt-1">
                    {{ project.description }}
                  </p>
                  <div class="mt-2 flex justify-between items-center">
                    <div>
                      <span class="text-sm">Оценка: </span>
                      <span class="font-bold"> {{project.averageRating ?? '—'  }} /5</span>
                    </div>
                    <div>
                      <span class="text-sm">Участие: с {{ formatDate(project.date) }} по {{ formatDate(project.endDate) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Команды -->
            <div class="w-1/2">
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">Команды</h3>
              <div class="mt-2">
                <div
                  v-for="(team, index) in userTeams"
                  :key="index"
                  class="mb-4 p-4 bg-input rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ team.name }}</h4>
                    <span class="text-sm text-gray-300"
                      >{{ team.members.length  }} участников</span
                    >
                  </div>
                  <div class="mt-2">
                    <p class="text-sm">
                    </p>
                    <p class="text-sm mt-1">
                      <span class="font-medium">Статус команды:</span>
                      <span class="ml-3"
                        :class="{
                          'text-green-400': team.teamStatus === 'Активна',
                          'text-red-400': team.teamStatus === 'Распущена',
                          'text-yellow-400': team.teamStatus === 'Заморожена',
                        }"
                      >
                        {{ team.status }}
                      </span>
                    </p>
                    <div class="mt-2 text-sm">
                      <p>
                        Участие: с {{ formatDate(team.joinDate) }} по {{ formatDate(team.leaveDate) }}
                      </p>
                    </div>
                    <button
                      class="mt-2 text-purple-300 hover:text-purple-200 text-sm flex items-center"
                    >
                      <span @click="viewTeam(team.id)">Подробнее о команде</span>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 ml-1"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Список навыков -->
<h3 class="mt-10 text-xl font-semibold border-b pb-2 mb-3">Навыки</h3>
    <div class="flex flex-wrap gap-2 mt-4">
      <span
  v-for="tech in userSkillsDetailed"
  :key="tech.id"
  class="px-3 py-1 bg-purple-600/50 rounded-full text-sm flex items-center"
>
  {{ tech.name }}
</span>
    </div>

    
        </div>
      </div>


      <!-- Модальное окно для увеличения аватара -->
      <div
        v-if="showAvatarModal"
        class="fixed inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-50"
        @click="showAvatarModal = false"
      >
        <div class="p-2 max-w-[90vw] max-h-[90vh]">
          <img
            :src="userData.avatar || randomAvatar"
            class="max-w-full max-h-full rounded-lg"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import Cookies from "js-cookie";
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth";

export default {
  inject: ["globalState"],
  components: { Header },
  props: ['userId'],
  data() {
    return {
    allTechnologies: [], // Все технологии
    groupedTechnologies: {}, // Группировка по типу
    userSkills: [], // ID скиллов пользователя
    userProjects: [],
    userTeams: [],
    currentBgColor: "",
    userData: null,
    showAvatarModal: false,
    avatars: Array.from({ length: 6 }, (_, i) => `/ava-${i + 1}.jpg`),
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
    userSkillsDetailed() {
    // userSkills содержит id скиллов (числа)
    // allTechnologies — полный список навыков с id и name
    return this.userSkills.map(skillId => {
      return this.allTechnologies.find(tech => tech.id === skillId) || { id: skillId, name: 'Неизвестный навык' };
    });
  },
  },
  methods: {
    async fetchTechnologies() {
      const res = await api.get('/core/technologies');
      const data = res.data;

      this.allTechnologies = data;
      this.groupedTechnologies = data.reduce((acc, tech) => {
        if (!acc[tech.type]) acc[tech.type] = [];
        acc[tech.type].push(tech);
        return acc;
      }, {});
    },
    async fetchUserProfile(userId) {
  try {
    const res = await api.get(`/users/${userId}/`);
    this.userData = res.data;
    this.userSkills = res.data.skills || [];
    await this.fetchUserActivity(userId); // <--- вызывай тут
  } catch (e) {
    console.error('Ошибка загрузки пользователя:', e);
  }
},

toggleSkillInModal(tech) {
    const index = this.selectedSkillsInModal.findIndex(t => t.id === tech.id);
    if (index === -1) {
      this.selectedSkillsInModal.push(tech);
    } else {
      this.selectedSkillsInModal.splice(index, 1);
    }
  },
    formatDate(dateStr) {
    if (!dateStr) return 'по настоящее время';
    const date = new Date(dateStr);
    return date.toLocaleString("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  },
async fetchUserActivity(userId) {
  const response = await api.get(`/users/user-activity/?user_id=${userId}`);
  const activityData = response.data;

  const projectIds = activityData
    .filter(item => item.type === 'project' && item.project_id)
    .map(item => ({
      id: item.project_id,
      started_at: item.started_at,
      ended_at: item.ended_at
    }));

  const teamIds = activityData
    .filter(item => item.type === 'team' && item.team_id)
    .map(item => ({
      id: item.team_id,
      started_at: item.started_at,
      ended_at: item.ended_at
    }));

  const projectRequests = projectIds.map(async item => {
    // Получаем данные проекта и участников
    const [projectRes, participantsRes] = await Promise.all([
      api.get(`/projects/${item.id}`),
      api.get(`/projects/${item.id}/participants-details/`)
    ]);

    const projectData = projectRes.data;
    const participants = participantsRes.data;

    // Находим этого пользователя среди участников
const userEntry = [
  ...(participants?.workers || []),
  ...(participants?.teams?.flatMap(team => team.members) || [])
].find(p => p?.user?.id === userId);
    return {
      ...projectData,
      date: item.started_at,
      endDate: item.ended_at,
      averageRating: userEntry?.rating ?? null // используем rating, если есть
    };
  });

  const teamRequests = teamIds.map(async item => {
    const res = await api.get(`/teams/${item.id}`);
    const data = await res.data;
    return {
      ...data,
      joinDate: item.started_at,
      leaveDate: item.ended_at
    };
  });

  const [projects, teams] = await Promise.all([
    Promise.all(projectRequests),
    Promise.all(teamRequests)
  ]);

  this.userProjects = projects;
  this.userTeams = teams;
},
    viewTeam(teamId) {
    this.$router.push(`/${this.selectedInstitute}/team/${teamId}`);
  },
    handleAvatarUpload(event) {
  const file = event.target.files[0];
  if (file) {
    this.userData.avatarFile = file; // сохраняем в отдельное поле
    // можно тут же локально обновить превью:
    this.userData.avatar = URL.createObjectURL(file);
  }
},
  },
  watch: {
  userId: {
    immediate: true,
    handler(newId) {
      if (newId) {
        this.fetchUserProfile(newId);
        // лишний: this.fetchUserActivity(newId);
      }
    },
  },
  instituteStyle: {
    handler(newStyle) {
      this.currentBgColor = newStyle.buttonOffColor;
    },
    immediate: true,
  },
},
async mounted() {
    await this.fetchTechnologies();
},
}
</script>

<style scoped>
.transform-gpu {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}
.filter {
  filter: blur(8px);
}
.fixed {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}
.bg-zinc-700\/80 {
  background-color: rgba(63, 63, 70, 0.8);
}
.bg-zinc-700\/90 {
  background-color: rgba(63, 63, 70, 0.9);
}
.bg-zinc-800\/50,
.bg-zinc-800\/90,
.bg-zinc-800\/95 {
  background-color: rgba(39, 39, 42, 0.9);
}
.hover\:bg-purple-500:hover {
  background-color: rgb(168, 85, 247);
}
.hover\:bg-red-500:hover {
  background-color: rgb(239, 68, 68);
}
.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Анимации */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
.relative:hover .text-purple-300 {
  color: rgb(192, 132, 252);
}
.rotate-180 {
  transform: rotate(180deg);
}

/* Стили для ошибки */
.text-red-400 {
  color: #f87171;
}

/* Стили для заблокированной кнопки */
.opacity-50 {
  opacity: 0.5;
}
.cursor-not-allowed {
  cursor: not-allowed;
}

/* Новые стили для карточек проектов и команд */
.bg-zinc-600 {
  background-color: rgba(82, 82, 91, 0.7);
}
.bg-green-500 {
  background-color: rgb(34, 197, 94);
}
.bg-blue-500 {
  background-color: rgb(59, 130, 246);
}
.bg-yellow-500 {
  background-color: rgb(234, 179, 8);
}
.text-green-400 {
  color: rgb(74, 222, 128);
}
.text-red-400 {
  color: rgb(248, 113, 113);
}
.text-yellow-400 {
  color: rgb(250, 204, 21);
}
.bg-purple-600\/50 {
  background-color: rgba(147, 51, 234, 0.5);
}

/* Стили для модального окна навыков */
.max-h-\[90vh\] {
  max-height: 90vh;
}
</style>
