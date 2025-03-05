<template>
  <div>
    <div class="absolute inset-0 bg-black opacity-30 z-10"></div>
    <!-- Картинка на фоне -->
    <img
      aria-hidden="true"
      class="top-0 left-0 h-screen w-screen object-cover fixed z-0"
      src="/bgg.jpg"
    />
    <div>
      <div class="relative w-4/5 m-auto mt-15 z-20">
        <h1 class="text-white text-8xl text-center font-display">
          Регистрация
        </h1>
        <div class="w-110 m-auto mt-10">
          <div class="flex flex-col items-center p-10">
            <!-- Поля формы -->
            <div class="w-full mb-4">
              <h2 class="text-white mb-1">Имя</h2>
              <input
                v-model="FirstName"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите имя..."
              />
            </div>
            <div class="w-full mb-4 flex flex-col">
              <h2 class="text-white mb-1">Фамилия</h2>
              <input
                v-model="LastName"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите фамилию..."
              />
            </div>
            <div class="w-full mb-4 flex flex-col">
              <h2 class="text-white mb-1">Почта</h2>
              <input
                v-model="email"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите почту..."
              />
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
            <!-- Поле Пароля (Теперь внутри общего контейнера!) -->
            <div class="w-full mb-4">
              <h2 class="text-white mb-1">Пароль</h2>
              <input
                v-model="password"
                type="password"
                class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
                placeholder="Введите пароль..."
              />
            </div>

            <button
              @click="registerUser"
              class="bg-purple-500 mt-4 text-white font-medium w-90 h-12 p-2 rounded-lg hover:bg-purple-600 duration-500"
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
export default {
  data() {
    return {
      FirstName: "",
      LastName: "",
      GroupID: null, // Будем хранить ID группы
      email: "",
      password: "",
      dropdownOpen: false,
      searchQuery: "",
      selectedGroup: null,
      groups: [], // Список групп загружаем с сервера
      filteredGroups: [], // Для фильтрации
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await fetch(
          "${API_BASE_URL}/api/users/registration/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({
              first_name: this.FirstName,
              last_name: this.LastName,
              group: Array.isArray(this.GroupID)
                ? this.GroupID[0]
                : this.GroupID, // Убираем массив, если это он
              email: this.email,
              password: this.password,
            }),
          }
        );

        // ✅ Читаем JSON только один раз
        const data = await response.json();

        if (response.ok) {
          console.log("Пользователь зарегистрирован:", data);
        } else {
          console.error("Ошибка регистрации:", data);
        }
      } catch (error) {
        console.error("Ошибка при отправке данных:", error);
      }
    },

    // Функция для получения списка групп с нового URL
    async fetchGroups() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/core/groups/list"
        );
        if (response.ok) {
          const data = await response.json();
          this.groups = data; // Сохраняем группы
          this.filteredGroups = data; // Инициализируем список для фильтрации
        } else {
          console.error("Ошибка при получении групп");
        }
      } catch (error) {
        console.error("Ошибка при загрузке групп:", error);
      }
    },

    // Функция для фильтрации групп
    filterGroups() {
      this.filteredGroups = this.groups.filter((group) =>
        group.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    // Функция для выбора группы
    selectGroup(group) {
      this.selectedGroup = group;
      this.GroupID = group.id; // Сохраняем ID группы
      this.dropdownOpen = false; // Закрываем список
    },
  },
  mounted() {
    this.fetchGroups(); // Загружаем группы при монтировании компонента
  },
};
</script>

<style scoped>
/* Стиль для выпадающего списка */
.max-h-48 {
  max-height: 12rem; /* Ограничиваем высоту списка для прокрутки */
}

.overflow-y-auto {
  overflow-y: auto; /* Включаем вертикальную прокрутку */
}

.cursor-pointer {
  cursor: pointer;
}

.hover\:bg-gray-200:hover {
  background-color: #edf2f7;
}
</style>
