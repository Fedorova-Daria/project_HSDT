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
            <th class="p-3 text-left">Избранное</th>
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
            v-for="(team, index) in sortedTeams"
            :key="index"
            :class="{
              'bg-cards': !team.markedForDeletion,
              'bg-marked-for-deletion': team.markedForDeletion,
              'bg-favorite': team.isFavorite,
            }"
            class="transition-colors text-white hover:bg-zinc-600"
          >
            <!-- Кнопка "Избранное" -->
            <td class="p-3 border-t border-zinc-600">
              <button
                class="btn bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 transition-colors w-15 cursor-pointer"
                @click="toggleFavorite(team)"
              >
                {{ team.isFavorite ? "★" : "☆" }}
              </button>
            </td>
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
                class="btn bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors cursor-pointer"
                @click="viewTeamDetails(team.name)"
              >
                Подробнее
              </button>
              <button
                class="px-4 py-2 rounded-md transition-all transform hover:scale-105 ml-2 cursor-pointer"
                @click="markTeamForDeletion(team)"
              >
                ❌
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Кнопка "Создать команду" -->
      <button
        class="w-25 mt-4 px-6 py-2 rounded-md transition-all transform hover:scale-105"
        @click="openCreateModal"
      >
        <img
          :src="liked ? 'Penis.svg' : 'Penis2.svg'"
          alt="Like"
          class="w-6 h-6 mr-4 mb-5 duration-300 cursor-pointer"
        />
      </button>

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

export default {
  components: {
    Header,
    TeamCreate,
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
          isFavorite: false,
        },
        {
          name: "Команда 2",
          members: 5,
          techStack: ["React", "Express", "MongoDB"],
          rating: 9,
          status: "В поисках",
          isFavorite: false,
        },
      ],
      isCreateModalOpen: false,
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
  computed: {
    sortedTeams() {
      return [...this.teams].sort((a, b) => {
        if (a.isFavorite && !b.isFavorite) return -1;
        if (!a.isFavorite && b.isFavorite) return 1;
        return 0;
      });
    },
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
  },
};
</script>

<style>
.bg-cards {
  background-color: #374151;
}

.bg-cards:hover {
  background-color: #4b5563;
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
</style>
