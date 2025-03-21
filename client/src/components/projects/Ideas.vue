<template>
  <div>
    <Header />
    <div class="ideas-container text-white">
      <!-- Форма для добавления новой идеи -->
      <div class="add-idea">
        <input v-model="newIdeaText" placeholder="Введите новую идею" />
        <button @click="addIdea">Добавить</button>
      </div>

      <!-- Таблица идей (основная) -->
      <h2>СПИСОК ГОТОВЫХ ИДЕЙ</h2>
      <table>
        <thead>
          <tr>
            <th>Идея</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(idea, index) in ideas" :key="idea.id">
            <td>{{ idea.text }}</td>
            <td>
              <select v-model="idea.status">
                <option value="новая">Новая</option>
                <option value="в процессе">В процессе</option>
                <option value="завершена">Завершена</option>
              </select>
            </td>
            <td>
              <button @click="deleteIdea(index)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Таблица с идеями для улучшения работы -->
      <h2>ЛУЧШИЕ ИДЕИ</h2>
      <table>
        <thead>
          <tr>
            <th>Название идеи</th>
            <th>Оценка идеи</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(idea, index) in workEfficiencyIdeas" :key="idea.id">
            <td>{{ idea.text }}</td>
            <td>
              <button @click="deleteWorkEfficiencyIdea(index)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import Header from "@/components/header.vue";

export default {
  components: { Header },

  data() {
    return {
      newIdeaText: "",
      ideas: [],
      workEfficiencyIdeas: [
        { id: 1, text: "Знаете, как сделать работу лучше?" },
        { id: 2, text: "Есть новое и полезное решение?" },
        {
          id: 3,
          text: "Использовать систему Pomodoro для повышения концентрации",
        },
      ],
    };
  },

  methods: {
    // Метод для добавления новой идеи в основную таблицу
    addIdea() {
      if (this.newIdeaText.trim() === "") return;

      const newIdea = {
        id: Date.now(), // Уникальный ID для каждой идеи
        text: this.newIdeaText,
        status: "новая",
      };

      this.ideas.push(newIdea);
      this.newIdeaText = ""; // Очистить поле ввода
    },

    // Метод для удаления идеи из основной таблицы
    deleteIdea(index) {
      this.ideas.splice(index, 1);
    },

    // Метод для удаления идеи из таблицы "Идеи для улучшения работы"
    deleteWorkEfficiencyIdea(index) {
      this.workEfficiencyIdeas.splice(index, 1);
    },
  },
};
</script>

<style scoped>
.ideas-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1,
h2 {
  text-align: center;
  margin-bottom: 20px;
}

.add-idea {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.add-idea input {
  width: 75%;
  padding: 8px;
  font-size: 14px;
}

.add-idea button {
  width: 20%;
  padding: 8px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

.add-idea button:hover {
  background-color: #45a049;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table,
th,
td {
  border: 1px solid #ddd;
}

th,
td {
  padding: 10px;
  text-align: left;
}

td select {
  width: 100%;
  padding: 5px;
}

button {
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #d32f2f;
}
</style>
