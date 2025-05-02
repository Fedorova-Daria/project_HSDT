<template>
  <div class="modal-wrapper fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
    <div class="modal-content bg-white p-6 rounded shadow-lg w-3/5">
      <h2 class="text-2xl font-bold mb-4">Заявки на проект</h2>

      <!-- 📌 Таблица с заявками от команд -->
      <h3 class="text-xl font-semibold mt-4">Команды</h3>
      <table class="w-full border-collapse border border-gray-300 text-center">
        <thead>
          <tr class="bg-gray-100">
            <th class="border border-gray-300 p-2">Название команды</th>
            <th class="border border-gray-300 p-2">Количество участников</th>
            <th class="border border-gray-300 p-2">Навыки</th>
            <th class="border border-gray-300 p-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="team in teamApplications" :key="team.id">
            <td class="border border-gray-300 p-2">{{ team.name }}</td>
            <td class="border border-gray-300 p-2">{{ team.members.length }}</td>
            <td class="border border-gray-300 p-2">{{ team.skills.join(', ') }}</td>
            <td class="border border-gray-300 p-2 flex justify-center space-x-2">
              <button @click="acceptApplication(team.applicationId, team)" class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
                Принять
              </button>
              <button @click="cancelApplication(team.applicationId)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
                Отменить
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 📌 Таблица с заявками от фрилансеров -->
      <h3 class="text-xl font-semibold mt-6">Фрилансеры</h3>
      <table class="w-full border-collapse border border-gray-300 text-center">
        <thead>
          <tr class="bg-gray-100">
            <th class="border border-gray-300 p-2">ID Фрилансера</th>
            <th class="border border-gray-300 p-2">Дата подачи заявки</th>
            <th class="border border-gray-300 p-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="freelancer in freelancerApplications" :key="freelancer.id">
            <td class="border border-gray-300 p-2">{{ freelancer.freelancer }}</td>
            <td class="border border-gray-300 p-2">{{ new Date(freelancer.created_at).toLocaleString() }}</td>
            <td class="border border-gray-300 p-2 flex justify-center space-x-2">
              <button @click="acceptApplication(freelancer.id, freelancer)" class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
                Принять
              </button>
              <button @click="cancelApplication(freelancer.id, freelancer)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
                Отменить
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Кнопка закрытия -->
      <button class="mt-4 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600" @click="$emit('close')">
        Закрыть
      </button>
    </div>
  </div>
</template>

<script>
import { getProjectApplications, acceptProjectApplication, cancelProjectApplication } from "@/services/projectRequests";
import api from "@/composables/auth.js";

export default {
  name: "ProjectApplications",
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      teamApplications: [], // Заявки от команд
      freelancerApplications: [], // Заявки от фрилансеров
    };
  },
  methods: {
    async fetchProjectApplications() {
  try {
    const applications = await getProjectApplications();

    // 🔹 Фильтруем заявки только для открытого проекта и со статусом "pending"
    const filteredApplications = applications.filter(app => app.project === Number(this.projectId) && app.status === "pending");

    // 🔹 Разделяем заявки команд и фрилансеров
    const teamPromises = filteredApplications
      .filter(app => app.team) // Только команды
      .map(app => this.fetchTeamDetails(app.team, app.id));

    this.freelancerApplications = filteredApplications.filter(app => app.freelancer); // Только фрилансеры
    this.teamApplications = await Promise.all(teamPromises);
  } catch (error) {
    console.error("Ошибка при получении заявок:", error);
  }
},

async fetchTeamDetails(teamId, applicationId) {
      try {
        const response = await api.get(`/teams/${teamId}/`);
        return { ...response.data, applicationId }; // Добавляем ID заявки
      } catch (error) {
        console.error(`Ошибка при получении информации о команде с ID ${teamId}:`, error);
        return null;
      }
    },
  async acceptApplication(id, applicationData) {
    try {
      const acceptData = {
        applicant_type: applicationData.applicant_type || null,
        project: applicationData.project || null,
        freelancer: applicationData.freelancer || null,
        team: applicationData.team || null
      };

      console.log("Отправляемые данные:", acceptData);

      await acceptProjectApplication(id, acceptData);
      alert("Заявка принята!");
      this.fetchProjectApplications(); // Обновляем список заявок
    } catch (error) {
      alert("Ошибка при принятии заявки.");
      console.error(error);
    }
  },

    async cancelApplication(id, applicationData) {
  try {
    if (!applicationData) {
      console.error("Ошибка: applicationData отсутствует!", id);
      return;
    }

    const cancelData = {
      applicant_type: applicationData.applicant_type || null,
      project: applicationData.project || null,
      freelancer: applicationData.freelancer || null,
      team: applicationData.team || null
    };

    console.log("Отправляемые данные:", JSON.stringify(cancelData, null, 2));

    await cancelProjectApplication(id, cancelData);
    alert("Заявка отменена!");
    this.fetchProjectApplications(); // Обновляем список
  } catch (error) {
    alert("Ошибка при отмене заявки.");
    console.error(error);
  }
},
    async cancelApplication(id, applicationData) {
      // Формируем объект для отправки заявки на принятие
    const cancelData = {
      applicant_type: applicationData.applicant_type || null,
      project: applicationData.project || null,
      freelancer: applicationData.freelancer || null,
      team: applicationData.team || null
    };
      try {
        await cancelProjectApplication(id, cancelData );
        alert("Заявка отменена!");
        this.fetchProjectApplications(); // Обновляем список
      } catch (error) {
        alert("Ошибка при отмене заявки.");
        console.error(error);
      }
    },
  },
  mounted() {
    this.fetchProjectApplications();
  },
};
</script>

<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: right;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  width: 600px;
  height: 100%;
  max-width: 90%;
}
</style>
