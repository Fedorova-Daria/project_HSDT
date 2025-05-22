import "./assets/main.css";
import { createApp, reactive } from "vue";
import App from "./App.vue";
import router from "./router";
import UserService from "@/composables/storage.js"; // Импортируем нужные функции
import { useTheme } from "./composables/useTheme";

const app = createApp(App);

const { initTheme } = useTheme();
initTheme(); // применяем тему до запуска приложения

// Глобальное реактивное состояние
const globalState = reactive({
  institute: UserService.getUserData()?.institute || "TYIU", // Используем getUserData для получения института
});

// Передаём глобальное состояние в приложение
app.provide("globalState", globalState);

// Подключаем Vuex и роутер
app.use(router);

// Монтируем приложение
app.mount("#app");
