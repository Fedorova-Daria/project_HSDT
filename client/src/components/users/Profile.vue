<template>
  <div class="relative min-h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <!--<img
      ref="backgroundImage"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105 -z-10"
      src="/bgg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />-->

    <!-- Затемнение фона -->
    <!--<div class="absolute inset-0 bg-black opacity-60 -z-10"></div>-->

    <div class="min-h-screen flex flex-col relative z-10">
      <!-- Хедер -->
      <Header />

      <!-- Основной контейнер профиля -->
      <div class="flex w-4/5 mx-auto mt-10 gap-6">
        <!-- Левый блок (Информация о пользователе) -->
        <div
          class="w-1/4 bg-card p-6 rounded-2xl shadow-lg backdrop-blur-sm"
        >
          <div class="text-center">
            <img
              class="w-32 h-32 rounded-full border-4 mx-auto cursor-pointer transition-colors"
              :src="userData.avatar || null"
              alt="Аватар пользователя"
              @click="showAvatarModal = true"
            />
            <h1
              v-if="userData.first_name && userData.last_name"
              class="text-2xl font-semibold mt-4"
            >
              {{ userData.first_name }} {{ userData.last_name }}
            </h1>
            <div class="mt-2">
              <span class="px-3 py-1 bg-purple-600 rounded-full text-sm">
                {{ userData.role || "Роль не указана" }}
              </span>
            </div>
          </div>

          <div class="mt-5 text-dynamic">
            <p class="text-sm flex justify-betwee">
              <strong>Почта:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-sm rounded-lg p-2.5 border border-zinc-600 font-medium"
            >
              {{ userData.email || "Не указано" }}
            </div>
            <p class="text-sm mt-2 flex justify-between">
              <strong>Группа:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-sm rounded-lg p-2.5 border border-zinc-600 font-medium"
            >
              {{ userData.university_group || "Не указано" }}
            </div>
          </div>

          <!-- Блок биографии -->
          <div class="mt-5">
            <p class="text-sm flex justify-between text-dynamic">
              <strong>Биография:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-input text-dynamic text-sm rounded-lg p-2.5 border border-zinc-600 min-h-[100px] font-medium"
            >
              {{ userData.bio || "Пока ничего не рассказал о себе" }}
            </div>
          </div>

          <button
          :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
            @click="showModal = true"
            class="w-full mt-4 py-2 text-always-white rounded-lg transition duration-300 hover:shadow-lg"
          >
            Редактировать профиль
          </button>
          <button
            @click="logout"
            class="w-full mt-2 py-2 bg-red-600 text-always-white rounded-lg transition duration-300 hover:bg-red-500 hover:shadow-lg"
          >
            Выйти
          </button>
        </div>

        <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
        <div
          class="w-3/4 bg-card p-6 rounded-2xl shadow-lg backdrop-blur-sm"
        >
          <h2 class="text-2xl font-semibold mb-4">Информация о пользователе</h2>

          <div class="flex gap-10">
            <!-- Проекты -->
            <div class="w-1/2">
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">Проекты</h3>
              <div class="mt-2">
                <div
                  v-for="(project, index) in userProjects"
                  :key="index"
                  class="mb-4 p-4 bg-input rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ project.title }}</h4>
                    <span
                      :class="{
                        'bg-green-500': project.status === 'Завершен',
                        'bg-blue-500': project.status === 'В работе',
                        'bg-yellow-500': project.status === 'Заморожен',
                      }"
                      class="px-2 py-1 rounded-full text-xs"
                    >
                      {{ project.status }}
                    </span>
                  </div>
                  <p class="text-sm mt-1">
                    {{ project.description }}
                  </p>
                  <div class="mt-2 flex justify-between items-center">
                    <div>
                      <span class="text-sm">Оценка: </span>
                      <span class="font-bold"> {{userProjects.averageRating }} /10</span>
                    </div>
                    <div>
                      <span class="text-sm">Участие: с {{ formatDate(project.date) }} по {{ formatDate(project.endDate) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Команды -->
            <div class="w-1/2">
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">Команды</h3>
              <div class="mt-2">
                <div
                  v-for="(team, index) in userTeams"
                  :key="index"
                  class="mb-4 p-4 bg-input rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ team.name }}</h4>
                    <span class="text-sm text-gray-300"
                      >{{ team.members.lenght }} участников</span
                    >
                  </div>
                  <div class="mt-2">
                    <p class="text-sm">
                    </p>
                    <p class="text-sm mt-1">
                      <span class="font-medium">Статус команды:</span>
                      <span class="ml-3"
                        :class="{
                          'text-green-400': team.teamStatus === 'Активна',
                          'text-red-400': team.teamStatus === 'Распущена',
                          'text-yellow-400': team.teamStatus === 'Заморожена',
                        }"
                      >
                        {{ team.status }}
                      </span>
                    </p>
                    <div class="mt-2 text-sm">
                      <p>
                        Участие: с {{ formatDate(team.joinDate) }} по {{ formatDate(team.leaveDate) }}
                      </p>
                    </div>
                    <button
                      class="mt-2 text-purple-300 hover:text-purple-200 text-sm flex items-center"
                    >
                      <span @click="goToTeam">Подробнее о команде</span>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 ml-1"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Список навыков -->
<h3 class="mt-10 text-xl font-semibold border-b pb-2 mb-3">Навыки</h3>
<div class="flex flex-wrap gap-2 mt-4">
  <span
    v-for="(tech, index) in userSkills"
    :key="index"
    class="px-3 py-1 bg-purple-600/50 rounded-full text-sm flex items-center"
  >
    {{ tech.name }}
    <button
      @click="removeSkill(index)"
      class="ml-1 text-xs text-red-300 hover:text-red-200"
    >
      ×
    </button>
  </span>

  <button
    @click="showSkillsModal = true"
    class="w-8 h-8 flex items-center justify-center bg-purple-600/50 hover:bg-purple-600/70 rounded-full text-lg transition-colors"
  >
    +
  </button>
</div>


<!-- Модалка -->
<div v-if="showSkillsModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
  <div class="bg-white dark:bg-zinc-800 p-6 rounded-lg w-[90%] max-w-2xl">
    <h3 class="text-xl font-semibold mb-4">Выберите навыки</h3>
    <div class="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
      <div v-for="(techs, type) in groupedTechnologies" :key="type">
        <h4 class="text-lg font-semibold mb-2">{{ type }}</h4>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tech in techs"
            :key="tech.id"
            @click="addSkill(tech)"
            :disabled="userSkills.some(t => t.id === tech.id)"
            class="px-3 py-1 border rounded-full text-sm hover:bg-purple-500 hover:text-white disabled:opacity-40"
          >
            {{ tech.name }}
          </button>
        </div>
      </div>
    </div>

    <div class="mt-6 flex justify-end gap-2">
      <button
        @click="showSkillsModal = false"
        class="px-4 py-2 bg-zinc-600 rounded hover:bg-zinc-500"
      >
        Отмена
      </button>
    </div>
  </div>
</div>


        </div>
      </div>

      <!-- Модальное окно редактирования профиля -->
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50"
      >
        <div
          class="bg-zinc-800/95 p-6 rounded-lg shadow-lg backdrop-blur-sm w-full max-w-md"
        >
          <h2 class="text-purple-500 text-xl font-bold mb-4">
            Редактировать профиль
          </h2>
          <form
            @submit.prevent="updateProfile"
            class="w-full p-6 border border-purple-400 rounded-lg bg-zinc-800/90 text-white"
          >
            <!-- Поле для загрузки аватара -->
            <div class="form-group mb-4">
              <label class="font-bold text-purple-300">Аватар:</label>
              <div class="flex items-center mt-2">
                <img
                  :src="userData.avatar || randomAvatar"
                  class="w-16 h-16 rounded-full border-2 border-purple-400 mr-3"
                />
                <input
                  type="file"
                  accept="image/*"
                  @change="handleAvatarUpload"
                  class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-500 file:text-white hover:file:bg-purple-600"
                />
              </div>
            </div>

            <div class="form-group mb-4">
              <label for="email" class="font-bold text-purple-300"
                >Email:</label
              >
              <input
                type="email"
                id="email"
                v-model="userData.email"
                required
                class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-700/50"
              />
            </div>

            <div class="form-group mb-4">
              <label for="role" class="font-bold text-purple-300">Роль:</label>
              <select
                id="role"
                v-model="userData.role"
                class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-700/50 text-white"
              >
                <option value="" disabled>Выберите роль</option>
                <option value="Студент">Студент</option>
                <option value="Эксперт">Эксперт</option>
                <option value="Заказчик">Заказчик</option>
              </select>
            </div>

            <div class="form-group mb-4">
              <label for="bio" class="font-bold text-purple-300"
                >Биография:</label
              >
              <textarea
                id="bio"
                v-model="userData.bio"
                maxlength="500"
                rows="4"
                class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-700/50"
                placeholder="Расскажите о себе, своих интересах и опыте"
              ></textarea>
            </div>

            <div class="mb-4">
              <button
                type="button"
                @click="showPasswordFields = !showPasswordFields"
                class="flex items-center text-purple-300 hover:text-purple-200 transition-colors"
              >
                <span>{{
                  showPasswordFields ? "Скрыть" : "Изменить пароль"
                }}</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 ml-1 transition-transform duration-300"
                  :class="{ 'rotate-180': showPasswordFields }"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
            </div>

            <transition name="slide-fade">
              <div v-if="showPasswordFields">
                <div class="form-group mb-4">
                  <label for="password" class="font-bold text-purple-300"
                    >Новый пароль:</label
                  >
                  <div class="relative">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      id="password"
                      v-model="password"
                      @input="validatePasswords"
                      class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-700/50"
                      placeholder="Введите новый пароль"
                    />
                    <button
                      type="button"
                      @click="showPassword = !showPassword"
                      class="absolute right-2 top-2 text-purple-300 hover:text-purple-200"
                      :title="
                        showPassword ? 'Скрыть пароль' : 'Показать пароль'
                      "
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                      </svg>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label for="confirmPassword" class="font-bold text-purple-300"
                    >Подтвердите пароль:</label
                  >
                  <div class="relative">
                    <input
                      :type="showConfirmPassword ? 'text' : 'password'"
                      id="confirmPassword"
                      v-model="confirmPassword"
                      @input="validatePasswords"
                      class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-700/50"
                      placeholder="Повторите новый пароль"
                    />
                    <button
                      type="button"
                      @click="showConfirmPassword = !showConfirmPassword"
                      class="absolute right-2 top-2 text-purple-300 hover:text-purple-200"
                      :title="
                        showConfirmPassword
                          ? 'Скрыть пароль'
                          : 'Показать пароль'
                      "
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                      </svg>
                    </button>
                  </div>
                  <p v-if="passwordError" class="text-red-400 text-xs mt-1">
                    {{ passwordError }}
                  </p>
                </div>
              </div>
            </transition>

            <button
              type="submit"
              class="w-full mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
              :disabled="!formIsValid"
              :class="{
                'opacity-50 cursor-not-allowed': !formIsValid,
                'hover:bg-purple-500': !formIsValid,
              }"
            >
              Сохранить изменения
            </button>
          </form>

          <button
            @click="closeModal"
            class="mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600 w-full transition-colors"
          >
            Закрыть
          </button>
        </div>
      </div>

      <!-- Модальное окно для увеличения аватара -->
      <div
        v-if="showAvatarModal"
        class="fixed inset-0 flex items-center justify-center bg-black/80 backdrop-blur-sm z-50"
        @click="showAvatarModal = false"
      >
        <div class="p-2 max-w-[90vw] max-h-[90vh]">
          <img
            :src="userData.avatar || randomAvatar"
            class="max-w-full max-h-full rounded-lg"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import UserService from "@/composables/storage.js";
