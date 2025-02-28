<template>
  <div class="w-4xl m-auto mt-10">
    <h1 class="text-white text-8xl text-center">Регистрация</h1>
    <div class="w-110 m-auto mt-5">
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

        <div class="relative w-64">
          <!-- Кнопка для открытия списка -->
          <div
            class="w-full border rounded-md py-2 px-3 bg-white text-black cursor-pointer flex justify-between items-center"
            @click="dropdownOpen = !dropdownOpen"
          >
            <span>{{
              selectedGroup ? selectedGroup.name : "Выберите группу"
            }}</span>
            <span
              :class="{ 'rotate-180': dropdownOpen }"
              class="transition-transform"
              >&#9660;</span
            >
          </div>

          <!-- Выпадающий список -->
          <div
            v-if="dropdownOpen"
            class="absolute w-full bg-white border rounded-md shadow-lg mt-1 max-h-48 overflow-y-auto z-50"
          >
            <!-- Поле поиска -->
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск..."
              class="w-full px-3 py-2 border-b outline-none"
              @input="filterGroups"
            />
          </div>
        </div>
      </div>
      <div class="w-full mb-4 flex flex-col">
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
        class="bg-purple-500 mt-4 text-white font-medium w-90 p-2 rounded-lg hover:bg-purple-600 duration-500"
      >
        Войти
      </button>
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
      Phone: "",
      password: "",
      dropdownOpen: false,
      searchQuery: "",
      selectedGroup: null,
      groups: [], // Список групп загружаем с сервера
      filteredGroups: [],
    };
  },
  methods: {
    async fetchGroups() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/core/groups/list"
        ); // Замените на ваш эндпоинт
        if (!response.ok) throw new Error("Ошибка загрузки групп");
        const data = await response.json();
        this.groups = data; // Предполагаем, что сервер возвращает массив { id, name }
        this.filteredGroups = this.groups;
      } catch (error) {
        console.error("Ошибка при загрузке групп:", error);
      }
    },
    filterGroups() {
      this.filteredGroups = this.groups.filter((group) =>
        group.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    selectGroup(group) {
      this.selectedGroup = group;
      this.GroupID = group.id; // Присваиваем ID, а не name
      this.searchQuery = "";
      this.dropdownOpen = false;
    },
    async registerUser() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/users/registration/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              first_name: this.FirstName,
              last_name: this.LastName,
              group_id: this.GroupID, // Отправляем ID группы, а не название
              email: this.email,
              password: this.password,
            }),
          }
        );

        if (response.ok) {
          const data = await response.json();
          console.log("Пользователь зарегистрирован:", data);
        } else {
          console.error("Ошибка регистрации");
        }
      } catch (error) {
        console.error("Ошибка при отправке данных:", error);
      }
    },
  },
  mounted() {
    this.fetchGroups(); // Загружаем группы при загрузке страницы
  },
};
</script>
