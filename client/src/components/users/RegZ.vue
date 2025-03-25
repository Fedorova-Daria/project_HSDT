<template>
  <div class="relative h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <img
      ref="backgroundImage"
      alt="background"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105"
      src="/bgg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />

    <!-- Затемнение фона -->
    <div class="absolute inset-0 bg-black opacity-30 z-10"></div>

    <!-- Кнопка возврата -->
    <button
      @click="goBack"
      class="absolute top-5 left-5 z-30 bg-purple-500 text-white p-2 rounded-lg hover:bg-purple-600 transition duration-300 flex items-center justify-center"
      aria-label="Вернуться назад"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 19l-7-7m0 0l7-7m-7 7h18"
        />
      </svg>
    </button>

    <!-- Основной контент -->
    <div class="relative z-20 h-full overflow-y-auto">
      <div class="relative w-4/5 mx-auto pt-15 pb-10">
        <h1 class="text-white text-8xl text-center font-display">
          Регистрация Заказчика
        </h1>
        <div class="w-110 mx-auto mt-10">
          <div class="flex flex-col items-center p-10">
            <!-- Поля формы -->
            <div class="w-full mb-4">
              <h2 class="text-white mb-1">Имя</h2>
              <input
                v-model="first_name"
                @input="validateForm"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите имя..."
              />
            </div>
            <div class="w-full mb-4 flex flex-col">
              <h2 class="text-white mb-1">Фамилия</h2>
              <input
                v-model="last_name"
                @input="validateForm"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите фамилию..."
              />
            </div>
            <div class="w-full mb-4 flex flex-col">
              <h2 class="text-white mb-1">Почта</h2>
              <input
                v-model="email"
                @blur="validateEmail"
                @input="validateForm"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите почту..."
              />
              <span v-if="emailError" class="text-red-500 text-sm mt-1">{{
                emailError
              }}</span>
            </div>
            <div class="w-full mb-4 flex flex-col">
              <h2 class="text-white mb-1">Юридическое имя(ИП/ООО)</h2>
              <input
                v-model="Company"
                @input="validateForm"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите юридическое имя..."
              />
            </div>
            <!-- Поле Пароля -->
            <div class="w-full mb-4 relative">
              <h2 class="text-white mb-1">Пароль</h2>
              <div class="relative">
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  @input="validatePassword"
                  class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none pr-10"
                  placeholder="Введите пароль..."
                />
                <button
                  @click="toggleShowPassword"
                  type="button"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 focus:outline-none"
                >
                  <span v-if="showPassword">👁️</span>
                  <span v-else>👁️‍🗨️</span>
                </button>
              </div>
              <div v-if="passwordError" class="text-red-500 text-sm mt-1">
                {{ passwordError }}
              </div>
              <div
                v-if="passwordStrength"
                class="text-xs mt-1"
                :class="{
                  'text-red-500': passwordStrength === 'weak',
                  'text-yellow-500': passwordStrength === 'medium',
                  'text-green-500': passwordStrength === 'strong',
                }"
              >
                Надёжность пароля:
                {{
                  passwordStrength === "weak"
                    ? "Слабая"
                    : passwordStrength === "medium"
                    ? "Средняя"
                    : "Сильная"
                }}
              </div>
            </div>

            <!-- Поле Подтверждения пароля -->
            <div class="w-full mb-4 relative">
              <h2 class="text-white mb-1">Подтвердите пароль</h2>
              <div class="relative">
                <input
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  @input="validateConfirmPassword"
                  class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none pr-10"
                  placeholder="Повторите пароль..."
                />
                <button
                  @click="toggleShowConfirmPassword"
                  type="button"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 focus:outline-none"
                >
                  <span v-if="showConfirmPassword">👁️</span>
                  <span v-else>👁️‍🗨️</span>
                </button>
              </div>
              <span
                v-if="confirmPasswordError"
                class="text-red-500 text-sm mt-1"
                >{{ confirmPasswordError }}</span
              >
            </div>

            <button
              @click="registerUser"
              :disabled="!isFormValid"
              class="bg-purple-500 mt-4 text-white font-medium w-90 h-12 p-2 rounded-lg hover:bg-purple-600 duration-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Зарегистрироваться
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      Company: "",
      email: "",
      password: "",
      confirmPassword: "",
      role: "ST",
      showPassword: false,
      showConfirmPassword: false,
      emailError: "",
      passwordError: "",
      confirmPasswordError: "",
      passwordStrength: "",
      isFormValid: false,
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
  mounted() {
    // Инициализация параллакс-эффекта
    this.windowWidth = window.innerWidth;
    this.windowHeight = window.innerHeight;
    window.addEventListener("mousemove", this.handleMouseMove);
    window.addEventListener("resize", this.handleResize);
    this.animate();

    // Остальная инициализация...
  },
  beforeDestroy() {
    window.removeEventListener("mousemove", this.handleMouseMove);
    window.removeEventListener("resize", this.handleResize);
    cancelAnimationFrame(this.animationFrame);
  },
  methods: {
    // Методы параллакс-эффекта
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
    goBack() {
      this.$router.go(-1);
    },

    // Остальные методы формы
    toggleShowPassword() {
      this.showPassword = !this.showPassword;
    },
    toggleShowConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.emailError = "Поле email обязательно";
      } else if (!emailRegex.test(this.email)) {
        this.emailError = "Введите корректный email";
      } else {
        this.emailError = "";
      }
      this.validateForm();
    },
    validatePassword() {
      if (!this.password) {
        this.passwordError = "Поле пароля обязательно";
        this.passwordStrength = "";
        return;
      }

      if (this.password.length < 8) {
        this.passwordError = "Пароль должен содержать минимум 8 символов";
        this.passwordStrength = "weak";
        return;
      }

      const hasUpperCase = /[A-Z]/.test(this.password);
      const hasLowerCase = /[a-z]/.test(this.password);
      const hasNumbers = /\d/.test(this.password);
      const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(this.password);

      let strength = 0;
      if (hasUpperCase) strength++;
      if (hasLowerCase) strength++;
      if (hasNumbers) strength++;
      if (hasSpecialChars) strength++;

      if (strength < 2) {
        this.passwordStrength = "weak";
      } else if (strength < 4) {
        this.passwordStrength = "medium";
      } else {
        this.passwordStrength = "strong";
      }

      this.passwordError = "";
      this.validateForm();
    },
    validateConfirmPassword() {
      if (!this.confirmPassword) {
        this.confirmPasswordError = "Подтвердите пароль";
      } else if (this.password !== this.confirmPassword) {
        this.confirmPasswordError = "Пароли не совпадают";
      } else {
        this.confirmPasswordError = "";
      }
      this.validateForm();
    },
    validateForm() {
      this.isFormValid =
        this.first_name &&
        this.last_name &&
        this.Company &&
        this.email &&
        !this.emailError &&
        this.password &&
        !this.passwordError &&
        this.confirmPassword &&
        !this.confirmPasswordError &&
        this.password === this.confirmPassword;
    },
    async registerUser() {
      if (!this.isFormValid) {
        alert("Пожалуйста, заполните все поля корректно.");
        return;
      }

      const data = {
        first_name: this.first_name,
        last_name: this.last_name,
        company: this.Company,
        email: this.email,
        password: this.password,
        role: this.role,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/users/registration/",
          data
        );

        if (response.status === 201) {
          const userData = {
            first_name: this.first_name,
            last_name: this.last_name,
            company: this.Company,
            email: this.email,
            role: this.role,
          };

          localStorage.setItem("userData", JSON.stringify(userData));
          this.$router.push("/login");
        }
      } catch (error) {
        console.error("Ошибка при отправке данных:", error);
        if (error.response?.data?.email) {
          this.emailError = "Пользователь с таким email уже существует";
        } else {
          alert("Ошибка при регистрации. Проверьте введённые данные.");
        }
      }
    },
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

/* Стили для кнопки возврата */
button[aria-label="Вернуться назад"] {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

button[aria-label="Вернуться назад"]:hover {
  transform: translateX(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

button[aria-label="Вернуться назад"] svg {
  transition: transform 0.2s ease;
}

button[aria-label="Вернуться назад"]:hover svg {
  transform: translateX(-2px);
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
.btn {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:active {
  transform: scale(0.95);
}
</style>
