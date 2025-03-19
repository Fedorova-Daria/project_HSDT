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
            <th class="p-3 text-left">Действия</th>
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
              <button
                class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
                @click="viewTeamDetails(team.name)"
              >
                Подробнее
              </button>
              <button
                class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors ml-2"
                @click="markTeamForDeletion(team)"
              >
                Удалить
              </button>
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
      <div
        v-if="isCreateModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      >
        <div class="bg-zinc-800 p-6 rounded-lg w-1/3">
          <h2 class="text-white text-xl mb-4">Создать новую команду</h2>
          <form @submit.prevent="createTeam">
            <div class="mb-4">
              <label class="block text-white mb-2">Название команды</label>
              <input
                v-model="newTeam.name"
                type="text"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Стек технологий</label>
              <div class="grid grid-cols-2 gap-2">
                <div
                  v-for="tech in availableTechStack"
                  :key="tech"
                  class="flex items-center"
                >
                  <input
                    type="checkbox"
                    :id="`create-${tech}`"
                    :value="tech"
                    v-model="newTeam.techStack"
                    class="mr-2"
                  />
                  <label :for="`create-${tech}`" class="text-white">{{
                    tech
                  }}</label>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Статус</label>
              <select
                v-model="newTeam.status"
                class="w-full p-2 rounded bg-zinc-700 text-white"
              >
                <option value="В работе">В работе</option>
                <option value="В поисках">В поисках</option>
                <option value="Неактивна">Неактивна</option>
                <option value="Проверяем">Проверяем</option>
                <option value="Забанена">Забанена</option>
              </select>
            </div>
            <div class="flex justify-end">
              <button
                type="button"
                class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2"
                @click="closeCreateModal"
              >
                Отмена
              </button>
              <button
                type="submit"
                class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors"
                :disabled="newTeam.members < 1"
              >
                Создать
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";

export default {
  components: {
    Header,
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
      newTeam: {
        name: "",
        members: 1,
        techStack: [],
        rating: 0,
        status: "В поисках",
      },
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
    isTeamNameUnique(name) {
      return !this.teams.some((team) => team.name === name);
    },
    viewTeamDetails(teamName) {
      this.$router.push({ name: "TeamDetails", params: { name: teamName } });
    },
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
      this.resetNewTeam();
    },
    resetNewTeam() {
      this.newTeam = {
        name: "",
        members: 1,
        techStack: [],
        rating: 0,
        status: "В поисках",
      };
    },
    createTeam() {
      if (this.newTeam.members < 1) {
        return;
      }
      if (!this.isTeamNameUnique(this.newTeam.name)) {
        alert("Команда с таким именем уже существует!");
        return;
      }
      this.teams.push({ ...this.newTeam });
      this.closeCreateModal();
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
</style>
