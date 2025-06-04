<template>
  <div
    class="modal-wrapper fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50"
  >
    <div
      class="modal-content bg-card p-6 rounded-lg shadow-lg w-3/5 max-h-[90vh] overflow-y-auto"
    >
      <h2 class="text-2xl font-bold mb-4 text-dynamic">Заявки в команду</h2>


      <!-- 📌 Таблица с заявками от фрилансеров -->
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
                @click="viewProfile(freelancer.user)"
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
  fetchJoinRequestsByTeam,
  acceptJoinRequest,
  cancelJoinRequestPost,
} from "@/services/joinRequests";
import api from "@/composables/auth.js";

export default {
  inject: ["globalState"],
  name: "ProjectApplications",
  props: {
    teamId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      technologiesMap: {},
      teamApplications: [],
      freelancerApplications: [],
    };
  },
  methods: {
    async loadApplications() {
    try {
      const requests = await fetchJoinRequestsByTeam(this.teamId);

      // подгружаем данные пользователей для каждой заявки
      const detailedRequests = await Promise.all(
        requests.map(async (req) => {
          const userDetails = await this.fetchUserDetails(req.user);
          return {
            ...req,
            user_full_name: userDetails.user_full_name,
            skills: userDetails.skills,
          };
        })
      );

      this.freelancerApplications = detailedRequests;
    } catch (e) {
      console.error("Ошибка при загрузке заявок с деталями пользователей", e);
    }
  },

  async acceptApplication(id, freelancer) {
    try {
      await acceptJoinRequest(id);
      await this.loadApplications();
    } catch (e) {
      alert("Ошибка при принятии заявки");
      console.error(e);
    }
  },

  async cancelApplication(id, freelancer) {
    try {
      await cancelJoinRequestPost(id);
      await this.loadApplications();
    } catch (e) {
      alert("Ошибка при отмене заявки");
      console.error(e);
    }
  },
    viewProfile(userId) {
    this.$router.push(`/${this.selectedInstitute}/profile/${userId}`);
  },
    async fetchTechnologies() {
    try {
      const response = await api.get('/core/technologies');
      const map = {};
      response.data.forEach(tech => {
        map[tech.id] = tech.name;
      });
      this.technologiesMap = map;
    } catch (error) {
      console.error("Ошибка при загрузке технологий:", error);
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
    console.error(
      `Ошибка при получении информации о пользователе с ID ${userId}:`,
      error
    );
    return {
      user_full_name: "Неизвестно",
      skills: [],
    };
  }
},

  },
  async mounted() {
    await this.fetchTechnologies();
    await this.loadApplications();
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
