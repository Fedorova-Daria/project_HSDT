<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-zinc-800 p-6 rounded-lg w-1/3">
      <h2 class="text-white text-xl mb-4">Редактировать команду</h2>
      <form @submit.prevent="saveEditedTeam">
        <div class="mb-4">
          <label class="block text-white mb-2">Название команды</label>
          <input
            v-model="editedTeam.name"
            type="text"
            class="w-full p-2 rounded bg-zinc-700 text-white"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block text-white mb-2">Стек технологий</label>
          <div class="grid grid-cols-2 gap-2">
            <div
              v-for="tech in availableTechStack"
              :key="tech"
              class="flex items-center"
            >
              <input
                type="checkbox"
                :id="`edit-${tech}`"
                :value="tech"
                v-model="editedTeam.techStack"
                class="mr-2"
              />
              <label :for="`edit-${tech}`" class="text-white">{{ tech }}</label>
            </div>
          </div>
        </div>
        <div class="mb-4">
          <label class="block text-white mb-2">Статус</label>
          <select
            v-model="editedTeam.status"
            class="w-full p-2 rounded bg-zinc-700 text-white"
          >
            <option value="В работе">В работе</option>
            <option value="В поисках">В поисках</option>
            <option value="Неактивна">Неактивна</option>
            <option value="Проверяем">Проверяем</option>
            <option value="Забанена">Забанена</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button
            type="button"
            class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2"
            @click="closeModal"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors"
          >
            Сохранить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    editedTeam: {
      type: Object,
      required: true,
    },
    availableTechStack: {
      type: Array,
      required: true,
    },
  },
  methods: {
    saveEditedTeam() {
      this.$emit("save-edited-team", { ...this.editedTeam });
      this.closeModal();
    },
    closeModal() {
      this.$emit("close-modal");
    },
  },
};
</script>
