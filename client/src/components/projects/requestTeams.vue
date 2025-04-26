<template>
  <div class="modal-wrapper fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
    <div class="modal-content bg-white p-6 rounded shadow-lg w-3/5">
      <h2 class="text-2xl font-bold mb-4">Команды, откликнувшиеся на проект</h2>

      <!-- Таблица с заявками -->
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
          <tr v-for="team in teams" :key="team.id">
            <td class="border border-gray-300 p-2">{{ team.name }}</td>
            <td class="border border-gray-300 p-2">{{ team.members_count }}</td>
            <td class="border border-gray-300 p-2">{{ team.skills.join(', ') }}</td>
            <td class="border border-gray-300 p-2 flex justify-center space-x-2">
              <button
                @click="viewTeam(team.id)"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
              >
                Подробнее
              </button>

              <button
                @click="selectTeam(team.id)"
                class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
              >
                Добавить в проект
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Кнопка закрытия -->
      <button
        class="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        @click="$emit('close')"
      >
        Закрыть
      </button>
    </div>
  </div>
</template>

<script>
import api from "@/composables/auth.js";

export default {
  name: "RespondedTeams",
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      teams: [], // Список отозвавшихся команд
    };
  },
  created() {
    this.fetchRespondedTeams();
  },
  methods: {
    /**
     * Загружает список команд через API.
     */
     async fetchRespondedTeams() {
  try {
    // Получаем данные конкретной команды с ID = 1
    const response = await api.get(`/teams/1/`);

    // Проверяем, если ответ содержит корректные данные команды
    if (response.data && response.data.id) {
      // Записываем команду в массив
      this.teams = [
        {
          id: response.data.id,
          name: response.data.name || "Без названия",
          members_count: response.data.members?.length || 0,
          skills: response.data.skills || [],
        },
      ];
    } else {
      console.error("Ответ API не содержит данных команды:", response.data);
      this.teams = []; // Устанавливаем пустой массив, если данные некорректны
    }

    console.log("Загруженные команды:", this.teams);
  } catch (error) {
    console.error("Ошибка при загрузке команды:", error.response?.data || error);
  }
},
    /**
     * Переход на страницу команды.
     */
    viewTeam(teamId) {
      this.$router.push(`/teams/${teamId}`);
    },
    /**
     * Добавляет команду в проект через API.
     */
    async selectTeam(teamId) {
      try {
        const url = `/projects/${this.projectId}/select-team/${teamId}/`;
        await api.post(url, null, { headers: { "Content-Type": "application/json" } });
        alert("Команда успешно добавлена в проект!");
      } catch (error) {
        console.error("Ошибка при добавлении команды в проект:", error.response?.data || error);
        alert("Ошибка при добавлении команды в проект.");
      }
    },
  },
};
</script>

<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  width: 600px;
  max-width: 90%;
}
</style>