<template>
  <div>
    <Header />
    <div class="flex w-4/5 mx-auto mt-10 gap-4 text-white">
      <!-- Левый блок (Название и кнопки для функций идей) -->
      <div class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <strong class="mt-5 text-3xl"> Идея: пупырышки из пиздырышки</strong>
        <div class="mt-3 h-0.5 w-full m-auto bg-white"></div>
        <h1 class="text-xl mt-3">Инициатор:</h1>
        <h2 class="text-xl mt-1 font-bold">Павел Дуров</h2>
        <button>Взять идею</button>
        <button>Лайк сделать</button>
        <button>Редактировать</button>
        <button>Удалить</button>
      </div>
      <!-- Правый блок (вся информация о идее) -->
      <div class="w-3/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <strong class="mt-5 text-3xl"> Информация об идее</strong>
        <div class="mt-3 h-0.5 w-full m-auto bg-white"></div>
        <h1 class="text-xl mt-3">
          Ну тут вся инфа кароче да мы тут все пишем расписываем можем
          редактировать это спокойно так что вот так вот движемся
        </h1>
      </div>
    </div>
  </div>
  <!--<div class="text-white" v-else>
    <p>Загрузка...</p>
  </div>-->
</template>

<script>
import axios from "axios";
import Header from "@/components/header.vue";
export default {
  components: { Header },
  data() {
    return {
      idea: null, // Здесь будем хранить данные о выбранной идее
    };
  },
  async created() {
    // Получаем id из URL
    const ideaId = this.$route.params.id;
    await this.fetchIdeaDetail(ideaId); // Загружаем информацию о идее по id
  },
  methods: {
    async fetchIdeaDetail(id) {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/ideas/${id}/`
        );
        this.idea = response.data; // Сохраняем данные о идее в переменную idea
      } catch (error) {
        console.error("Ошибка при загрузке информации о идее:", error);
      }
    },
  },
};
</script>
