<template>
  <div>
    <!-- Модальное окно для создания команды -->
    <div
      v-if="isCreateModalOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-card p-6 rounded-lg w-1/3">
        <h2 class="text-white text-xl mb-4">Создать новую команду</h2>
        <form @submit.prevent="createTeam">
          <div class="mb-4">
            <label class="block text-white mb-2">Название команды</label>
            <input
              v-model="newTeam.name"
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
                  :id="`create-${tech}`"
                  :value="tech"
                  v-model="newTeam.techStack"
                  class="mr-2"
                />
                <label :for="`create-${tech}`" class="text-white">{{
                  tech
                }}</label>
              </div>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-white mb-2">Статус</label>
            <select
              v-model="newTeam.status"
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
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors mr-2 btn cursor-pointer"
              @click="closeCreateModal"
            >
              Отмена
            </button>
            <button
              type="submit"
              class="btn cursor-pointer bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors"
              :disabled="newTeam.members < 1"
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
export default {
  props: {
    isCreateModalOpen: {
      type: Boolean,
      required: true,
    },
    availableTechStack: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      newTeam: {
        name: "",
        members: 1,
        techStack: [],
        rating: 0,
        status: "В поисках",
      },
    };
  },
  methods: {
    closeCreateModal() {
      this.$emit("close-create-modal");
      this.resetNewTeam();
    },
    resetNewTeam() {
      this.newTeam = {
        name: "",
        members: 1,
        techStack: [],
        rating: 0,
        status: "В поисках",
      };
    },
    createTeam() {
      if (this.newTeam.members < 1) {
        return;
      }
      this.$emit("create-team", { ...this.newTeam });
      this.closeCreateModal();
    },
  },
};
</script>
