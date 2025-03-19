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
          <th class="p-3 text-left">Дата создания</th>
          <!--жопа-->
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
              <textarea
                v-model="idea.description"
                id="ideaDescription"
                required
              ></textarea>
            </div>
            <div class="modal-actions">
              <button type="submit">Создать</button>
              <button type="button" @click="$emit('close')">Закрыть</button>
            </div>
          </form>
        </div>
      </div>
    </template>
  </div>
</template>
