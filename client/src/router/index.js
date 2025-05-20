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
import ProjectDetail from "@/components/projects/ProjectDetail.vue";
import ideaDetail from "@/components/projects/IdeaDetail.vue";
import AboutTYIU from "../components/university/AboutTYIU.vue"; // Страница About только для TYIU
import Kanban from "@/components/in project/kanban.vue";
import Statistic from "@/components/in project/statistics.vue";
import info from "@/components/in project/info.vue";
import Offers from "@/components/university/offers.vue";
import OfferDetail from "@/components/university/offerDetail.vue";
import Cookies from "js-cookie";
const routes = [
  {
    path: "/",
    redirect: () => {
      const userData = JSON.parse(Cookies.get("userData") || "{}");
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
    path: "/:institute/offers",
    name: "offers",
    component: Offers,
  },
  {
    path: "/:institute/teams",
    name: "teams",
    component: Teams,
  },
  {
    path: "/:institute/team/:teamId",
    name: "teamDetails",
    component: TeamDetails,
    props: true // Это позволяет передавать параметры как props в компонент
  },
  {
    path: "/:institute/ideas/",
    name: "Ideas",
    component: Ideas,
  },
  {
  path: '/:institute/project/:ideaId/kanban',
  name: 'Kanban',
  component: Kanban,
  props: true  // вот это!
},
  {
  path: '/:institute/project/:ideaId/statistic',
  name: 'Statistic',
  component: Statistic,
  props: true  // вот это!
},
  {
  path: '/:institute/project/:ideaId/info',
  name: 'info',
  component: info,
  props: true  // вот это!
},
  {
    path: "/:institute/project/:id",
    name: "ProjectDetail",
    component: ProjectDetail,
    props: route => ({ ideaId: route.params.id, institute: route.params.institute })  // Передаем параметры как пропсы
  },
  {
    path: "/:institute/idea/:id",
    name: "ideaDetail",
    component: ideaDetail,
    props: route => ({ ideaId: route.params.id, institute: route.params.institute })  // Передаем параметры как пропсы
  },
  {
    path: "/:institute/offer/:id",
    name: "OfferDetail",
    component: OfferDetail,
    props: route => ({ offerId: route.params.id, institute: route.params.institute })  // Передаем параметры как пропсы
  },
  {
    path: "/TYIU/about",
    name: "AboutTYIU",
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