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
            <th class="p-3 text-left">Статус</th>
            <th class="p-3 text-left">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(team, index) in teams"
            :key="index"
            class="bg-cards transition-colors text-white"
          >
            <td class="p-3 border-t border-zinc-200">{{ team.name }}</td>
            <td class="p-3 border-t border-zinc-200">{{ team.members }}</td>
            <td class="p-3 border-t border-zinc-200">{{ team.status }}</td>
            <td class="p-3 border-t border-zinc-200">
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
        @click="createTeam"
      >
        Создать команду
      </button>
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
        { name: "Команда 1", members: 3, status: "В работе" },
        { name: "Команда 2", members: 5, status: "В поисках" },
      ],
    };
  },
  methods: {
    // Метод для показа деталей команды
    showDetails(team) {
      alert(`Детали команды: ${team.name}`);
    },
    // Метод для создания новой команды
    createTeam() {
      this.teams.push({
        name: `Команда ${this.teams.length + 1}`,
        members: 0,
        status: "В поисках",
      });
    },
  },
};
</script>
