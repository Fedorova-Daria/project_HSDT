<template>
  <div class="relative min-h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <img
      ref="backgroundImage"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105 -z-10"
      src="/bgg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />

    <!-- Затемнение фона -->
    <div class="absolute inset-0 bg-black opacity-60 -z-10"></div>

    <div class="min-h-screen text-white flex flex-col relative z-10">
      <!-- Хедер -->
      <Header />

      <!-- Основной контейнер профиля -->
      <div class="flex w-4/5 mx-auto mt-10 gap-6">
        <!-- Левый блок (Информация о пользователе) -->
        <div
          class="w-1/4 bg-zinc-700/80 p-6 rounded-2xl shadow-lg backdrop-blur-sm"
        >
          <div class="text-center">
            <img
              class="w-32 h-32 rounded-full border-4 border-purple-400 mx-auto cursor-pointer hover:border-purple-300 transition-colors"
              :src="userData.avatar || randomAvatar"
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

          <div class="mt-5">
            <p class="text-sm flex justify-between text-white">
              <strong>Почта:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-zinc-700/50 text-white text-sm rounded-lg p-2.5 border border-zinc-600"
            >
              {{ userData.email || "Не указано" }}
            </div>
            <p class="text-sm mt-2 flex justify-between text-white">
              <strong>Группа:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-zinc-700/50 text-white text-sm rounded-lg p-2.5 border border-zinc-600"
            >
              {{ userData.group?.name || "Не указано" }}
            </div>
          </div>

          <!-- Блок биографии -->
          <div class="mt-5">
            <p class="text-sm flex justify-between text-white">
              <strong>Биография:</strong>
            </p>
            <div
              class="w-auto mt-2 bg-zinc-700/50 text-white text-sm rounded-lg p-2.5 border border-zinc-600 min-h-[100px]"
            >
              {{ userData.bio || "Пока ничего не рассказал о себе" }}
            </div>
          </div>

          <button
            @click="showModal = true"
            class="w-full mt-4 py-2 bg-purple-600 text-white rounded-lg transition duration-300 hover:bg-purple-500 hover:shadow-lg"
          >
            Редактировать профиль
          </button>
          <button
            @click="logout"
            class="w-full mt-2 py-2 bg-red-600 text-white rounded-lg transition duration-300 hover:bg-red-500 hover:shadow-lg"
          >
            Выйти
          </button>
        </div>

        <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
        <div
          class="w-3/4 bg-zinc-700/80 p-6 rounded-2xl shadow-lg backdrop-blur-sm"
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
                  class="mb-4 p-4 bg-zinc-600 rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ project.name }}</h4>
                    <span
                      :class="{
                        'bg-green-500': project.status === 'Завершен',
                        'bg-blue-500': project.status === 'В работе',
                        'bg-yellow-500': project.status === 'Заморожен',
                      }"
                      class="px-2 py-1 rounded-full text-xs text-white"
                    >
                      {{ project.status }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-300 mt-1">
                    {{ project.description }}
                  </p>
                  <div class="mt-2 flex justify-between items-center">
                    <div>
                      <span class="text-sm">Оценка: </span>
                      <span class="font-bold">{{ project.grade }}/10</span>
                    </div>
                    <div>
                      <span class="text-sm">{{ project.date }}</span>
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
                  class="mb-4 p-4 bg-zinc-600 rounded-lg"
                >
                  <div class="flex justify-between items-start">
                    <h4 class="font-medium text-lg">{{ team.name }}</h4>
                    <span class="text-sm text-gray-300"
                      >{{ team.members }} участников</span
                    >
                  </div>
                  <div class="mt-2">
                    <p class="text-sm">
                      <span class="font-medium">Проекты:</span>
                      {{ team.projects.join(", ") }}
                    </p>
                    <p class="text-sm mt-1">
                      <span class="font-medium">Статус команды:</span>
                      <span
                        :class="{
                          'text-green-400': team.teamStatus === 'Активна',
                          'text-red-400': team.teamStatus === 'Распущена',
                          'text-yellow-400': team.teamStatus === 'Заморожена',
                        }"
                      >
                        {{ team.teamStatus }}
                      </span>
                    </p>
                    <div class="mt-2 text-sm">
                      <p>
                        Участие: с {{ team.joinDate }} по
                        {{ team.leaveDate || "настоящее время" }}
                      </p>
                    </div>
                    <button
                      class="mt-2 text-purple-300 hover:text-purple-200 text-sm flex items-center"
                    >
                      <span>Подробнее о команде</span>
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

          <!-- Навыки -->
          <h3 class="mt-10 text-xl font-semibold border-b pb-2 mb-3">Навыки</h3>
          <div class="flex flex-wrap gap-2 mt-4">
            <span
              v-for="(tech, index) in userTechStack"
              :key="index"
              class="px-3 py-1 bg-purple-600/50 rounded-full text-sm flex items-center"
            >
              {{ tech.name || tech }}
              <button
                v-if="typeof tech === 'object'"
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

      <!-- Модальное окно выбора навыков -->
      <div
        v-if="showSkillsModal"
        class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50"
      >
        <div
          class="bg-zinc-800/95 p-6 rounded-lg shadow-lg backdrop-blur-sm w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        >
          <h2 class="text-purple-500 text-xl font-bold mb-4">
            Добавить навыки
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="category in skillCategories"
              :key="category.name"
              class="border border-zinc-600 rounded-lg p-3"
            >
              <h3 class="font-bold text-purple-300 mb-2">
                {{ category.name }}
              </h3>
              <div class="space-y-2">
                <div v-if="category.subskills">
                  <div
                    v-for="subskill in category.subskills"
                    :key="subskill"
                    class="flex items-center"
                  >
                    <input
                      type="checkbox"
                      :id="`skill-${category.name}-${subskill}`"
                      :value="{ category: category.name, name: subskill }"
                      v-model="selectedSkills"
                      class="mr-2 rounded text-purple-500 focus:ring-purple-400"
                    />
                    <label
                      :for="`skill-${category.name}-${subskill}`"
                      class="text-sm"
                    >
                      {{ subskill }}
                    </label>
                  </div>
                </div>
                <div class="flex items-center pt-2 border-t border-zinc-600">
                  <input
                    type="checkbox"
                    :id="`skill-${category.name}`"
                    :value="category.name"
                    v-model="selectedSkills"
                    class="mr-2 rounded text-purple-500 focus:ring-purple-400"
                  />
                  <label
                    :for="`skill-${category.name}`"
                    class="text-sm font-medium"
                  >
                    {{ category.name }} (общее направление)
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              @click="showSkillsModal = false"
              class="px-4 py-2 bg-zinc-600 text-white rounded hover:bg-zinc-500 transition-colors"
            >
              Отмена
            </button>
            <button
              @click="addSelectedSkills"
              class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
            >
              Добавить выбранные ({{ selectedSkills.length }})
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import { saveUserData, getUserData } from "@/api/storage.js";

