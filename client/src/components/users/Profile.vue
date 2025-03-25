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

    <!-- Затемнение фона (увеличена прозрачность) -->
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
              class="w-32 h-32 rounded-full border-4 border-purple-400 mx-auto"
              :src="userData.avatar || 'https://via.placeholder.com/150'"
              alt="Аватар пользователя"
            />
            <h1
              v-if="userData.first_name && userData.last_name"
              class="text-2xl font-semibold mt-4"
            >
              {{ userData.first_name }} {{ userData.last_name }}
            </h1>
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
          <!-- Кнопка для открытия модального окна -->
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
            <div>
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">Проекты</h3>
              <div class="mt-2">
                <table
                  class="w-full border-collapse shadow-lg rounded-lg overflow-hidden"
                >
                  <thead class="bg-zinc-800">
                    <tr>
                      <th class="p-3 text-left text-white">Название</th>
                      <th class="p-3 text-left text-white">Статус</th>
                      <th class="p-3 text-left text-white">Оценка</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="bg-zinc-600 transition-colors">
                      <td class="p-3 border-t border-zinc-200">
                        Проект "Паровозик" (пример)
                      </td>
                      <td class="p-3 border-t border-zinc-200">Окончено</td>
                      <td class="p-3 border-t border-zinc-200">5</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <!-- Стек технологий -->

            <div>
              <h3 class="text-xl font-semibold border-b pb-2 mb-3">
                Стеки технологий
              </h3>
              <ul>
                <li class="p-2 bg-gray-700 rounded-md mb-2"></li>
              </ul>
              <p>Нет командной активности</p>
            </div>
          </div>
          <!-- Команды -->
          <h3 class="mt-10 text-xl font-semibold border-b pb-2 mb-3">
            Команды
          </h3>
          <div class="mt-2">
            <table
              class="w-full border-collapse shadow-lg rounded-lg overflow-hidden"
            >
              <thead class="bg-border">
                <tr>
                  <th class="p-3 text-left text-white">Название команды</th>
                  <th class="p-3 text-left text-white">Дата вступления</th>
                  <th class="p-3 text-left text-white">Дата ухода</th>
                </tr>
              </thead>
              <tbody>
                <tr class="bg-zinc-600 transition-colors">
                  <td class="p-3 border-t border-zinc-200"></td>
                  <td class="p-3 border-t border-zinc-200"></td>
                  <td class="p-3 border-t border-zinc-200"></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Модальное окно -->
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50"
      >
        <div class="bg-zinc-700/90 p-6 rounded-lg shadow-lg backdrop-blur-sm">
          <h2 class="text-purple-500 text-xl font-bold mb-4">
            Редактировать профиль
          </h2>
          <form
            @submit.prevent="updateProfile"
            class="w-full max-w-md p-6 border border-purple-400 rounded-lg bg-zinc-700/90 text-white"
          >
            <div class="form-group mb-4">
              <label for="email" class="font-bold text-purple-300"
                >Email:</label
              >
              <input
                type="email"
                id="email"
                v-model="userData.email"
                required
                class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-800/50"
              />
            </div>
            <div class="form-group mb-4">
              <label for="bio" class="font-bold text-purple-300"
                >Немного о себе:</label
              >
              <textarea
                id="bio"
                v-model="userData.bio"
                maxlength="40"
                class="mt-1 block w-full p-2 border border-purple-400 rounded bg-zinc-800/50"
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
            class="mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600 w-full"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import { saveUserData, getUserData } from "@/utils/localStorage.js";

export default {
  components: { Header },
  data() {
    return {
      userData: {
        avatar: "https://via.placeholder.com/150",
        first_name: "",
        last_name: "",
        email: "",
        group: { id: "", name: "Не указано" },
      },
      showModal: false,
      // Данные для параллакс-эффекта
      offsetX: 0,
      offsetY: 0,
      targetX: 0,
      targetY: 0,
      mouseX: 0,
      mouseY: 0,
      windowWidth: 0,
      windowHeight: 0,
      animationFrame: null,
    };
  },
  methods: {
    // Инициализация параллакс-эффекта
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

      // Вычисляем смещение относительно центра экрана (от -1 до 1)
      const x = (e.clientX / this.windowWidth - 0.5) * 2;
      const y = (e.clientY / this.windowHeight - 0.5) * 2;

      // Устанавливаем целевые координаты с коэффициентом
      const coefficient = 30;
      this.targetX = x * coefficient;
      this.targetY = y * coefficient;
    },

    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },

    animate() {
      // Интерполяция с коэффициентом плавности
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

    updateProfile() {
      saveUserData(this.userData);
      alert("Профиль обновлён!");
      this.showModal = false;
    },

    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("userData");
      this.$router.push("/login");
    },
  },
  async mounted() {
    this.userData = await getUserData();
    console.log("Данные из localStorage:", this.userData);
    this.initParallax();
  },
  beforeDestroy() {
    this.cleanupParallax();
  },
};
</script>

<style scoped>
/* Стили для параллакс-эффекта */
.transform-gpu {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

.filter {
  filter: blur(8px);
}

/* Стили для модального окна */
.fixed {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}

/* Общие стили для карточек */
.bg-zinc-700\/80 {
  background-color: rgba(63, 63, 70, 0.8);
}

.bg-zinc-700\/90 {
  background-color: rgba(63, 63, 70, 0.9);
}

.bg-zinc-800\/50 {
  background-color: rgba(39, 39, 42, 0.5);
}

/* Эффекты при наведении */
.hover\:bg-purple-500:hover {
  background-color: rgb(168, 85, 247);
}

.hover\:bg-red-500:hover {
  background-color: rgb(239, 68, 68);
}

/* Тени */
.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>
