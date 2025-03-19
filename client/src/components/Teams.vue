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
            class="bg-cards transition-colors text-white hover:bg-zinc-700"
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
                  'bg-purple-500': team.status === 'Заблокирован',
                  'bg-blue-500': team.status === 'На рассмотрении',
                  'bg-orange-500': team.status === 'На отдыхе',
                }"
                class="flex justify-between px-3 py-1 rounded-full text-sm w-22"
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
            <!--ТУТ ШТУКА, КОТОРАЯ ЗАДАЁТ КОЛИЧЕСТВО ЧЕЛОВЕК КОМАНДАМ РУКАМИ-->
            <!--
            <div class="mb-4">
              <label class="block text-white mb-2">Количество человек</label>
              <input
                v-model.number="newTeam.members"
                type="number"
                min="1"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
              <p v-if="newTeam.members < 1" class="text-red-500 text-sm mt-1">
                Количество участников должно быть больше 0.
              </p>
            </div> -->
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

            <!--ТУТ ШТУКА, КОТОРАЯ ЗАДАЁТ РЕЙТИНГ КОМАНДАМ РУКАМИ-->

            <!--<div class="mb-4">
              <label class="block text-white mb-2">Рейтинг</label>
              <input
                v-model.number="newTeam.rating"
                type="number"
                min="0"
                max="10"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
            </div> -->

            <div class="mb-4">
              <label class="block text-white mb-2">Статус</label>
              <select
                v-model="newTeam.status"
                class="w-full p-2 rounded bg-zinc-700 text-white"
              >
                <option value="В работе">В работе</option>
                <option value="В поисках">В поисках</option>
                <option value="Неактивна">Неактивна</option>
                <option value="Заблокирован">Заблокирован</option>
                <option value="На рассмотрении">На рассмотрении</option>
                <option value="На отдыхе">На отдыхе</option>
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

      <!-- Модальное окно для редактирования команды -->
      <div
        v-if="isEditModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      >
        <div class="bg-zinc-800 p-6 rounded-lg w-1/3">
          <h2 class="text-white text-xl mb-4">Редактировать команду</h2>
          <form @submit.prevent="saveEditedTeam">
            <div class="mb-4">
              <label class="block text-white mb-2">Название команды</label>
              <input
                v-model="editedTeam.name"
                type="text"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Количество человек</label>
              <input
                v-model.number="editedTeam.members"
                type="number"
                min="1"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
              <p
                v-if="editedTeam.members < 1"
                class="text-red-500 text-sm mt-1"
              >
                Количество участников должно быть больше 0.
              </p>
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
                    :id="`edit-${tech}`"
                    :value="tech"
                    v-model="editedTeam.techStack"
                    class="mr-2"
                  />
                  <label :for="`edit-${tech}`" class="text-white">{{
                    tech
                  }}</label>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Рейтинг (0-10)</label>
              <input
                v-model.number="editedTeam.rating"
                type="number"
                min="0"
                max="10"
                class="w-full p-2 rounded bg-zinc-700 text-white"
                required
              />
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Статус</label>
              <select
                v-model="editedTeam.status"
                class="w-full p-2 rounded bg-zinc-700 text-white"
              >
                <option value="В работе">В работе</option>
                <option value="В поисках">В поисках</option>
                <option value="Неактивна">Неактивна</option>
                <option value="Заблокирован">Заблокирован</option>
                <option value="На рассмотрении">На рассмотрении</option>
                <option value="На отдыхе">На отдыхе</option>
              </select>
            </div>
            <div class="flex justify-end">
              <button
                type="button"
                class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2"
                @click="closeEditModal"
              >
                Отмена
              </button>
              <button
                type="submit"
                class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors"
                :disabled="editedTeam.members < 1"
              >
                Сохранить
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
      // Данные таблицы
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
      // Состояние модальных окон
      isCreateModalOpen: false,
      isEditModalOpen: false,
      // Данные для новой команды
      newTeam: {
        name: "",
        members: 1, // Начальное значение 1, чтобы избежать 0
        techStack: [],
        rating: 0,
        status: "В поисках",
      },
      // Данные для редактирования команды
      editedTeam: null,
      // Список доступных технологий
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
    // Переход на страницу деталей команды
    viewTeamDetails(teamName) {
      this.$router.push({ name: "TeamDetails", params: { name: teamName } });
    },

    // Открыть модальное окно создания
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    // Закрыть модальное окно создания
    closeCreateModal() {
      this.isCreateModalOpen = false;
      this.resetNewTeam();
    },
    // Сбросить данные новой команды
    resetNewTeam() {
      this.newTeam = {
        name: "",
        members: 1, // Сбрасываем на 1, чтобы избежать 0
        techStack: [],
        rating: 0,
        status: "В поисках",
      };
    },
    // Создать новую команду
    createTeam() {
      if (this.newTeam.members < 1) {
        return; // Не создаем команду, если участников меньше 1
      }
      this.teams.push({ ...this.newTeam });
      this.closeCreateModal();
    },
    // Открыть модальное окно редактирования
    openEditModal(team) {
      this.editedTeam = { ...team };
      this.isEditModalOpen = true;
    },
    // Закрыть модальное окно редактирования
    closeEditModal() {
      this.isEditModalOpen = false;
      this.editedTeam = null;
    },
    // Сохранить изменения команды
    saveEditedTeam() {
      if (this.editedTeam.members < 1) {
        return; // Не сохраняем, если участников меньше 1
      }
      const index = this.teams.findIndex(
        (team) => team.name === this.editedTeam.name
      );
      if (index !== -1) {
        this.teams.splice(index, 1, { ...this.editedTeam });
      }
      this.closeEditModal();
    },
  },
};
</script>

<style>
/* Дополнительные стили */
.bg-cards {
  background-color: #1f2937; /* Цвет фона строк таблицы */
}

.bg-cards:hover {
  background-color: #374151; /* Цвет фона при наведении */
}

.bg-zinc-800 {
  background-color: #1f2937; /* Цвет фона заголовка таблицы */
}

.border-zinc-600 {
  border-color: #4b5563; /* Цвет границ */
}
</style>
