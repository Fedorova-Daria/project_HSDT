import "./assets/main.css";
import { createApp, reactive } from "vue";
import App from "./App.vue";
import router from "./router";
import UserService from "@/composables/storage.js"; // Импортируем нужные функции

const app = createApp(App);

document.addEventListener("DOMContentLoaded", () => {
  // Считываем сохранённую тему из LocalStorage
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.classList.toggle("dark-theme", savedTheme === "dark");

  // Привязываем переключатель к логике изменения темы
  const themeSwitch = document.getElementById("checkbox");
  themeSwitch.checked = savedTheme === "dark";

  themeSwitch.addEventListener("change", () => {
    const isDark = themeSwitch.checked;
    document.documentElement.classList.toggle("dark-theme", isDark);
    document.documentElement.classList.toggle("light-theme", !isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
});

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