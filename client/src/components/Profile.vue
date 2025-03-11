<template>
  <div class="min-h-screen text-white flex flex-col">
    <!-- Хедер -->
    <Header />
    <!-- Основной контейнер профиля -->
    <div class="flex w-4/5 mx-auto mt-10 gap-6">
      <!-- Левый блок (Информация о пользователе) -->
      <div class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <div class="text-center">
          <img
            class="w-32 h-32 rounded-full border-4 border-purple-400 mx-auto"
            :src="user.avatar || 'https://via.placeholder.com/150'"
            alt="Аватар пользователя"
          />
          <h1
            v-if="user.name && user.surname"
            class="text-2xl font-semibold mt-4"
          >
            {{ user.name }} {{ user.surname }}
          </h1>
          <p v-if="user.role" class="text-purple-400 text-lg">
            {{ user.role }}
          </p>
        </div>

        <div class="mt-5">
          <p>
            <span class="font-bold">📧 Почта:</span>
            {{ user.email || "Не указано" }}
          </p>
          <p>
            <span class="font-bold">🎓 Группа:</span>
            {{ user.group || "Не указано" }}
          </p>
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
            <ul v-if="user.projects && user.projects.length > 0">
              <li
                v-for="project in user.projects"
                :key="project"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ project }}
              </li>
            </ul>
            <p v-else class="text-gray-400">Нет активных проектов</p>
          </div>

          <!-- Команды -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              👥 Командная деятельность
            </h3>
            <ul v-if="user.teams && user.teams.length > 0">
              <li
                v-for="team in user.teams"
                :key="team"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ team }}
              </li>
            </ul>
            <p v-else class="text-gray-400">Нет командной активности</p>
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
            <ul v-if="user.scores && user.scores.length > 0">
              <li
                v-for="score in user.scores"
                :key="score.project"
                class="p-2 bg-gray-700 rounded-md mb-2"
              >
                {{ score.project }} -
                <span class="font-bold">{{ score.grade }}/10</span>
              </li>
            </ul>
            <p v-else class="text-gray-400">Нет оценок за проекты</p>
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
        <form
          @submit.prevent="updateProfile"
          class="w-full max-w-md p-6 border border-purple-400 rounded-lg bg-zinc-700 text-white"
        >
          <div class="form-group mb-4">
            <label for="email" class="font-bold text-purple-300">Email:</label>
            <input
              type="email"
              id="email"
              v-model="user.email"
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
import Header from "@/components/header.vue";
import {
  getUserData,
  getAccessToken,
  saveUserData,
  clearStorage,
} from "@/utils/localStorage";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { API_BASE_URL } from "@/config";

export default {
  components: { Header },
  data() {
    return {
      user: getUserData() || {
        name: "",
        surname: "",
        email: "",
        bio: "",
        avatar: "https://via.placeholder.com/150",
        group: { id: "", name: "" }, // Группа теперь объект
        projects: [],
        teams: [],
        technologies: [],
        scores: [],
      },
      showModal: false,
      token: getAccessToken(),
      avatarFile: null,
      groups: [], // Список групп из API
    };
  },
  async mounted() {
    if (this.token) {
      try {
        const decodedToken = jwtDecode(this.token);
        this.user = decodedToken.user || getUserData();
      } catch (error) {
        console.error("Ошибка при декодировании токена:", error);
        this.redirectToLogin();
      }
    } else {
      this.redirectToLogin();
    }

    // Загружаем данные о пользователе и список групп
    if (!this.user.name) {
      await this.fetchUserData();
    }
    await this.fetchGroups();
  },
  methods: {
    redirectToLogin() {
      clearStorage();
      window.location.href = "/login";
    },

    async fetchUserData() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/users/me/`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });

        this.user = response.data;

        // Если у пользователя указан `id` группы, подменяем его на `name`
        if (this.groups.length > 0) {
          const userGroup = this.groups.find((g) => g.id === this.user.group);
          this.user.group = userGroup
            ? { id: userGroup.id, name: userGroup.name }
            : { id: "", name: "Неизвестная группа" };
        }

        saveUserData(this.user);
      } catch (error) {
        console.error("Ошибка при получении данных пользователя:", error);
        this.redirectToLogin();
      }
    },

    async fetchGroups() {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/api/core/groups/list`
        );
        if (response.status === 200) {
          this.groups = response.data;

          // Если у пользователя уже есть `id` группы, ищем её название
          if (this.user.group.id) {
            const userGroup = this.groups.find(
              (g) => g.id === this.user.group.id
            );
            if (userGroup) {
              this.user.group = { id: userGroup.id, name: userGroup.name };
              saveUserData(this.user); // Сохраняем обновленные данные
            }
          }
        }
      } catch (error) {
        console.error("Ошибка при загрузке групп:", error);
      }
    },

    async updateProfile() {
      try {
        const response = await axios.put(
          `${API_BASE_URL}/api/users/me/`,
          { ...this.user, group: this.user.group.id }, // Отправляем только `id`
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        this.user = response.data;

        // Обновляем название группы после сохранения
        const userGroup = this.groups.find((g) => g.id === this.user.group);
        this.user.group = userGroup
          ? { id: userGroup.id, name: userGroup.name }
          : { id: "", name: "Неизвестная группа" };

        saveUserData(this.user);
        this.showModal = false;
        alert("Профиль успешно обновлен!");
      } catch (error) {
        console.error("Ошибка при обновлении профиля:", error);
      }
    },

    cancelEdit() {
      this.user = getUserData();
      this.showModal = false;
    },
  },
};
</script>
