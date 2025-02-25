<template>
  <div>
    <header class="flex justify-between border-b border-zinc-700">
      <div class="flex items-center gap-4 p-2 ml-auto">
        <ul class="flex items-center gap-10">
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Биржа</button>
          </li>
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Команды</button>
          </li>
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Идеи</button>
          </li>
        </ul>
        <img src="/notific.svg" alt="notification" class="w-10 ml-5" />
      </div>
    </header>

    <h1 class="font-display w-4/5 m-auto mt-20 text-white text-5xl">
      Биржа проектов ВШЦТ
    </h1>

    <div class="flex w-4/5 m-auto mt-5">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          class="border bg-white rounded-md py-2 pl-10 pr-4 outline-none focus:border-fiol duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
        class="ml-5 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>
      <select
        class="ml-5 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все стеки технологий</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>
    </div>
    <button class="bg-purple-600 text-white">Создать идею</button>
    <router-view />
  </div>
</template>

<script>
//import IdeaCard from "./components/RialtoCard1.vue"; // Убедись, что путь правильный

export default {
  //  components: { IdeaCard },
  //  data() {
  //   return {
  //      testIdea: {
  //      id: 1,
  //    title: "Создание сайта для конкурса 'Педагог года'",
  //  description:
  //  "Разработка веб-приложения для анкет преподавателей и голосования.",
  //author: "Екатерина Сердюкова",
  //technologies: ["C#", "Vue.js"],
  //status: "Набор открыт",
  //},
  userRole: "заказчик", // Подставь реальную роль пользователя (например, из API или Vuex)
  allowedRoles: ["admin", "эксперт", "заказчик"], // Роли, которым доступна кнопка
  methods: {
    createIdea() {
      console.log("Переход на создание идеи");
      // Заменить на реальный маршрут
    },
  },
};
</script>
// //
<style scoped>
.idea-card {
  transition: transform 0.3s ease, border-color 0.3s ease;
}
</style>
