<script>
import { startBackgroundTokenRefresh } from "@/api/auth.js"; // Импортируем вашу функцию обновления токенов

export default {
  name: "App",
  mounted() {
    // Запускаем процесс фонового обновления токенов при загрузке приложения
    startBackgroundTokenRefresh();
  },
};
</script>

<template>
  <div>
    <!-- Исправляем ключ -->
    <router-view v-slot="{ Component }" :key="$route.params.institute">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>