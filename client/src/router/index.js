import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue"; // Импортируйте компонент Login
import Register from "../components/Register.vue"; // Импортируйте компонент Register
import Rialto from "../components/Rialto.vue";
import Profile from "../components/Profile.vue";
const routes = [
  { path: "/", redirect: "/login" }, // Перенаправление с корневого маршрута на страницу входа
  { path: "/login", component: Login }, // Маршрут для страницы входа
  { path: "/register", component: Register }, // Маршрут для страницы регистрации
  { path: "/rialto", component: Rialto },
  { path: "/profile", component: Profile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
