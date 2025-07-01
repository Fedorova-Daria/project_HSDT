<template>
  <div v-if="show" >
        <!-- 1. Приглашение в команду -->
<div v-if="notification.notification_type === 'added_to_team'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Поздравляем! Вас пригласили в команду!</h2>
    <p class="text-gray-600 mb-4">Вас пригласили в команду: {{ team?.name }}</p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <img src="https://via.placeholder.com/80" class="w-20 h-20 rounded-full mx-auto mb-3">
      <h3 class="text-xl font-semibold mb-1">{{team.name}}</h3>
      <p class="text-sm text-gray-500 mb-3">Участников: {{ team.members.lenght }}</p>
      <div class="flex flex-wrap gap-2 mt-2">
  <span
    v-for="(skills_required, i) in project.skills_required"
    :key="i"
    class="px-3 py-1 bg-zinc-200 text-gray-600 text-sm rounded-full"
  >
    {{ skills_required.name }}
  </span>
</div>
      <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">Подробнее</button>
    </div>
    
    <div class="flex flex-col gap-3">
      <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Принять приглашение</button>
      <button class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg">Отклонить</button>
    </div>
  </div>
</div>

<!-- 2. Вам кинули заявку в команду -->
<div v-else-if="notification.notification_type === 'team_join_request_sent' && joinRequest && userData" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="relative bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <button
      @click="$emit('close')"
      class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-3xl font-bold mr-3 mt-3"
      aria-label="Закрыть"
    >
      ×
    </button>
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в команду</h2>
    <p class="text-gray-600 mb-4">В вашу команду хочет вступить:</p>

    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <img
        :src="userData.avatar ? `http://127.0.0.1:8000/${userData.avatar}` : 'https://via.placeholder.com/80'"
        class="w-20 h-20 rounded-full mx-auto mb-3"
      >
      <h3 class="text-xl font-semibold mb-3">{{ userData.full_name }}</h3>
      <div class="flex flex-wrap justify-center gap-2 mb-3">
        <span
          v-for="(skill, i) in userData.skills"
          :key="i"
          class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full"
        >
          {{ skill }}
        </span>
      </div>
      <button @click="viewProfile" class="text-blue-600 hover:text-blue-800 text-sm font-medium">Подробнее</button>
    </div>

    <div class="flex flex-col gap-3">
      <button @click="openAllJoinRequests" class="text-blue-600 hover:text-blue-800 text-sm font-medium mt-1">
        Рассмотреть все заявки
      </button>
    </div>
  </div>
</div>

<!-- 3. Заявка в проект (для заказчика) -->
<div v-else-if="notification.notification_type === 'project_join_request_sent'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="relative bg-card rounded-xl p-6 w-full max-w-md shadow-2xl">
    
    <div class="flex justify-between mb-3">
    <h2 class="text-2xl font-bold mb-2">Заявка в проект</h2>
    <button
            @click="close"
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
    <div class="space-y-4 mb-4">
      <div v-if="project" class="bg-input p-4 rounded-lg">
        <h4 class="font-semibold text-lg mb-2">{{ project.title }}</h4>
        <p class="text-sm mb-3 line-clamp-2">{{project.description}}</p>
        <div class="flex flex-wrap gap-2">
<div class="flex flex-wrap gap-2 mt-2">
  <span
    v-for="(skills_required, i) in project.skills_required"
    :key="i"
    class="px-3 py-1 bg-zinc-200 text-gray-600 text-sm rounded-full"
  >
    {{ skills_required.name }}
  </span>
</div>
        </div>
      </div>
      <p class="font-semibold mb-4">Над вашим проектом хочет работать:</p>
      <div class="bg-input p-4 rounded-lg text-center">
        <h4 v-if="team" class="font-semibold mb-6 text-xl">Команда: {{team?.name}}</h4>
        <div class="flex flex-wrap justify-center gap-2">
          <div class="flex flex-wrap gap-2 mt-2">
  <span
  v-for="(skill, i) in team?.skills || []"
  :key="i"
  class="px-3 py-1 bg-zinc-200 text-gray-600 text-sm rounded-full"
>
  {{ skill }}
</span>
</div>
        </div>
      </div>
    </div>
    
    <router-link
  :to="{ name: 'ProjectDetail', params: { id: project.id }}"
  class="text-sm text-blue-400 font-medium mt-1 flex justify-center"
>
  Рассмотреть все заявки
</router-link>
  </div>
</div>

<!-- 4. Принятие заявки в проект (для студента) -->
<div v-if="notification.notification_type === 'project_join_request_accepted'" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
  <div class="bg-card rounded-xl p-6 w-full max-w-md shadow-2xl">
    <div class="flex justify-between mb-3">
    <h2 class="text-2xl font-bold mb-2">Заявка в проект</h2>
    <button
            @click="close"
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
    <p class=" mb-4">Поздравляем! Вашу заявку принял проект <span class="font-semibold">{{project.title}}</span></p>
    
    <div class="bg-input p-4 rounded-lg mb-4">
      <h4 class="font-semibold text-dynamic text-lg mb-2">{{project.title}}</h4>
      <p class="text-dynamic opacity-70 text-sm mb-5 line-clamp-2">{{project.description}}</p>
      <div class="flex flex-wrap gap-2 mt-2">
  <span
    v-for="(skill, i) in project.skills_required"
    :key="i"
    class="px-3 py-1 bg-zinc-200 text-gray-600 text-sm rounded-full"
  >
    {{ skill.name }}
  </span>
