<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm">
    <!-- Main modal -->
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative rounded-lg shadow-sm bg-card">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-zinc-600">
          <h3 class="text-lg font-semibold">
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
                class="block mb-2 text-sm font-medium"
                >Название проекта</label
              >
              <input
                v-model="form.title"
                type="text"
                name="name"
                id="name"
                class="bg-input border-dynamic text-sm rounded-lg block w-full p-2.5 focus:outline-none focus:ring-0 focus:border-none"
                placeholder="Какой вы придумали проект? Удивите нас!"
                required
              />
            </div>

            <div class="col-span-2">
              <label
                for="description"
                class="block mb-2 text-sm font-medium"
                >Расскажите, как можно улучшить наш университет!</label
              >
              <textarea
                v-model="form.description"
                id="description"
                rows="4"
                class="block mt-3 bg-input border-dynamic text-sm rounded-lg block w-full p-2.5 focus:outline-none focus:ring-0 focus:border-none"
                placeholder="Напишите подробное описание проекта здесь"
                required
              ></textarea>
            </div>
          </div>
          <div class="flex justify-between gap-4">
            <button
              @click="submitOffer('review')"
              type="button"
              :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
              class="text-always-white inline-flex items-center focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
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
import { instituteStyles } from "@/assets/instituteStyles.js";

export default {
  inject: ["globalState"],
  data() {
    return {
      currentBgColor: "",
      form: {
        title: '',
        description: '',
      },
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute]; // Используем глобальное состояние
      return style || { buttonOffColor: "#ccc" }; // Дефолтный стиль
    },
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
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