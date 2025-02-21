<template>
  <div class="w-4xl m-auto mt-40">
    <h1 class="text-white text-9xl text-center">Портал ВШЦТ</h1>
  </div>

  <div class="w-110 m-auto mt-5">
    <div class="flex flex-col items-center p-10">
      <div class="w-full mb-4">
        <h2 class="text-white mb-1">Почта</h2>
        <input
          v-model="email"
          class="m-auto w-90 bg-white text-grey px-2 py-2 rounded-lg border-3 border-solid border-fiol duration-500 ease-linear transition-colors hover:border-purple-500 focus:border-purple-600 outline-none"
          placeholder="Введите почту..."
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
        <div class="flex justify-end mt-2">
          <button class="text-blue-300 text-sm">Забыли пароль?</button>
        </div>
      </div>

      <button
        class="bg-purple-500 text-white font-medium w-90 p-2 rounded-lg hover:bg-purple-600 duration-500"
      >
        Войти
      </button>
    </div>
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
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  methods: {
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>
