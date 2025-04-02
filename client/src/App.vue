<script>
export default {
  methods: {
    goToHome() {
      this.$router.push("/");
    },
    goToAbout() {
      this.$router.push("/register");
    },
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