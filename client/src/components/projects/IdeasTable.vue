<template>
    <table class="w-full mt-5 border-collapse shadow-lg rounded-lg overflow-hidden bg-card table-auto">
      <thead>
        <tr class="bg-card text-center">
          <th class="px-6 py-3 w-10">#</th>
          <th class="px-6 py-3 w-1/4">Название</th>
          <th class="px-6 py-3 w-1/4">Инициатор</th>
          <th class="px-6 py-3 w-1/4">Дата создания</th>
          <th class="px-6 py-3 w-1/8">Статус</th>
          <th class="px-6 py-3 w-1/6"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="idea in items"
          :key="idea.id"
          class="border-b border-zinc-700 bg-card transition duration-200 text-center"
        >
          <td class="px-6 py-4">{{ idea.id }}</td>
          <td class="px-6 py-4 font-medium">{{ idea.title }}</td>
          <td class="px-6 py-4">{{ idea.initiator || "Неизвестный автор" }}</td>
          <td class="px-6 py-4">{{ new Date(idea.created_at).toLocaleDateString("ru-RU") }}</td>
          <td class="px-6 py-4 rounded text-white font-semibold text-center"
>
  <span class="inline-block px-2 py-1 rounded-lg" 
        :style="{ backgroundColor: getStatusStyle(idea.status).color }">
    {{ getStatusStyle(idea.status).label }}
  </span>
</td>
          <td class="px-6 py-4 flex justify-end gap-2">
            <button
              @click="$emit('open-idea', idea)"
              class="px-4 py-2 text-sm font-medium text-always-white rounded-lg transition"
              :style="{ backgroundColor: hoverStates[idea.id] || instituteStyle.buttonOffColor }"
              @mouseover="hoverStates[idea.id] = instituteStyle.buttonOnColor"
              @mouseleave="hoverStates[idea.id] = instituteStyle.buttonOffColor"
            >
              Посмотреть
            </button>
            <div class="flex items-center gap-2 min-w-[80px] justify-end">
              <h1 class="text-dynamic font-semibold">{{ idea.likes_count || 0 }}</h1>
              <img
      :src="isLiked(idea) ? '/liked.svg' : '/like.svg'"
      alt="like"
      class="w-6 h-6 cursor-pointer"
      @click="(event) => $emit('toggle-like', idea, event)"
    />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script>
import { instituteStyles } from "@/assets/instituteStyles.js";

  export default {
    inject: ["globalState"],
     data() {
    return {
      currentBgColor: "",
      hoverStates: {}
    };
  },
    props: {
      items: Array, // Список идей
      userId: Number, // ID текущего пользователя
    },
    methods: {
      isLiked(idea) {
        return idea.likes.includes(this.userId);
      },
      getStatusStyle(status) {
      const statusStyles = {
        draft: { color: "#f0f0f0", label: "Черновик" },
        open: { color: "#2AC778",color: "#2AC778", label: "Доступен" },
        under_review: { color: "#ffe5b4", label: "Рассматриваем" },
        unknown: { color: "#cccccc", label: "Неизвестно" }
      };
      return statusStyles[status] || statusStyles.unknown;
    },
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
  };
  </script>
  
  <style scoped>
  .bg-cards {
    background-color: rgba(30, 30, 30, 0.8);
    backdrop-filter: blur(5px);
  }
  .bg-buttonoff {
    background-color: rgba(107, 33, 168, 0.7);
  }
  .bg-buttonoff:hover {
    background-color: rgba(107, 33, 168, 0.9);
  }
  </style>