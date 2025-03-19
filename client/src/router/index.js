import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue"; // Импортируйте компонент Login
import Register from "../components/Register.vue"; // Импортируйте компонент Register
import Rialto from "../components/Rialto.vue";
import Profile from "../components/Profile.vue";
import Teams from "../components/Teams.vue";
import ChangeProfile from "../components/ChangeProfile.vue";
import TeamDetails from "@/components/TeamDetails.vue";
import Ideas from "@/components/Ideas.vue";

const routes = [
  { path: "/", redirect: "/login" }, // Перенаправление с корневого маршрута на страницу входа
  { path: "/login", component: Login }, // Маршрут для страницы входа
  { path: "/register", component: Register }, // Маршрут для страницы регистрации
  { path: "/rialto", component: Rialto },
  { path: "/profile", component: Profile },
  { path: "/ChangeProfile", component: ChangeProfile },
  { path: "/teams", component: Teams },
  { path: "/ideas", component: Ideas },
  {
    path: "/team/:name",
    name: "TeamDetails",
    component: TeamDetails,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
