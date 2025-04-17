<script>


export default {
  name: "App",
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