<template>
  <div class="min-h-screen text-white flex flex-col">
    <!-- Хедер -->
    <header class="flex justify-between border-b border-zinc-700 p-4">
      <div class="flex items-center gap-4 ml-auto">
        <ul class="flex items-center gap-10">
          <li
            class="flex items-center gap-3 hover:text-purple-400 duration-500"
          >
            <button>Биржа</button>
          </li>
          <li
            class="flex items-center gap-3 hover:text-purple-400 duration-500"
          >
            <button>Команды</button>
          </li>
          <li
            class="flex items-center gap-3 hover:text-purple-400 duration-500"
          >
            <button>Идеи</button>
          </li>
        </ul>
        <img src="/notific.svg" alt="notification" class="w-10 ml-5" />
      </div>
    </header>

    <!-- Основной контейнер профиля -->
    <div class="flex w-4/5 mx-auto mt-10 gap-6">
      <!-- Левый блок (Информация о пользователе) -->
      <div
        class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg"
        className="p-3 border-solid border-2 border-purple-400 rounded-lg"
      >
        <div class="text-center">
          <img
            class="w-32 h-32 rounded-full border-4 border-purple-400 mx-auto"
            src="https://via.placeholder.com/150"
            alt=""
          />
          <h1 class="text-2xl font-semibold mt-4">
            {{ user.name }} {{ user.surname }}
          </h1>
          <p class="text-purple-400 text-lg">{{ user.role }}</p>
        </div>
        <div class="mt-5">
          <p><span class="font-bold">📧 Почта:</span> {{ user.email }}</p>
          <p><span class="font-bold">📞 Телефон:</span> {{ user.phone }}</p>
          <p><span class="font-bold">🎓 Группа:</span> {{ user.group }}</p>
        </div>
      </div>

      <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
      <div
        class="w-3/4 bg-zinc-700 p-6 rounded-2xl shadow-lg"
        className="p-3 border-solid border-2 border-purple-400 rounded-lg"
      >
        <h2 class="text-2xl font-semibold mb-4">Информация о пользователе</h2>

        <div class="grid grid-cols-2 gap-6">
          <!-- Проекты -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              👾 Активность пользователя
            </h3>
            <ul>
              <li
                v-for="project in user.projects"
                :key="project"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ project }}
              </li>
            </ul>
          </div>

          <!-- Команды -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              👥 Командная деятельность
            </h3>
            <ul>
              <li
                v-for="team in user.teams"
                :key="team"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ team }}
              </li>
            </ul>
          </div>

          <!-- Стек технологий -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              🛠 Используемый Стек технологий
            </h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tech in user.technologies"
                :key="tech"
                class="p-2 bg-purple-400 rounded-md"
              >
                {{ tech }}
              </span>
            </div>
          </div>

          <!-- Оценки за проекты -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              ⭐️ Баллы за проекты
            </h3>
            <ul>
              <li
                v-for="score in user.scores"
                :key="score.project"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ score.project }} -
                <span class="font-bold">{{ score.grade }}/10</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: "Имён",
        surname: "Имёнович",
        role: "Студент",
        email: "student@example.com",
        phone: "+7 800-555-35-35",
        group: "АСОиУБ-24-1",
        projects: [
          "Биржа проектов",
          "Форум разработчиков",
          "Система тестирования",
        ],
        teams: ["Team Alpha", "Web Masters"],
        technologies: ["Vue.js", "Node.js", "TailwindCSS"],
        scores: [
          { project: "Биржа проектов", grade: 9 },
          { project: "Форум разработчиков", grade: 8 },
          { project: "Система тестирования", grade: 10 },
        ],
      },
    };
  },
};
</script>
