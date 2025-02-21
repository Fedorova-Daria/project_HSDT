import "./assets/main.css";

import Vue from "vue";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

new Vue({
  router, // Убедитесь, что роутер включен здесь
  render: (h) => h(App),
}).$mount("#app");
createApp(App).use(router).mount("#app");
