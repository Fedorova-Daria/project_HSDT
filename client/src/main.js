import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from './store'; // Подключаем Vuex store

// Сначала создаем экземпляр приложения
const app = createApp(App);

// Подключаем Vuex и роутер
app.use(store);
app.use(router);

// Монтируем приложение
app.mount("#app");