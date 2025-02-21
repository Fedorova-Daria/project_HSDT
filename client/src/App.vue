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
    <router-view></router-view>
  </div>
</template>
