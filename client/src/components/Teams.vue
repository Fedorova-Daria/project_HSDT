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
            <th class="p-3 text-left min-w-[200px]">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(team, index) in teams"
            :key="index"
            :class="{
              'bg-purple-500': team.markedForDeletion,
              'bg-zinc-700': !team.markedForDeletion,
            }"
            class="transition-colors text-white hover:bg-zinc-600"
          >
            <!-- Кнопка "Избранное" -->
            <td class="p-3 border-t border-zinc-600">
              <button
                class="w-25 mt-4 px-6 py-2 rounded-md transition-all transform hover:scale-105"
                :class="{ 'animate-pulse': team.isFavorite }"
                @click="toggleFavorite(team)"
              >
                <img
                  :src="team.isFavorite ? 'cross.svg' : 'cross2.svg'"
                  alt="Like"
                  class="w-6 h-6 mr-4 mb-5 duration-300 cursor-pointer hover:text-yellow-500"
                />
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
              <div class="button-container">
                <button
                  class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-all transform hover:scale-105 cursor-pointer"
                  @click="viewTeamDetails(team.name)"
                >
                  Подробнее
                </button>
                <button
                  class="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 transition-all transform hover:scale-105 ml-2 cursor-pointer"
                  @click="openEditModal(team)"
                >
                  Редактировать
                </button>
                <button
                  class="px-4 py-2 rounded-md transition-all transform hover:scale-105 ml-2 cursor-pointer"
                  @click="markTeamForDeletion(team)"
                >
                  ❌
                </button>
              </div>
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

      <!-- Модальные окна -->
      <TeamModalDetails
        v-if="isCreateModalOpen"
        :available-tech-stack="availableTechStack"
        @create-team="createTeam"
        @close-modal="closeCreateModal"
      />
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
          isFavorite: false,
          markedForDeletion: false,
        },
        {
          name: "Команда 2",
          members: 5,
          techStack: ["React", "Express", "MongoDB"],
          rating: 9,
          status: "В поисках",
          isFavorite: false,
          markedForDeletion: false,
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
    toggleFavorite(team) {
      team.isFavorite = !team.isFavorite;
    },
    markTeamForDeletion(team) {
      team.markedForDeletion = true;
      team.status = "Проверяем";
    },
    // Остальные методы
  },
};
</script>

<style>
.animate-pulse {
  animation: pulse 0.5s ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}
</style>
