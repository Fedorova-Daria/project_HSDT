<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm">
    <!-- Main modal -->
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative rounded-lg shadow-sm bg-card">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-zinc-600">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Создать свое предложение
          </h3>
          <button
            @click="closeModal"
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-toggle="crud-modal"
          >
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 14"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
              />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <!-- Modal body -->
        <form @submit.prevent="submitOffer" class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <label
                for="name"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Название проекта</label
              >
              <input
                v-model="form.title"
                type="text"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-zinc-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                placeholder="Какой вы придумали проект? Удивите нас!"
                required
              />
            </div>

            <div class="col-span-2">
              <label
                for="description"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Расскажите, как можно улучшить наш университет!</label
              >
              <textarea
                v-model="form.description"
                id="description"
                rows="4"
                class="block mt-3 p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-zinc-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Напишите подробное описание проекта здесь"
                required
              ></textarea>
            </div>
          </div>
          <div class="flex justify-between gap-4">
            <button
              @click="submitOffer('open')"
              type="button"
              class="text-white inline-flex items-center bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-800"
            >
              <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
              </svg>
              Добавить предложение
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/composables/auth";

export default {
  data() {
    return {
      form: {
        title: '',
        description: '',
      },
    };
  },
  methods: {
    async submitOffer(status) {
  // Проверка, что статус один из допустимых
  const OfferData = {
    ...this.form,
    status,
  };
  try {
    const response = await api.post("/offers/", OfferData);
    console.log("Создано:", response);
  } catch (error) {
    console.error("Ошибка при создании:", error);
  }
},
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
/* Немного мягче фон */
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
</style>