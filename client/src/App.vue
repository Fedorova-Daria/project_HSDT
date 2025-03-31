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
    <router-view v-slot="{ Component }">
  <keep-alive>
    <component :is="Component" />
  </keep-alive>
</router-view>
  </div>
</template>
