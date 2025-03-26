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
    <keep-alive>
    <router-view />
  </keep-alive>
  </div>
</template>
