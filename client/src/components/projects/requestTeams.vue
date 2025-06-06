<template>
  <div
    class="modal-wrapper fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50"
  >
    <div
      class="modal-content bg-card p-6 rounded-lg shadow-lg w-3/5 max-h-[90vh] overflow-y-auto"
    >
      <h2 class="text-2xl font-bold mb-4 text-dynamic">Заявки на проект</h2>

      <!-- 📌 Таблица с заявками от команд -->
      <h3 class="text-xl font-semibold mt-4 text-dynamic mb-3">Команды</h3>
      <table class="w-full border-dynamic text-center rounded-lg shadow-lg overflow-hidden">
        <thead>
          <tr class="bg-input">
            <th class="border-dynamic p-2">Название команды</th>
            <th class="border-dynamic p-2">Количество участников</th>
            <th class="border-dynamic p-2">Навыки</th>
            <th class="border-dynamic p-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="team in teamApplications"
            :key="team.id"
            class="hover:bg-hover"
          >
            <td class="border-dynamic p-2">{{ team.name }}</td>
            <td class="border-dynamic p-2">
              {{ team.members.length }}
            </td>
            <td class="border-dynamic p-2">
              {{ team.skills.join(", ") }}
            </td>
            <td class=" p-2 flex justify-center space-x-2">
              <button
                @click="viewTeam(team.id)"
                class="bg-blue-500 text-always-white px-3 py-1 rounded hover:bg-blue-600 transition-colors"
              >
                Просмотр
              </button>
              <button
                @click="acceptApplication(team.applicationId, team)"
                class="bg-green-500 text-always-white px-3 py-1 rounded hover:bg-green-600 transition-colors"
              >
                Принять
              </button>
              <button
                @click="cancelApplication(team.applicationId)"
                class="bg-red-500 text-always-white px-3 py-1 rounded hover:bg-red-600 transition-colors"
              >
                Отменить
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 📌 Таблица с заявками от фрилансеров -->
      <h3 class="text-xl font-semibold mt-6 text-dynamic mb-3">Фрилансеры</h3>
      <table class="w-full border-dynamic text-center rounded-lg shadow-lg overflow-hidden">
        <thead>
          <tr class="bg-input">
            <th class="border-dynamic p-2"></th>
            <th class="border-dynamic p-2">Навыки</th>
            <th class="border-dynamic p-2">Дата подачи заявки</th>
            <th class="border-dynamic p-2">Профиль</th>
            <th class="border-dynamic p-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="freelancer in freelancerApplications"
            :key="freelancer.id"
            class="hover:bg-hover"
          >
            <td class="border-dynamic p-2">
              {{ freelancer.user_full_name || "Не указано" }}
            </td>
            <td class="border-dynamic p-2">
              {{ freelancer.skills?.join(", ") || "Не указаны" }}
            </td>
            <td class="border-dynamic p-2">
              {{ new Date(freelancer.created_at).toLocaleString() }}
            </td>
            <td class="border-dynamic p-2">
              <button
                @click="viewProfile(freelancer.freelancer)"
                class="bg-blue-500 text-always-white px-3 py-1 rounded hover:bg-blue-600 transition-colors"
              >
                Просмотр
              </button>
            </td>
            <td class="border-dynamic p-2 flex justify-center space-x-2">
              <button
                @click="acceptApplication(freelancer.id, freelancer)"
                class="bg-green-500 text-always-white px-3 py-1 rounded hover:bg-green-600 transition-colors"
              >
                Принять
              </button>
              <button
                @click="cancelApplication(freelancer.id, freelancer)"
                class="bg-red-500 text-always-white px-3 py-1 rounded hover:bg-red-600 transition-colors"
              >
                Отменить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
<button @click="toggleApplicationState">{{ isApplicationsClosed ? 'Возобновить прием заявок' : 'Закрыть прием заявок' }}</button>
      <!-- Кнопка закрытия -->
      <button
        class="mt-4 bg-gray-500 text-always-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
        @click="$emit('close')"
      >
        Закрыть
      </button>
    </div>

  </div>
</template>

<script>
import {
  getProjectApplications,
  acceptProjectApplication,
  cancelProjectApplication,
} from "@/services/projectRequests";
import api from "@/composables/auth.js";

