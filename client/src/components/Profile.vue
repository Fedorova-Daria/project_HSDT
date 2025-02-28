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
      <div class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
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
        <!-- Кнопка для открытия модального окна -->
        <button
          @click="showModal = true"
          class="w-full mt-4 py-2 bg-purple-600 text-white rounded-lg transition duration-300 hover:bg-purple-500 hover:shadow-lg"
        >
          Редактировать профиль
        </button>
      </div>

      <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
      <div class="w-3/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
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

    <!-- Модальное окно -->
    <div
      v-if="showModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-zinc-700 p-6 rounded-lg shadow-lg">
        <h2 class="text-purple-500 text-xl font-bold mb-4">
          Редактировать профиль
        </h2>
        <div
          class="w-full max-w-md p-6 border border-purple-400 rounded-lg bg-zinc-700 text-white"
        >
          <h1 class="text-purple-500 text-2xl font-bold mb-4">
            Профиль пользователя
          </h1>
          <form @submit.prevent="updateProfile">
            <div class="form-group mb-4">
              <label for="email" class="font-bold text-purple-300"
                >Email:</label
              >
              <input
                type="email"
                id="email"
                v-model="user.email"
                required
                class="mt-1 block w-full p-2 border border-purple-400 rounded"
              />
            </div>
            <div class="form-group mb-4">
              <label for="phone" class="font-bold text-purple-300"
                >Телефон:</label
              >
              <input
                type="tel"
                id="phone"
                v-model="user.phone"
                required
                class="mt-1 block w-full p-2 border border-purple-400 rounded"
              />
            </div>
            <div class="form-group mb-4">
              <label for="bio" class="font-bold text-purple-300"
                >Немного о себе:</label
              >
              <textarea
                id="bio"
                v-model="user.bio"
                maxlength="40"
                class="mt-1 block w-full p-2 border border-purple-400 rounded"
              ></textarea>
            </div>
            <button
              type="submit"
              class="w-full mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600"
            >
              Сохранить изменения
            </button>
          </form>

          <h2 class="text-purple-500 text-xl font-bold mt-6">
            Информация о пользователе
          </h2>

          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Телефон:</strong> {{ user.phone }}</p>
          <p><strong>Немного о себе:</strong> {{ user.bio }}</p>
        </div>
        <button
          @click="showModal = false"
          class="mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: "",
        surname: "",
        email: "",
        phone: "",
        bio: "",
        techStack: "",
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
      showModal: false, // Добавлено состояние для управления модальным окном
    };
  },
  methods: {
    updateProfile() {
      console.log("Профиль обновлен:", this.user);
      alert("Профиль успешно обновлен!");
    },
    cancelEdit() {
      this.user = {
        name: "",
        surname: "",
        email: "",
        phone: "",
        bio: "",
        techStack: "",
      };
    },
    goToChangeProfile() {
      this.$router.push("/ChangeProfile");
    },
  },
};
</script>
