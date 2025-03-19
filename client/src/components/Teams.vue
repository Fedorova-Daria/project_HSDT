<template>
  <div>
    <Header />
    <div class="p-6 w-4/5 mx-auto">
      <!-- Таблица команд -->
      <table
        class="w-full border-collapse shadow-lg rounded-lg overflow-hidden"
      >
        <thead class="bg-zinc-800 text-white">
          <tr>
            <th class="p-3 text-left">Название команды</th>
            <th class="p-3 text-left">Количество человек</th>
            <th class="p-3 text-left">Стек технологий</th>
            <th class="p-3 text-left">Рейтинг (0-10)</th>
            <th class="p-3 text-left">Статус</th>
            <th class="p-3 text-left min-w-[200px]">Действия</th>
            <!-- Минимальная ширина для ячейки -->
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(team, index) in teams"
            :key="index"
            :class="{
              'bg-cards': !team.markedForDeletion,
              'bg-marked-for-deletion': team.markedForDeletion,
            }"
            class="transition-colors text-white hover:bg-zinc-700"
          >
            <td class="p-3 border-t border-zinc-600">{{ team.name }}</td>
            <td class="p-3 border-t border-zinc-600">{{ team.members }}</td>
            <td class="p-3 border-t border-zinc-600">
              <span
                v-for="(tech, i) in team.techStack"
                :key="i"
                class="bg-zinc-600 text-sm px-2 py-1 rounded-full mr-1"
              >
                {{ tech }}
              </span>
            </td>
            <td class="p-3 border-t border-zinc-600">{{ team.rating }}</td>
            <td class="p-3 border-t border-zinc-600">
              <span
                :class="{
                  'bg-green-500': team.status === 'В работе',
                  'bg-yellow-500': team.status === 'В поисках',
                  'bg-red-500': team.status === 'Неактивна',
                  'bg-purple-500': team.status === 'Забанена',
                  'bg-blue-500': team.status === 'Проверяем',
                }"
                class="flex justify-between px-3 py-1 rounded-full text-m w-27"
              >
                {{ team.status }}
              </span>
            </td>
            <td class="p-3 border-t border-zinc-600">
              <div class="button-container">
                <button
                  class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
                  @click="viewTeamDetails(team.name)"
                >
                  Подробнее
                </button>
                <button
                  class="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 transition-colors ml-2"
                  @click="openEditModal(team)"
                >
                  Редактировать
                </button>
                <button
                  class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors ml-2"
                  @click="markTeamForDeletion(team)"
                >
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Кнопка "Создать команду" -->
      <button
        class="mt-4 bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition-colors"
        @click="openCreateModal"
      >
        Создать команду
      </button>

      <!-- Модальное окно для создания команды -->
      <TeamModalDetails
        v-if="isCreateModalOpen"
        :available-tech-stack="availableTechStack"
        @create-team="createTeam"
        @close-modal="closeCreateModal"
      />

      <!-- Модальное окно для редактирования команды -->
      <TeamModalEdit
        v-if="isEditModalOpen"
        :edited-team="editedTeam"
        :available-tech-stack="availableTechStack"
        @save-edited-team="saveEditedTeam"
        @close-modal="closeEditModal"
      />
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import TeamModalDetails from "@/components/TeamModalDetails.vue";
import TeamModalEdit from "@/components/TeamModalEdit.vue";

export default {
  components: {
    Header,
    TeamModalDetails,
    TeamModalEdit,
  },
  data() {
    return {
      teams: [
        {
          name: "Команда 1",
          members: 3,
          techStack: ["Vue.js", "Node.js", "PostgreSQL"],
          rating: 7,
          status: "В работе",
        },
        {
          name: "Команда 2",
          members: 5,
          techStack: ["React", "Express", "MongoDB"],
          rating: 9,
          status: "В поисках",
        },
      ],
      isCreateModalOpen: false,
      isEditModalOpen: false,
      editedTeam: null,
      availableTechStack: [
        "Vue.js",
        "React",
        "Angular",
        "Node.js",
        "Express",
        "Django",
        "Flask",
        "PostgreSQL",
        "MongoDB",
        "MySQL",
        "GraphQL",
        "REST API",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "Git",
        "TypeScript",
        "JavaScript",
        "Python",
        "Java",
        "C#",
      ],
    };
  },
  methods: {
    viewTeamDetails(teamName) {
      this.$router.push({ name: "TeamDetails", params: { name: teamName } });
    },
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
    },
    createTeam(newTeam) {
      if (!this.isTeamNameUnique(newTeam.name)) {
        alert("Команда с таким именем уже существует!");
        return;
      }
      this.teams.push(newTeam);
      this.closeCreateModal();
    },
    isTeamNameUnique(name) {
      return !this.teams.some((team) => team.name === name);
    },
    openEditModal(team) {
      this.editedTeam = { ...team };
      this.isEditModalOpen = true;
    },
    closeEditModal() {
      this.isEditModalOpen = false;
    },
    saveEditedTeam(editedTeam) {
      const index = this.teams.findIndex(
        (team) => team.name === editedTeam.name
      );
      if (index !== -1) {
        this.teams.splice(index, 1, editedTeam);
      }
      this.closeEditModal();
    },
    markTeamForDeletion(team) {
      team.status = "Проверяем";
      team.markedForDeletion = true;
    },
  },
};
</script>


<style>
.bg-cards {
  background-color: #1f2937;
}

.bg-cards:hover {
  background-color: #374151;
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

/* Стили для контейнера кнопок */
.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* Отступ между кнопками */
}

/* Минимальная ширина для кнопок */
.button-container button {
  min-width: 100px; /* Минимальная ширина кнопки */
}
</style>