export default {
  inject: ["globalState"],
  name: "ProjectApplications",
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isApplicationsClosed: false,
      technologiesMap: {},
      teamApplications: [],
      freelancerApplications: [],
    };
  },
  methods: {
    toggleApplicationState() {
      // Переключаем состояние
      this.isApplicationsClosed = !this.isApplicationsClosed;

      // Дополнительно можно добавить логику для того, чтобы обработать реальное изменение
      if (this.isApplicationsClosed) {
        this.closeApplications();  // Если закрыть, выполняем этот метод
      } else {
        this.reopenApplications(); // Если возобновить, выполняем этот метод
      }
    },
    closeApplications() {
    this.isApplicationsClosed = true;
    this.$emit('close-application-acceptance');
  },
  reopenApplications() {
    this.isApplicationsClosed = false; 
  },
    viewProfile(userId) {
      this.$router.push(`/${this.selectedInstitute}/profile/${userId}`);
    },
    viewTeam(teamId) {
      this.$router.push(`/${this.selectedInstitute}/team/${teamId}`);
    },
    async fetchTechnologies() {
      try {
        const response = await api.get('/core/technologies');
        this.technologiesMap = response.data.reduce((map, tech) => {
          map[tech.id] = tech.name;
          return map;
        }, {});
      } catch (error) {
        console.error("Ошибка при загрузке технологий:", error);
      }
    },
    async fetchProjectApplications() {
      try {
        const applications = await getProjectApplications();
        const filteredApplications = applications.filter(
          (app) => app.project === Number(this.projectId) && app.status === "pending"
        );

        const [teamResponses, freelancerResponses] = await Promise.all([
          this.fetchTeamApplications(filteredApplications),
          this.fetchFreelancerApplications(filteredApplications),
        ]);

        this.teamApplications = teamResponses;
        this.freelancerApplications = freelancerResponses;
      } catch (error) {
        console.error("Ошибка при получении заявок:", error);
      }
    },
    async fetchTeamApplications(filteredApplications) {
      const teamPromises = filteredApplications
        .filter((app) => app.team)
        .map((app) => this.fetchTeamDetails(app.team, app.id));
      return await Promise.all(teamPromises);
    },
    async fetchFreelancerApplications(filteredApplications) {
      const freelancerPromises = filteredApplications
        .filter((app) => app.freelancer)
        .map(async (app) => {
          const userInfo = await this.fetchUserDetails(app.freelancer);
          return { ...app, ...userInfo };
        });
      return await Promise.all(freelancerPromises);
    },
    async fetchTeamDetails(teamId, applicationId) {
      try {
        const response = await api.get(`/teams/${teamId}/`);
        return { ...response.data, applicationId };
      } catch (error) {
        console.error(`Ошибка при получении информации о команде с ID ${teamId}:`, error);
        return null;
      }
    },
    async fetchUserDetails(userId) {
      try {
        const response = await api.get(`/users/${userId}/`);
        const skillsIds = response.data.skills || [];
        const skillNames = skillsIds.map(id => this.technologiesMap[id] || "Неизвестно");

        return {
          user_full_name: `${response.data.first_name} ${response.data.last_name}`,
          skills: skillNames,
        };
      } catch (error) {
        console.error(`Ошибка при получении информации о пользователе с ID ${userId}:`, error);
        return { user_full_name: "Неизвестно", skills: [] };
      }
    },
    async acceptApplication(id, applicationData) {
      try {
        const acceptData = this.getApplicationData(applicationData);
        await acceptProjectApplication(id, acceptData);
        alert("Заявка принята!");

        const data = await this.fetchApplicationData(id);
        if (data.team && data.project) {
          await this.createKanbanBoard(data);
        }
        this.fetchProjectApplications();
      } catch (error) {
        alert("Ошибка при принятии заявки или создании доски.");
        console.error(error);
      }
    },
    getApplicationData(applicationData) {
      return {
        applicant_type: applicationData.applicant_type || null,
        project: applicationData.project || null,
        freelancer: applicationData.freelancer || null,
        team: applicationData.team || null,
      };
    },
    async fetchApplicationData(id) {
      const response = await api.get(`/project-applications/${id}/`);
      return response.data;
    },
    async createKanbanBoard(data) {
      await api.post('/kanban/boards/', {
        team: data.team,
        project: data.project,
      });
      alert("Канбан-доска создана!");
    },
    async cancelApplication(id, applicationData) {
      try {
        const cancelData = this.getApplicationData(applicationData);
        await cancelProjectApplication(id, cancelData);
        alert("Заявка отменена!");
        this.fetchProjectApplications();
      } catch (error) {
        alert("Ошибка при отмене заявки.");
        console.error(error);
      }
    },
  },
  mounted() {
    this.fetchProjectApplications();
    this.fetchTechnologies();
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute;
    },
  },
};
</script>

<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  padding: 1.5rem;
  border-radius: 0.5rem;
  width: 60%;
  max-height: 90vh;
  overflow-y: auto;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 🌟 Красивый скроллбар */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #4d4d4e;
  border-radius: 4px;
  border: 2px solid transparent;
  background-clip: padding-box;
  transition: background-color 0.2s;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: #718096;
}

.bg-hover {
  background-color: var(--color-hover);
}
</style>
