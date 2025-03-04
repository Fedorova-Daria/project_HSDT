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
      </div>
      <!-- Остальная часть шаблона без изменений -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
    clearError(field) {
      if (field === "email") this.emailError = "";
      if (field === "password") this.passwordError = "";
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
      // Сброс предыдущих ошибок
      this.emailError = "";
      this.passwordError = "";

      // Валидация формы
      if (!this.validateForm()) return;

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/users/login/",
          {
            email: this.email,
            password: this.password,
          }
        );

        // Проверка на успешный вход
        if (response.data.success === true) {
          this.$router.push("/rialto");
        } else {
          // Если success === false, отображаем сообщение об ошибке
          if (response.data.message === "Invalid credentials") {
            this.passwordError = "Неверный email или пароль";
          } else if (response.data.message === "Email not found") {
            this.emailError = "Данная почта не зарегистрирована";
          } else {
            this.passwordError = "Произошла ошибка при входе";
          }
        }
      } catch (error) {
        console.error("Ошибка входа", error);

        // Обработка ошибок сети или сервера
        if (error.response) {
          // Ошибки от сервера (например, 400, 500)
          if (error.response.data && error.response.data.message) {
            if (error.response.data.message === "Invalid credentials") {
              this.passwordError = "Неверный email или пароль";
            } else if (error.response.data.message === "Email not found") {
              this.emailError = "Данная почта не зарегистрирована";
            } else {
              this.passwordError = error.response.data.message;
            }
          } else {
            this.passwordError = "Произошла ошибка при входе";
          }
        } else if (error.request) {
          // Ошибки сети (нет ответа от сервера)
          this.passwordError = "Ошибка соединения с сервером";
        } else {
          // Другие ошибки
          this.passwordError = "Произошла непредвиденная ошибка";
        }
      }
    },

    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>
