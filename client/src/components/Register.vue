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
        <div class="w-full mb-4">
          <h2 class="text-white mb-1">Группа</h2>
          <input
            v-model="Group"
            class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
            placeholder="Введите группу..."
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
        <div class="w-full mb-4">
          <h2 class="text-white mb-1">Номер телефона</h2>
          <input
            v-model="Phone"
            class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
            placeholder="Введите номер телефона..."
          />
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      FirstName: "",
      LastName: "",
      Group: "",
      email: "",
      Phone: "",
      password: "",
    };
  },
  methods: {
    async registerUser() {
      // Делаем запрос на сервер для регистрации
      try {
        const response = await fetch("http://localhost:8000/api/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            first_name: this.FirstName,
            last_name: this.LastName,
            group: this.Group,
            email: this.email,
            phone: this.Phone,
            password: this.password,
          }),
        });

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
};
</script>