import Cookies from "js-cookie";
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth";

export default {
  inject: ["globalState"],
  components: { Header },
  data() {
    return {
      showSkillsModal: false,
    allTechnologies: [], // Все технологии
    groupedTechnologies: {}, // Группировка по типу
    userSkills: [], // ID скиллов пользователя
      userProjects: [],
    userTeams: [],
      currentBgColor: "",
      userData: {
        avatar: "",
        first_name: "",
        last_name: "",
        email: "",
        role: "",
        bio: "",
        group: { id: "", name: "Не указано" },
      },
      showModal: false,
      showAvatarModal: false,
      avatars: Array.from({ length: 6 }, (_, i) => `/ava-${i + 1}.jpg`),
      password: "",
      confirmPassword: "",
      showPassword: false,
      showConfirmPassword: false,
      showPasswordFields: false,
      passwordError: "",
      formIsValid: true,
    };
  },
  computed: {
    passwordMismatch() {
      return this.password && this.password !== this.confirmPassword;
    },
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
  },
  methods: {
    async fetchTechnologies() {
    const res = await api.get('/core/technologies');
    const data = await res.data;

    this.allTechnologies = data;
    this.groupedTechnologies = data.reduce((acc, tech) => {
      if (!acc[tech.type]) acc[tech.type] = [];
      acc[tech.type].push(tech);
      return acc;
    }, {});
  },

  addSkill(tech) {
    if (!this.userSkills.includes(tech)) {
      this.userSkills.push(tech);
    }
  },

  removeSkill(index) {
    this.userSkills.splice(index, 1);
  },
    formatDate(dateStr) {
    if (!dateStr) return 'по настоящее время';
    const date = new Date(dateStr);
    return date.toLocaleString("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  },
async fetchUserActivity(userId) {
  const response = await api.get(`/users/user-activity/?user_id=${userId}`);
  const activityData = response.data;

  const projectIds = activityData
    .filter(item => item.type === 'project' && item.project_id)
    .map(item => ({
      id: item.project_id,
      started_at: item.started_at,
      ended_at: item.ended_at
    }));

  const teamIds = activityData
    .filter(item => item.type === 'team' && item.team_id)
    .map(item => ({
      id: item.team_id,
      started_at: item.started_at,
      ended_at: item.ended_at
    }));

  const projectRequests = projectIds.map(async item => {
    // Получаем данные проекта и участников
    const [projectRes, participantsRes] = await Promise.all([
      api.get(`/projects/${item.id}`),
      api.get(`/projects/${item.id}/participants-details/`)
    ]);

    const projectData = projectRes.data;
    const participants = participantsRes.data;

    // Находим этого пользователя среди участников
const userEntry = [
  ...(participants?.workers || []),
  ...(participants?.teams?.flatMap(team => team.members) || [])
].find(p => p?.user?.id === userId);
    return {
      ...projectData,
      date: item.started_at,
      endDate: item.ended_at,
      averageRating: userEntry?.rating ?? null // используем rating, если есть
    };
  });

  const teamRequests = teamIds.map(async item => {
    const res = await api.get(`/teams/${item.id}`);
    const data = await res.data;
    return {
      ...data,
      joinDate: item.started_at,
      leaveDate: item.ended_at
    };
  });

  const [projects, teams] = await Promise.all([
    Promise.all(projectRequests),
    Promise.all(teamRequests)
  ]);

  this.userProjects = projects;
  this.userTeams = teams;
},
    goToTeam(){
      this.$router.push({ path: "/HSDT/team/1/" });
    },
    getRandomAvatar() {
      const randomIndex = Math.floor(Math.random() * this.avatars.length);
      return this.avatars[randomIndex];
    },
    handleAvatarUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.userData.avatar = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    validatePasswords() {
      if (this.showPasswordFields) {
        if (this.password && this.confirmPassword) {
          if (this.password !== this.confirmPassword) {
            this.passwordError = "Пароли не совпадают";
            this.formIsValid = false;
            return;
          }

          if (this.password.length < 6) {
            this.passwordError = "Пароль должен содержать минимум 6 символов";
            this.formIsValid = false;
            return;
          }
        }

        if (!this.password || !this.confirmPassword) {
          this.passwordError = "Заполните оба поля пароля";
          this.formIsValid = false;
          return;
        }
      }

      this.passwordError = "";
      this.formIsValid = true;
    },
    updateProfile() {
      if (!this.formIsValid) {
        return;
      }

      if (this.password && this.password === this.confirmPassword) {
        console.log("Пароль будет изменён на:", this.password);
      }

      UserService.saveUserData(this.userData);
      alert("Профиль обновлён!");
      this.closeModal();
    },
    closeModal() {
      this.showModal = false;
      this.password = "";
      this.confirmPassword = "";
      this.showPasswordFields = false;
      this.passwordError = "";
      this.formIsValid = true;
    },
    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("userData");
      Cookies.remove("access_token");
      Cookies.remove("refresh_token");
      this.$router.push("/login");
    },
  },
  watch: {
    showPasswordFields(newVal) {
      if (newVal) {
        this.validatePasswords();
      } else {
        this.passwordError = "";
        this.formIsValid = true;
      }
    },
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
  },
  async mounted() {
    this.fetchTechnologies();
    const savedData = await UserService.getUserData();
    this.userData = savedData;
    this.fetchUserActivity(this.userData.id);
  },
};
</script>

<style scoped>
.transform-gpu {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}
.filter {
  filter: blur(8px);
}
.fixed {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}
.bg-zinc-700\/80 {
  background-color: rgba(63, 63, 70, 0.8);
}
.bg-zinc-700\/90 {
  background-color: rgba(63, 63, 70, 0.9);
}
.bg-zinc-800\/50,
.bg-zinc-800\/90,
.bg-zinc-800\/95 {
  background-color: rgba(39, 39, 42, 0.9);
}
.hover\:bg-purple-500:hover {
  background-color: rgb(168, 85, 247);
}
.hover\:bg-red-500:hover {
  background-color: rgb(239, 68, 68);
}
.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Анимации */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
.relative:hover .text-purple-300 {
  color: rgb(192, 132, 252);
}
.rotate-180 {
  transform: rotate(180deg);
}

/* Стили для ошибки */
.text-red-400 {
  color: #f87171;
}

/* Стили для заблокированной кнопки */
.opacity-50 {
  opacity: 0.5;
}
.cursor-not-allowed {
  cursor: not-allowed;
}

/* Новые стили для карточек проектов и команд */
.bg-zinc-600 {
  background-color: rgba(82, 82, 91, 0.7);
}
.bg-green-500 {
  background-color: rgb(34, 197, 94);
}
.bg-blue-500 {
  background-color: rgb(59, 130, 246);
}
.bg-yellow-500 {
  background-color: rgb(234, 179, 8);
}
.text-green-400 {
  color: rgb(74, 222, 128);
}
.text-red-400 {
  color: rgb(248, 113, 113);
}
.text-yellow-400 {
  color: rgb(250, 204, 21);
}
.bg-purple-600\/50 {
  background-color: rgba(147, 51, 234, 0.5);
}

/* Стили для модального окна навыков */
.max-h-\[90vh\] {
  max-height: 90vh;
}
</style>
