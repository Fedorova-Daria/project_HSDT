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
              <h2 class="text-always-white mb-1">Почта</h2>
              <input
                v-model="email"
                @input="clearError('email')"
                class="m-auto w-90 bg-white text-always-black px-2 py-2 rounded-lg border-3 border-solid duration-500 ease-linear transition-colors outline-none"
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
            <h2 class="text-always-white mb-1">Пароль</h2>
            <input
              v-model="password"
              @input="clearError('password')"
              type="password"
              class="m-auto w-90 bg-white text-always-black px-2 py-2 rounded-lg border-3 border-solid duration-500 ease-linear transition-colors outline-none"
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
            @click="asyncLogin"
            class="bg-purple-500 text-always-white font-medium w-90 p-2 rounded-lg hover:bg-purple-600 duration-500"
          >
            Войти
          </button>
        </div>
        <div class="w-110 m-auto pl-25 mt-8">
          <button
            @click="goToRegisterZ"
            class="bg-sky-500 text-always-white font-medium w-60 p-2 rounded-lg hover:bg-sky-600 duration-500"
          >
            Я заказчик
          </button>
        </div>
        <div class="m-auto w-65 mt-3 flex items-center justify-between">
          <h2 class="text-white text-ms">Нет аккаунта?</h2>
          <button
  @click="goToRegister"
  :style="{
    color: 'rgb(56, 189, 248) !important', 
    hover: 'rgb(37, 99, 235) !important'
  }"
  class="duration-500 cursor-pointer"
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
import { useAuth } from "@/composables/useAuth"; // Импортируем useAuth
import Cookies from "js-cookie";
import { nextTick } from "vue";

export default {
  name: "LoginPage",
  data() {
    return {
      authCheck: false,
      email: "",
      password: "",
      emailError: "",
      passwordError: "",
      // Данные для параллакс-эффекта
      offsetX: 0,
      offsetY: 0,
      targetX: 0,
      targetY: 0,
      mouseX: 0,
      mouseY: 0,
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      animationFrame: null,
    };
  },
  computed: {
    isLoggedIn() {
    const access = Cookies.get("access_token");
    const refresh = Cookies.get("refresh_token");

    console.log("Текущие токены:", access, refresh);

    return this.authCheck || !!(access && access !== "undefined" && refresh && refresh !== "undefined");
  }
  },
  created() {
    // Если пользователь уже авторизован, то сразу редиректим его на целевую страницу
    if (this.isLoggedIn) {
      this.$router.push("/TYIU/about");
    }
  },
  methods: {
    goToRegisterZ() {
      this.$router.push({ path: "/registerZ" });
    },
    goToRegister() {
      this.$router.push({ path: "/register" });
    },
    /**
     * Способ входа. Вызывается при клике по кнопке входа.
     */
     async asyncLogin() {
  this.clearError("email");
  this.clearError("password");

  if (!this.validateForm()) return;

  try {
    const { login } = useAuth();
    await login(this.email, this.password);

    console.log("Токены после логина:", Cookies.get("access_token"), Cookies.get("refresh_token"));

    // Принудительно обновляем состояние авторизации
    this.authCheck = true;

    console.log("Авторизация успешна. Перенаправление...");
    this.$router.push("/TYIU/about");

  } catch (error) {
    this.handleError(error);
  }
},
    validateForm() {
      let isValid = true;
      if (!this.email) {
        this.emailError = "Поле почты обязательно для заполнения!";
        isValid = false;
      } else if (!this.validateEmail(this.email)) {
        this.emailError = "Некорректный формат почты";
        isValid = false;
      }
      if (!this.password) {
        this.passwordError = "Поле пароля обязательно для заполнения!";
        isValid = false;
      }
      return isValid;
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    clearError(field) {
      if (field === "email") this.emailError = "";
      if (field === "password") this.passwordError = "";
    },
    handleError(error) {
      if (error.response?.data?.message) {
        const msg = error.response.data.message;
        if (msg === "Invalid credentials") {
          this.passwordError = "Неверный email или пароль";
        } else if (msg === "Email not found") {
          this.emailError = "Почта не найдена";
        } else {
          this.passwordError = msg;
        }
      } else {
        this.passwordError = "Ошибка при входе, попробуйте позже";
      }
    },
    // Методы для параллакс-эффекта:
    initParallax() {
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
      // Используем стрелочную функцию, чтобы сохранить контекст this
      this.animationFrame = requestAnimationFrame(() => this.animate());
    },
    cleanupParallax() {
      window.removeEventListener("mousemove", this.handleMouseMove);
      window.removeEventListener("resize", this.handleResize);
      if (this.animationFrame) {
        cancelAnimationFrame(this.animationFrame);
      }
    },
  },
  mounted() {
    //this.initParallax();
    console.log("LoginPage mounted");
  },
  beforeDestroy() {
    //this.cleanupParallax();
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
