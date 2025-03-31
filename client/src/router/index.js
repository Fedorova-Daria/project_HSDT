import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/users/Login.vue";
import Register from "../components/users/Register.vue";
import RegZ from "../components/users/RegZ.vue";
import Rialto from "../components/projects/Rialto.vue";
import Profile from "../components/users/Profile.vue";
import Teams from "../components/teams/Teams.vue";
import ChangeProfile from "../components/users/ChangeProfile.vue";
import TeamDetails from "@/components/teams/TeamDetails.vue";
import Ideas from "@/components/projects/Ideas.vue";
import IdeaDetail from "@/components/projects/IdeaDetail.vue";
import AboutTYIU from "../components/university/AboutTYIU.vue"; // Страница About только для TYIU

const routes = [
  {
    path: "/",
    redirect: () => {
      const userData = JSON.parse(localStorage.getItem("userData") || "{}");
      return userData.institute ? `/${userData.institute}/rialto` : "/login";
    },
  },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/registerZ", component: RegZ },
  { path: "/:institute/profile", name: "profile", component: Profile },
  { path: "/change-profile", component: ChangeProfile },

  // Динамические маршруты для всех институтов
  {
    path: "/:institute/rialto",
    name: "rialto",
    component: Rialto,
  },
  {
    path: "/:institute/teams",
    name: "teams",
    component: Teams,
  },
  {
    path: "/:institute/team/:name",
    name: "teamDetails",
    component: TeamDetails,
  },
  {
    path: "/:institute/ideas/",
    name: "Ideas",
    component: Ideas,
  },
  {
    path: "/:institute/ideas/:id",
    name: "ideaDetail",
    component: IdeaDetail,
    props: route => ({ ideaId: route.params.id, institute: route.params.institute })  // Передаем параметры как пропсы
  },
  {
    path: "/TYIU/about",
    name: "aboutTYIU",
    component: AboutTYIU,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 };
  },
});

export default router;