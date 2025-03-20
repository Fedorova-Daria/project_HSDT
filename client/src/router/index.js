import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/users/Login.vue"; // Импортируйте компонент Login
import Register from "../components/users/Register.vue"; // Импортируйте компонент Register
import Rialto from "../components/projects/Rialto.vue";
import Profile from "../components/users/Profile.vue";
import Teams from "../components/teams/Teams.vue";
import ChangeProfile from "../components/users/ChangeProfile.vue";
import TeamDetails from "@/components/teams/TeamDetails.vue";
import Ideas from "@/components/projects/Ideas.vue";
import IdeaDetail from "@/components/projects/IdeaDetail.vue";

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
  {
    path: "/ideas/:id", // Параметр id в URL
    name: "IdeaDetail",
    component: IdeaDetail,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
