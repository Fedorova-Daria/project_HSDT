import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue"; // Импортируйте компонент Login
import Register from "../components/Register.vue"; // Импортируйте компонент Register

const routes = [
  { path: "/", redirect: "/login" }, // Перенаправление с корневого маршрута на страницу входа
  { path: "/login", component: Login }, // Маршрут для страницы входа
  { path: "/register", component: Register }, // Маршрут для страницы регистрации
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
