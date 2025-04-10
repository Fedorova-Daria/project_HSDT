import "./assets/main.css";
import { createApp, reactive } from "vue";
import App from "./App.vue";
import router from "./router";
import { getAccessToken, getUserData } from "@/api/storage.js"; // Импортируем нужные функции

const app = createApp(App);

// Глобальное реактивное состояние
const globalState = reactive({
  institute: getUserData()?.institute || "TYIU", // Используем getUserData для получения института
});

// Передаём глобальное состояние в приложение
app.provide("globalState", globalState);

// Подключаем Vuex и роутер
app.use(router);

// Монтируем приложение
app.mount("#app");