export default {
  components: { Header },
  data() {
    return {
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
      offsetX: 0,
      offsetY: 0,
      targetX: 0,
      targetY: 0,
      mouseX: 0,
      mouseY: 0,
      windowWidth: 0,
      windowHeight: 0,
      animationFrame: null,
      avatars: Array.from({ length: 6 }, (_, i) => `/ava-${i + 1}.jpg`),
      randomAvatar: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
      showConfirmPassword: false,
      showPasswordFields: false,
      passwordError: "",
      formIsValid: true,
      userProjects: [
        {
          name: "Паровозик",
          description: "Система управления железнодорожными перевозками",
          status: "Завершен",
          grade: 9,
          date: "15.03.2022 - 20.06.2022",
        },
        {
          name: "Флора",
          description: "Приложение для идентификации растений",
          status: "В работе",
          grade: "-",
          date: "10.01.2023 - настоящее время",
        },
        {
          name: "Космос",
          description: "AR-приложение для изучения астрономии",
          status: "Заморожен",
          grade: 7,
          date: "05.09.2021 - 12.12.2021",
        },
      ],
      userTeams: [
        {
          name: "Технократы",
          members: 5,
          projects: ["Паровозик", "Космос"],
          teamStatus: "Распущена",
          joinDate: "10.02.2021",
          leaveDate: "25.06.2022",
        },
        {
          name: "Зеленый патруль",
          members: 4,
          projects: ["Флора"],
          teamStatus: "Активна",
          joinDate: "05.01.2023",
          leaveDate: null,
        },
      ],
      showSkillsModal: false,
      selectedSkills: [],
      skillCategories: [
        {
          name: "IT навыки",
          subskills: [
            "Frontend разработка",
            "Backend разработка",
            "Мобильная разработка",
            "DevOps",
            "UI/UX дизайн",
            "Тестирование",
            "Базы данных",
          ],
        },
        {
          name: "Строительные навыки",
          subskills: [
            "Кровельные работы",
            "Отделочные работы",
            "Электромонтаж",
            "Сантехника",
            "Фундаментные работы",
            "Каменная кладка",
            "Плотницкие работы",
          ],
        },
        {
          name: "Архитектурные",
          subskills: [
            "3D моделирование",
            "Черчение",
            "Ландшафтный дизайн",
            "Интерьерный дизайн",
            "Визуализация",
            "Проектирование",
            "Строительные нормы",
          ],
        },
        {
          name: "Дизайн",
          subskills: [
            "Графический дизайн",
            "Веб-дизайн",
            "Иллюстрация",
            "Анимация",
            "Типографика",
            "Брендинг",
            "Фотография",
          ],
        },
        {
          name: "Маркетинг",
          subskills: [
            "SMM",
            "Контент-маркетинг",
            "SEO",
            "Аналитика",
            "Копирайтинг",
            "Таргетированная реклама",
            "PR",
          ],
        },
        {
          name: "Менеджмент",
          subskills: [
            "Управление проектами",
            "Управление командой",
            "Финансовый менеджмент",
            "Аналитика данных",
            "Стратегическое планирование",
            "Управление продуктом",
            "Agile методологии",
          ],
        },
        {
          name: "Иностранные языки",
          subskills: [
            "Английский",
            "Немецкий",
            "Французский",
            "Китайский",
            "Испанский",
            "Японский",
            "Итальянский",
          ],
        },
      ],
      userTechStack: [
        "Дизайн",
        { category: "IT навыки", name: "Frontend разработка" },
        { category: "Строительные навыки", name: "Отделочные работы" },
      ],
    };
  },
  computed: {
    passwordMismatch() {
      return this.password && this.password !== this.confirmPassword;
    },
  },
  methods: {
    initParallax() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
      window.addEventListener("mousemove", this.handleMouseMove);
      window.addEventListener("resize", this.handleResize);
      this.animate();
    },
    handleMouseMove(e) {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
      const x = (e.clientX / this.windowWidth - 0.5) * 2;
      const y = (e.clientY / this.windowHeight - 0.5) * 2;
      const coefficient = 30;
      this.targetX = x * coefficient;
      this.targetY = y * coefficient;
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    animate() {
      const smoothness = 0.08;
      this.offsetX += (this.targetX - this.offsetX) * smoothness;
      this.offsetY += (this.targetY - this.offsetY) * smoothness;
      this.animationFrame = requestAnimationFrame(this.animate);
    },
    cleanupParallax() {
      window.removeEventListener("mousemove", this.handleMouseMove);
      window.removeEventListener("resize", this.handleResize);
      if (this.animationFrame) {
        cancelAnimationFrame(this.animationFrame);
      }
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

      saveUserData(this.userData);
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
      this.$router.push("/login");
    },
    addSelectedSkills() {
      // Фильтруем, чтобы не добавлять дубликаты
      const newSkills = this.selectedSkills.filter((skill) => {
        if (typeof skill === "string") {
          return !this.userTechStack.includes(skill);
        } else {
          return !this.userTechStack.some(
            (s) =>
              typeof s === "object" &&
              s.category === skill.category &&
              s.name === skill.name
          );
        }
      });

      this.userTechStack = [...this.userTechStack, ...newSkills];
      this.selectedSkills = [];
      this.showSkillsModal = false;

      // Сохраняем изменения
      saveUserData({
        ...this.userData,
        skills: this.userTechStack,
      });
    },
    removeSkill(index) {
      this.userTechStack.splice(index, 1);
      // Сохраняем изменения
      saveUserData({
        ...this.userData,
        skills: this.userTechStack,
      });
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
  },
  async mounted() {
    const savedData = await getUserData();
    this.userData = savedData;
    if (savedData.skills) {
      this.userTechStack = savedData.skills;
    }
    this.randomAvatar = this.getRandomAvatar();
    this.initParallax();
  },
  beforeDestroy() {
    this.cleanupParallax();
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
