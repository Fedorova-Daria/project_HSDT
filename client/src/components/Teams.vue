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
            <th class="p-3 text-left">Средний уровень</th>
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
            <td class="p-3 border-t border-zinc-600">
              {{ team.averageLevel }}
            </td>
            <td class="p-3 border-t border-zinc-600">
              <span
                :class="{
                  'bg-green-500': team.status === 'В работе',
                  'bg-yellow-500': team.status === 'В поисках',
                  'bg-red-500': team.status === 'Неактивна',
                }"
                class="px-3 py-1 rounded-full text-sm"
              >
                {{ team.status }}
              </span>
            </td>
            <td class="p-3 border-t border-zinc-600">
              <button
                class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
                @click="showDetails(team)"
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
            <div class="mb-4">
              <label class="block text-white mb-2">Количество человек</label>
              <input
                v-model="newTeam.members"
                type="number"
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
                    :id="tech"
                    :value="tech"
                    v-model="newTeam.techStack"
                    class="mr-2"
                  />
                  <label :for="tech" class="text-white">{{ tech }}</label>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <label class="block text-white mb-2">Средний уровень</label>
              <select
                v-model="newTeam.averageLevel"
                class="w-full p-2 rounded bg-zinc-700 text-white"
              >
                <option value="Низкий">Низкий</option>
                <option value="Средний">Средний</option>
                <option value="Высокий">Высокий</option>
              </select>
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
      // Данные таблицы
      teams: [
        {
          name: "Команда 1",
          members: 3,
          techStack: ["Vue.js", "Node.js", "PostgreSQL"],
          averageLevel: "Средний",
          status: "В работе",
        },
        {
          name: "Команда 2",
          members: 5,
          techStack: ["React", "Express", "MongoDB"],
          averageLevel: "Высокий",
          status: "В поисках",
        },
      ],
      // Состояние модального окна
      isCreateModalOpen: false,
      // Данные для новой команды
      newTeam: {
        name: "",
        members: 0,
        techStack: [],
        averageLevel: "Низкий",
        status: "В поисках",
      },
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
    // Открыть модальное окно
    openCreateModal() {
      this.isCreateModalOpen = true;
    },
    // Закрыть модальное окно
    closeCreateModal() {
      this.isCreateModalOpen = false;
      this.resetNewTeam();
    },
    // Сбросить данные новой команды
    resetNewTeam() {
      this.newTeam = {
        name: "",
        members: 0,
        techStack: [],
        averageLevel: "Низкий",
        status: "В поисках",
      };
    },
    // Создать новую команду
    createTeam() {
      // Добавляем новую команду
      this.teams.push({ ...this.newTeam });

      // Закрываем модальное окно и сбрасываем данные
      this.closeCreateModal();
    },
    // Показать детали команды
    showDetails(team) {
      alert(`Детали команды:\n
Название: ${team.name}\n
Количество человек: ${team.members}\n
Стек технологий: ${team.techStack.join(", ")}\n
Средний уровень: ${team.averageLevel}\n
Статус: ${team.status}`);
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
