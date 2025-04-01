<template>
  <div v-if="!isLoggedIn" class="relative h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <img
      ref="backgroundImage"
      aria-hidden="true"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105"
      src="/bg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />

    <div class="relative h-full overflow-y-auto">
      <h1 class="pt-20 text-white text-9xl text-center font-display">
        ИДЕИ ТИУ
      </h1>
      <div class="w-110 m-auto mt-15">
        <div class="flex flex-col items-center p-10">
          <!-- Поле ввода почты -->
          <div>
            <div class="w-full mb-4">
              <h2 class="text-white mb-1">Почта</h2>
              <input
                v-model="email"
                @input="clearError('email')"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid duration-500 ease-linear transition-colors outline-none"
                :class="{
                  'border-fiolText hover:border-purple-500 focus:border-purple-600':
                    !emailError,
                  'border-red-500': emailError,
                }"
                placeholder="Введите почту..."
              />
              <!-- Сообщение об ошибке -->
              <div
                v-if="emailError"
                class="flex gap-1 text-red-400 text-sm mt-1"
              >
                <img src="/error.svg" alt="Ошибка" />
                {{ emailError }}
              </div>
            </div>
          </div>

          <!-- Поле ввода пароля -->
          <div class="w-full mb-4 flex flex-col">
            <h2 class="text-white mb-1">Пароль</h2>
            <input
              v-model="password"
              @input="clearError('password')"
              type="password"
              class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid duration-500 ease-linear transition-colors outline-none"
              :class="{
                'border-fiol hover:border-purple-500 focus:border-purple-600':
                  !passwordError,
                'border-red-500': passwordError,
              }"
              placeholder="Введите пароль..."
            />
            <div
              v-if="passwordError"
              class="flex gap-1 text-red-400 text-sm mt-1"
            >
              <img src="/error.svg" />
              {{ passwordError }}
            </div>
            <div class="flex justify-end mt-2">
              <button class="text-blue-300 text-sm">Забыли пароль?</button>
            </div>
          </div>

          <button
            @click="login"
            class="bg-purple-500 text-white font-medium w-90 p-2 rounded-lg hover:bg-purple-600 duration-500"
          >
            Войти
          </button>
        </div>
        <div class="w-110 m-auto pl-25 mt-8">
          <button
            @click="goToRegisterZ"
            class="bg-sky-500 text-white font-medium w-60 p-2 rounded-lg hover:bg-sky-600 duration-500"
          >
            Я заказчик
          </button>
        </div>
        <div class="m-auto w-65 mt-3 flex items-center justify-between">
          <h2 class="text-white text-ms">Нет аккаунта?</h2>
          <button
            @click="goToRegister"
            class="text-blue-300 text-ms hover:text-blue-400 duration-500 cursor-pointer"
          >
            Зарегистрироваться
          </button>
        </div>
        <div>
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getUserData, getAccessToken, clearStorage, saveTokens, saveUserData, updateInstitute } from "@/utils/storage.js";
const API_BASE_URL = "http://127.0.0.1:8000/api";
const LOGIN_URL = `${API_BASE_URL}/users/login/`;
const USER_DATA_URL = `${API_BASE_URL}/users/me/`;

export default {
  data() {
    return {
      email: "",
      password: "",
      emailError: "",
      passwordError: "",
      isLoggedIn: false,
      // Параллакс-эффект
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

    clearErrors() {
      this.emailError = "";
      this.passwordError = "";
    },

    checkToken() {
      const accessToken = getAccessToken();
      const selectedInstitute = updateInstitute() || "TYIU";

      if (accessToken) {
        this.isLoggedIn = true;
        this.$router.push(`/${selectedInstitute}/rialto`);
      }
    },

    validateForm() {
      let isValid = true;
      if (!this.email) {
        this.emailError = "Поле почты обязательно для заполнения";
        isValid = false;
      } else if (!this.validateEmail(this.email)) {
        this.emailError = "Некорректный формат почты";
        isValid = false;
      }
      if (!this.password) {
        this.passwordError = "Поле пароля обязательно для заполнения";
        isValid = false;
      }
      return isValid;
    },

    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },

    async login() {
      this.clearErrors();
      if (!this.validateForm()) return;

      try {
        clearStorage();
        const tokens = await this.authenticateUser(this.email, this.password);
        await this.fetchAndSaveUserData(tokens.access_token);
        this.redirectToHome();
      } catch (error) {
        this.handleError(error);
      }
    },

    async authenticateUser(email, password) {
      try {
        const response = await axios.post(LOGIN_URL, { email, password });
        if (!response.data.access_token || !response.data.refresh_token) {
          throw new Error("Токены не получены");
        }
        saveTokens(response.data.access_token, response.data.refresh_token);
        return response.data;
      } catch (error) {
        console.error("Ошибка при аутентификации:", error.response || error);
        throw error;
      }
    },

    async fetchAndSaveUserData(accessToken) {
      try {
        const userData = await this.fetchUserData(accessToken);
        saveUserData(userData);
      } catch (error) {
        console.error("Ошибка при получении данных пользователя:", error);
        throw error;
      }
    },

    async fetchUserData(accessToken) {
      const response = await axios.get(USER_DATA_URL, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });
      return response.data;
    },

    handleError(error) {
      if (error.response) {
        switch (error.response.data?.message) {
          case "Invalid credentials":
            this.passwordError = "Неверный email или пароль";
            break;
          case "Email not found":
            this.emailError = "Данная почта не зарегистрирована";
            break;
          default:
            this.passwordError = error.response.data.message || "Ошибка при входе";
        }
      } else if (error.request) {
        this.passwordError = "Ошибка соединения с сервером";
      } else {
        this.passwordError = "Произошла непредвиденная ошибка";
      }
    },

    redirectToHome() {
      const institute = getInstitute() || "TYIU";
      this.$router.push(`/${institute}/rialto`);
    },

    goToRegister() {
      this.$router.push("/register");
    },

    goToRegisterZ() {
      this.$router.push("/registerZ");
    },
  },

  mounted() {
    this.checkToken();
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

.h-screen {
  height: 100vh;
}

/* Остальные стили */
.max-h-48 {
  max-height: 12rem;
}

.overflow-y-auto {
  overflow-y: auto;
}

.cursor-pointer {
  cursor: pointer;
}

.hover\:bg-gray-200:hover {
  background-color: #edf2f7;
}
</style>