</div>
    </div>
    <router-link
  :to="{ name: 'ProjectDetail', params: { id: project.id }}"
  class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white px-3 flex justify-center text-sl rounded-lg text-always-white"
>
    Перейти к проекту
    </router-link>
  </div>
</div>

<!-- 5. Принятие в команду -->
<div v-if="notification.type === 'team_join_request_accepted'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в команду</h2>
    <p class="text-gray-600 mb-4">Поздравляем! Вас приняли в команду <span class="font-semibold">{{ team.name }}</span></p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <h3 class="text-xl font-semibold mb-1">{{team.name}}</h3>
      <div class="flex flex-wrap gap-2 mt-2">
  <span
    v-for="(skill, i) in team.skills"
    :key="i"
    class="px-3 py-1 bg-zinc-200 text-gray-600 text-sm rounded-full"
  >
    {{ skill }}
  </span>
</div>
    </div>
    
    <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Перейти к команде</button>
  </div>
</div>
  </div>
</template>

<script>
import api from "@/composables/auth";

export default {
  inject: ["globalState"], 
  props: {
    show: Boolean,
    notification: Object
  },
  data() {
  return {
    joinRequest: null,
    userData: null,
    technologiesMap: {},
    project: null,
    team: null,
    isModalOpen: false,
  };
},
computed: {
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
},
  watch: {
    notification: {
      immediate: true,
      handler: async function (newVal) {
        if (!newVal || !newVal.related_project) return;

        try {
          const response = await api.get(`/projects/${newVal.related_project}/`);
          this.project = response.data;
        } catch (error) {
          console.error('Ошибка при получении проекта:', error);
        }

        if (newVal.related_team) {
          this.team = await this.fetchTeam(newVal.related_team);
        }
      }
    }
  },
  methods: {
    async fetchTechnologies() {
    const response = await api.get("/core/technologies");
    const map = {};
    response.data.forEach(tech => {
      map[tech.id] = tech.name;
    });
    this.technologiesMap = map;
  },

  async loadJoinRequestAndUser() {
  try {
    // Запрос на получение данных о запросе присоединения
    const requestRes = await api.get(`/team-join-requests/${this.notification.related_team_join_request}/`);
    
    // Проверка статуса ответа
    if (requestRes.status !== 200 || !requestRes.data) {
      throw new Error(`Ошибка: Неверный ответ от API для запроса команды. Статус: ${requestRes.status}`);
    }
    
    this.joinRequest = requestRes.data;
    
    // Проверка, что user ID существует
    if (!this.joinRequest.user) {
      throw new Error('Ошибка: user ID отсутствует в ответе на запрос команды');
    }

    // Запрос на получение данных о пользователе
    const userRes = await api.get(`/users/${this.joinRequest.user}/`);
    
    // Проверка статуса ответа
    if (userRes.status !== 200 || !userRes.data) {
      throw new Error(`Ошибка: Неверный ответ от API для запроса пользователя. Статус: ${userRes.status}`);
    }

    // Обработка навыков пользователя
    const skillNames = (userRes.data.skills || []).map(id => this.technologiesMap[id] || "Неизвестно");

    // Сохранение данных пользователя
    this.userData = {
      full_name: `${userRes.data.first_name} ${userRes.data.last_name}`,
      avatar: userRes.data.avatar,
      skills: skillNames,
      id: userRes.data.id,
    };
  } catch (error) {
    console.error("Ошибка при загрузке данных:", error);
  }
},
async loadJoinRequestProject() {
    try {
      const requestRes = await api.get(`/project-applications/${this.notification.related_project_application}/`);
      this.joinRequest = requestRes.data;

      const userRes = await api.get(`/users/${this.joinRequest.freelancer}/`);
      console.log(userRes)
      const skillNames = (userRes.data.skills || []).map(id => this.technologiesMap[id] || "Неизвестно");

      this.userData = {
        full_name: `${userRes.data.first_name} ${userRes.data.last_name}`,
        avatar: userRes.data.avatar,
        skills: skillNames,
        id: userRes.data.id,
      };
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  },
  viewProfile() {
    this.$router.push(`/${this.selectedInstitute}/profile/${this.userData.id}`);
  },
  openAllJoinRequests() {
    this.$router.push(`/${this.selectedInstitute}/team/${this.joinRequest.team}`);
  },
    close() {
      this.$emit('close');  // отправляем событие закрытия родителю
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleString("ru-RU", {
        day: "numeric",
        month: "long",
        hour: "2-digit",
        minute: "2-digit"
      });
    },
    async fetchTeam(id) {
      try {
        const response = await api.get(`/teams/${id}/`);
        const team = response.data;
        return team;
      } catch (error) {
        console.error('Ошибка при загрузке команды:', error);
        return null;
      }
    },
  },
  async mounted() {
  if (this.notification.notification_type === "team_join_request_sent") {
    await this.fetchTechnologies();
    await this.loadJoinRequestAndUser();
    await this.loadJoinRequestProject();
    console.log("notification.notification_type:", this.notification.notification_type);
console.log("joinRequest:", this.joinRequest);
console.log("userData:", this.userData);
  }
},
};
</script>

<style scoped>
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
</style>