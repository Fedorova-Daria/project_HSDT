<template>
  <div v-if="idea">
    <h1>{{ idea.name }}</h1>
    <p>{{ idea.description }}</p>
    <p>
      <strong>Инициатор:</strong> {{ idea.initiator_info.name }} (Роль:
      {{ idea.initiator_info.role }})
    </p>
    <p><strong>Технологии:</strong> {{ idea.technologies_info.join(", ") }}</p>
    <p><strong>Дата создания:</strong> {{ idea.created_at }}</p>
    <!-- Добавить другие поля по необходимости -->
  </div>
  <div v-else>
    <p>Загрузка...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
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
