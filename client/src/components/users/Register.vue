<template>
  <div class="relative h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <ParallaxBackground />
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
          Регистрация
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
              <h2 class="text-white mb-1">Группа</h2>
              <div
                class="relative m-auto w-90 bg-white text-grey rounded-lg border-2 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
              >
                <!-- Кнопка для открытия списка -->
                <div
                  class="w-full border border-fiol rounded-md py-2 px-3 bg-white text-black cursor-pointer flex justify-between items-center transition-colors hover:border-purple-500 focus:border-purple-600"
                  @click="dropdownOpen = !dropdownOpen"
                >
                  <span>{{
                    selectedGroup ? selectedGroup.name : "Выберите группу"
                  }}</span>
                  <span
                    :class="{ 'rotate-180': dropdownOpen }"
                    class="transition-transform"
                  >
                    &#9660;
                  </span>
                </div>

                <!-- Выпадающий список -->
                <div
                  v-if="dropdownOpen"
                  class="flex flex-col absolute left-0 w-full bg-white border-3 border-solid border-fiol rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-50 transition-colors hover:border-purple-500"
                >
                  <!-- Поле поиска -->
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Поиск..."
                    class="w-full px-3 py-2 border-b border-fiol outline-none transition-colors hover:border-purple-500 focus:border-purple-600"
                    @input="filterGroups"
                  />

                  <!-- Список групп -->
                  <div
                    v-for="group in filteredGroups"
                    :key="group.id"
                    @click="selectGroup(group)"
                    class="p-2 cursor-pointer hover:bg-gray-200 transition-colors duration-300"
                  >
                    {{ group.name }}
                  </div>
                </div>
              </div>
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
              @click="registerStudent"
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
import { useAuth } from "@/composables/useAuth";
import ParallaxBackground from "@/components/ParallaxBackground.vue";
import api from '@/composables/auth'; // Путь к вашему axios instance

export default {
  components: {ParallaxBackground},
  data() {
  return {
    first_name: "",
    last_name: "",
    searchQuery: '', // Для хранения введенного текста
    dropdownOpen: false, // Для отображения выпадающего списка
    groups: [], // Список всех групп
    filteredGroups: [], // Отфильтрованный список групп
    selectedGroup: null, // Объект выбранной группы
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
  };
},
  mounted() {
    this.fetchGroups(); // Загружаем группы при монтировании компонента
  },
  methods: {

    goBack() {
      this.$router.go(-1);
    },

    // Остальные методы формы

     // Функция для получения списка всех групп
     async fetchGroups() {
      try {
        const response = await api.get('/core/university_groups');
        this.groups = response.data; // Сохраняем все группы
        this.filteredGroups = this.groups; // Изначально все группы видны
      } catch (error) {
        console.error("Ошибка при получении групп:", error);
      }
    },

    // Фильтрация групп по запросу
    filterGroups() {
      if (this.searchQuery === '') {
        this.filteredGroups = this.groups; // Если нет запроса, показываем все группы
      } else {
        this.filteredGroups = this.groups.filter(group =>
          group.name.toLowerCase().includes(this.searchQuery.toLowerCase()) // Фильтруем по имени
        );
      }
    },

    // Функция для выбора группы
    selectGroup(group) {
  this.selectedGroup = group; // Сохраняем объект выбранной группы
  this.searchQuery = group.name; // Заполняем поле поиска названием группы
  this.dropdownOpen = false; // Закрываем выпадающий список
},

    // Метод для открытия выпадающего списка
    openDropdown() {
      this.dropdownOpen = true;
      this.fetchGroups(); // Загружаем группы, когда открываем список
    },

    // Метод для закрытия выпадающего списка
    closeDropdown() {
      this.dropdownOpen = false;
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword;
    },
    toggleShowConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      this.emailError = !this.email
        ? "Поле email обязательно"
        : !emailRegex.test(this.email)
        ? "Введите корректный email"
        : "";
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

      this.passwordStrength =
        strength < 2 ? "weak" : strength < 4 ? "medium" : "strong";

      this.passwordError = "";
      this.validateForm();
    },
    validateConfirmPassword() {
      this.confirmPasswordError = !this.confirmPassword
        ? "Подтвердите пароль"
        : this.password !== this.confirmPassword
        ? "Пароли не совпадают"
        : "";
      this.validateForm();
    },
    validateForm() {
  this.isFormValid =
    this.first_name &&
    this.last_name &&
    this.selectedGroup &&  // Проверка на выбранную группу
    this.email &&
    !this.emailError &&
    this.password &&
    !this.passwordError &&
    this.confirmPassword &&
    !this.confirmPasswordError &&
    this.password === this.confirmPassword;
},
async registerStudent() {
  if (!this.isFormValid) {
    alert("Пожалуйста, заполните все поля корректно.");
    return;
  }

  const { registerStudent } = useAuth();

  try {
    await registerStudent({
      first_name: this.first_name,
      last_name: this.last_name,
      group: this.selectedGroup.id,  // Используем только ID группы
      email: this.email,
      password: this.password,
    });
     // Переход на страницу логина после успешной регистрации
     router.push("/login");
  } catch (error) {
    this.emailError = error.message;
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
</style>
