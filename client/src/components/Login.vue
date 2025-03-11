<template>
  <div>
    <img
      aria-hidden="true"
      class="absolute top-0 h-screen w-screen bg-cover bg-center bg-fixed"
      src="/bg.jpg"
    />
    <div class="relative">
      <h1 class="mt-20 text-white text-9xl text-center font-display">
        Портал ВШЦТ
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
                  'border-fiol hover:border-purple-500 focus:border-purple-600':
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
            class="bg-sky-500 text-white font-medium w-60 p-2 rounded-lg hover:bg-sky-600 duration-500"
          >
            Я заказчик
          </button>
        </div>
        <div class="m-auto w-65 mt-3 flex items-center justify-between">
          <h2 class="text-white text-ms">Нет аккаунта?</h2>
          <button
            @click="goToRegister"
            class="text-blue-300 text-ms hover:text-blue-400 duration-500"
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
import {
  saveUserData,
  saveTokens,
  clearStorage,
} from "@/utils/localStorage.js"; // Предположим, что функции находятся в отдельном файле

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
    };
  },

  methods: {
    // Очистка ошибок
    clearErrors() {
      this.emailError = "";
      this.passwordError = "";
    },

    // Валидация формы
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

    // Валидация email
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },

    // Основной метод для входа
    async login() {
      this.clearErrors();

      if (!this.validateForm()) return;

      try {
        // Очищаем localStorage перед входом
        clearStorage();

        // Аутентификация пользователя
        const tokens = await this.authenticateUser(this.email, this.password);

        // Получаем и сохраняем данные пользователя
        await this.fetchAndSaveUserData(tokens.access_token);

        // Перенаправляем пользователя на главную страницу
        this.redirectToHome();
      } catch (error) {
        // Обрабатываем ошибки
        this.handleError(error);
      }
    },

    // Метод для аутентификации пользователя
    async authenticateUser(email, password) {
      try {
        const response = await axios.post(LOGIN_URL, { email, password });
        console.log("Ответ сервера:", response.data); // Логируем ответ

        if (!response.data.access_token || !response.data.refresh_token) {
          throw new Error("Токены не получены");
        }

        // Используем вашу функцию для сохранения токенов
        saveTokens(response.data.access_token, response.data.refresh_token);

        return response.data;
      } catch (error) {
        console.error("Ошибка при аутентификации:", error.response || error); // Логируем ошибку
        throw error;
      }
    },

    // Метод для получения и сохранения данных пользователя
    async fetchAndSaveUserData(accessToken) {
      try {
        const userData = await this.fetchUserData(accessToken);
        console.log("Данные пользователя:", userData); // Логируем данные пользователя

        // Используем вашу функцию для сохранения данных пользователя
        saveUserData(userData);
      } catch (error) {
        console.error("Ошибка при получении данных пользователя:", error); // Логируем ошибку
        throw error;
      }
    },

    // Метод для получения данных пользователя
    async fetchUserData(accessToken) {
      const response = await axios.get(USER_DATA_URL, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });

      return response.data;
    },

    // Метод для обработки ошибок
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
            this.passwordError =
              error.response.data.message || "Произошла ошибка при входе";
        }
      } else if (error.request) {
        this.passwordError = "Ошибка соединения с сервером";
      } else {
        this.passwordError = "Произошла непредвиденная ошибка";
      }
    },

    // Метод для перенаправления на главную страницу
    redirectToHome() {
      this.$router.push("/rialto");
    },

    // Метод для перехода на страницу регистрации
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>
