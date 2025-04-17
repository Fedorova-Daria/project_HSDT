<template>
  <div>
    <table class="w-full border-collapse shadow-lg rounded-lg overflow-hidden mt-5">
      <thead class="bg-card text-white">
        <tr>
          <th class="p-3 text-left w-10"></th>
          <th class="p-3 text-left w-1/4">Название команды</th>
          <th class="p-3 text-left w-1/4">Количество человек</th>
          <th class="p-3 text-left w-1/8">Навыки</th>
          <th class="p-3 text-left w-1/8">Статус</th>
          <th class="p-3 text-left w-1/6"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="team in sortedTeams"
          :key="team.id"
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
          <td class="p-3 border-t border-zinc-600">{{ team.members.length }}</td>
          <td class="p-3 border-t border-zinc-600">
            <!-- Отображаем навыки всех участников команды -->
            <div v-if="team.members && team.members.length">
              <div
                v-for="member in team.members"
                :key="member.id"
                class="mb-2"
              >
                <span>
                  {{ formatSkills(member.skills) }}
                </span>
              </div>
            </div>
            <div v-else>Нет участников</div>
          </td>
          <td class="p-3 border-t border-zinc-600">
            <span class="flex justify-between px-3 py-1 rounded-full">
              {{ team.status }}
            </span>
          </td>
          <td class="p-3 border-t border-zinc-600">
            <button
              class="button btn text-white px-4 py-2 rounded-md transition-colors hover:button:hover cursor-pointer"
              @click="viewTeamDetails(team)"
            >
              Подробнее
            </button>
            <button
              class="px-4 py-2 rounded-md transition-all transform hover:scale-105 ml- cursor-pointer"
              @click="markTeamForDeletion(team)"
            >
              ❌
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { instituteStyles } from "@/assets/instituteStyles.js";

export default {
  inject: ["globalState"], // Глобальное состояние
  props: ['teams', 'availableTechStack'],
  computed: {
    sortedTeams() {
      return [...this.teams].sort((a, b) => b.isFavorite - a.isFavorite);
    },
    selectedInstitute() {
      return this.globalState ? this.globalState.institute : null;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style ? style : { buttonOffColor: "#ccc" };
    },
  },
  methods: {
  viewTeamDetails(team) {
    const institute = this.selectedInstitute;
    if (institute) {
      this.$router.push({ path: `/${institute}/team/${team.id}` });
    } else {
      console.error("Институт не выбран");
    }
  },
  toggleFavorite(team) {
    team.isFavorite = !team.isFavorite;
  },
  markTeamForDeletion(team) {
    if (!team.status) team.status = 'Не указан';
    if (team.markedForDeletion === undefined) team.markedForDeletion = false;
    team.status = 'Проверяем';
    team.markedForDeletion = true;
  },
  /**
   * Форматирует массив навыков:
   *  - Если навыков нет — возвращает "Нет навыков".
   *  - Если навыков больше 3, показывает первые 3 и добавляет «+N».
   *  - Иначе выводит все навыки, разделённые запятыми.
   *
   * @param {Array} skills - Массив названий навыков.
   * @returns {String} Отформатированная строка.
   */
  formatSkills(skills) {
    if (!Array.isArray(skills) || skills.length === 0) {
      return "Нет навыков";
    }
    if (skills.length > 3) {
      const firstThree = skills.slice(0, 3);
      const remainder = skills.length - 3;
      return firstThree.join(", ") + " +" + remainder;
    }
    return skills.join(", ");
  },
},
};
</script>
  
  <style scoped>
  /* Стили для размытого фона */
.blurred-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-repeat: no-repeat;
  filter: blur(10px); /* Размытие фона */
  z-index: -1; /* Фон будет под основным содержимым */
  pointer-events: none; /* Фон не блокирует взаимодействие */
}

/* Затемняющий слой */
.blurred-bg::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(
    0,
    0,
    0,
    0.5
  ); /* Затемнение (0.5 = 50% прозрачности) */
  z-index: 1;
}

/* Остальные стили */
.bg-cards {
  background-color: #292929;
}

.bg-cards:hover {
  background-color: #222222;
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
.button {
  transition: background-color 0.3s, transform 0.2s;
  background-color: v-bind("instituteStyle.buttonOffColor");
}
.button:hover {
  background-color: v-bind("instituteStyle.buttonOnColor");
  transform: scale(1.05);
}
  </style>