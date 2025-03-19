<template>
  <div>
    <Header />
    <table
      class="w-3/5 m-auto border-collapse shadow-lg rounded-lg overflow-hidden"
    >
      <thead class="bg-zinc-800 text-white">
        <tr>
          <th class="p-3 text-left">Название идеи</th>
          <th class="p-3 text-left">Статус</th>
          <th class="p-3 text-left">Дата создания</th><!--жопа-->
        </tr>
      </thead>
      <tbody>
        <tr class="bg-cards transition-colors text-white hover:bg-zinc-700">
          <td class="p-3 border-t border-zinc-600"></td>
          <td class="p-3 border-t border-zinc-600"></td>
          <td class="p-3 border-t border-zinc-600"></td>
        </tr>
      </tbody>
    </table>
    <template>
  <div class="idea-page">
    <div class="idea-container">
      <h1 class="idea-title">{{ idea.name }}</h1>
      <p class="idea-description">{{ idea.description }}</p>

      <div class="idea-actions">
        <button @click="editIdea">Редактировать</button>
        <button @click="deleteIdea">Удалить</button>
      </div>
    </div>
  </div>
</template>
    <template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Создать идею</h3>
      <form @submit.prevent="handleSubmit">
        <div>
          <label for="ideaName">Название идеи</label>
          <input v-model="idea.name" type="text" id="ideaName" required />
        </div>
        <div>
          <label for="ideaDescription">Описание идеи</label>
          <textarea v-model="idea.description" id="ideaDescription" required></textarea>
        </div>
        <div class="modal-actions">
          <button type="submit">Создать</button>
          <button type="button" @click="$emit('close')">Закрыть</button>
        </div>
      </form>
    </div>
  </div>
</template>




<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

button {
  padding: 8px 12px;
  border: none;
  background-color: #3498db;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button[type="button"] {
  background-color: #e74c3c;
}
</style>
  
      
  </div>
</template>

<script>
import Header from "@/components/header.vue";

export default {
  components: {
    Header,
  },
};
</script>
