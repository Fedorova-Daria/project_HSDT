<template>
  <div>
    <!-- Модальное окно для создания команды -->
    <div
      v-if="isCreateModalOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-card p-6 rounded-lg w-1/3">
        <h2 class="text-2xl mb-4 font-semibold">Создать новую команду</h2>
        <!-- Блок для аватарки -->
  
        <form @submit.prevent="createTeam">
          <!-- Название команды -->
          <div class="mb-4">
            <label class="block mb-2 font-medium">Название команды</label>
            <input
              v-model="newTeam.name"
              type="text"
              class="bg-input border-dynamic text-sm rounded-lg block w-full p-2.5 focus:outline-none focus:ring-0 focus:border-none"
              required
            />
          </div>
          <!-- Описание команды -->
          <div class="mb-4">
            <label class="block mb-2 font-medium">Описание команды</label>
            <textarea
              v-model="newTeam.description"
              class="bg-input border-dynamic text-sm rounded-lg block w-full p-2.5 focus:outline-none focus:ring-0 focus:border-none"
              required
            ></textarea>
          </div>
          <div class="flex justify-end">
            <button
              type="button"
              class="bg-red-500 text-always-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2 btn cursor-pointer"
              @click="closeCreateModal"
            >
              Отмена
            </button>
            <button
              type="submit"
              class="btn cursor-pointer bg-green-500 text-always-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors"
            >
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script>
import api from '@/composables/auth'; // Используем настроенный axios-инстанс
import UserService from '@/composables/storage.js'; // Сервис для работы с данными пользователя

export default {
  name: "TeamCreate",
  props: {
    isCreateModalOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      newTeam: {
        name: "",
        description: "",
        avatar: null, 
        avatarPreview: null,
        
      },
    };
  },
  methods: {
    /**
     * Обрабатывает выбор файла для аватарки.
     * Читает файл через FileReader и сохраняет данные в avatarPreview.
     */
    handleAvatarChange(e) {
      const file = e.target.files[0];
      if (file) {
        this.newTeam.avatar = file;
        const reader = new FileReader();
        reader.onload = (event) => {
          this.newTeam.avatarPreview = event.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.newTeam.avatar = null;
        this.newTeam.avatarPreview = null;
      }
    },
    /**
     * Закрывает модальное окно создания команды.
     */
    closeCreateModal() {
      this.$emit('close');
    },
    /**
     * Отправляет запрос на создание команды.
     * Если аватар выбран, используется FormData. Иначе – отправляются данные в формате JSON.
     */
    async createTeam() {
      try {
        let payload;
        let headers = {};
    
        if (this.newTeam.avatar) {
          payload = new FormData();
          payload.append('name', this.newTeam.name);
          payload.append('description', this.newTeam.description);
          // Передаём owner как строку (либо числовой ID)
        } else {
          payload = {
            name: this.newTeam.name,
            description: this.newTeam.description,
          };
        }
  
        // Обратите внимание: URL с завершающим слэшем
        const response = await api.post('/teams/', payload);
        console.log("Команда успешно создана:", response.data);
        this.$emit('teamCreated', response.data);
        // Очищаем форму
        this.newTeam = { name: "", description: ""};
        this.closeCreateModal();
      } catch (error) {
        console.error("Ошибка при создании команды:", error.response?.data || error.message);
      }
    },
  },
  /**
   * При создании компонента автоматически устанавливаем owner,
   * получая данные текущего пользователя из UserService.
   */
  created() {
  },
};
</script>
  
<style scoped>
.avatar-preview {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  background: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
</style>