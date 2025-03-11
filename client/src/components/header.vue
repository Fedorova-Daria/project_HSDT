<template>
  <div>
    <header
      class="flex items-center justify-between px-8 py-4 border border-border"
    >
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1 class="font-display text-fiol text-3xl">ВШЦТ</h1>
      </div>
      <!-- Навигация -->
      <nav class="flex items-center gap-10">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.link"
          class="relative text-lg font-medium transition-colors duration-300 group text-white hover:text-purple-400"
          :class="{ 'text-purple-400': $route.path === item.link }"
        >
          {{ item.name }}
          <span
            class="absolute left-1/2 bottom-[-5px] h-[3px] bg-purple-400 rounded-full transition-all duration-300 w-0 group-hover:w-full group-hover:left-0"
            :class="{ 'w-2/3 left-1/6': $route.path === item.link }"
          ></span>
        </router-link>

        <!-- Уведомления -->
        <button class="relative">
          <img src="/notificate.svg" alt="notification" class="w-6" />
        </button>

        <!-- Аватарка -->
        <div class="relative w-12 h-12">
          <img
            @click="goToProfile"
            src=""
            alt="User Avatar"
            class="w-full h-full rounded-full border-2 border-zinc-700 hover:border-purple-400 transition-all duration-300 cursor-pointer"
          />
        </div>
      </nav>
    </header>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      menuItems: [
        { name: "Биржа", link: "/rialto" },
        { name: "Команды", link: "/teams" },
        { name: "Идеи", link: "/ideas" },
      ],
    };
  },
  methods: {
    goToProfile() {
      this.$router.push("/profile");
    },
  },
};
</script>
