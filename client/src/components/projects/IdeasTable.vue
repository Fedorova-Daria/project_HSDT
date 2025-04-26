<template>
    <table class="w-full mt-5 border-collapse shadow-lg rounded-lg overflow-hidden bg-card table-auto">
      <thead>
        <tr class="bg-card text-left">
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
          class="border-b border-zinc-700 hover:bg-card transition duration-200"
        >
          <td class="px-6 py-4">{{ idea.id }}</td>
          <td class="px-6 py-4 font-medium">{{ idea.title }}</td>
          <td class="px-6 py-4">{{ idea.initiator || "Неизвестный автор" }}</td>
          <td class="px-6 py-4">{{ idea.created_at }}</td>
          <td class="px-6 py-4">{{ idea.status || "Неизвестно" }}</td>
          <td class="px-6 py-4 flex justify-end gap-2">
            <button
              @click="$emit('open-idea', idea)"
              class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
            >
              Посмотреть
            </button>
            <div class="flex items-center gap-2 min-w-[80px] justify-end">
              <h1 class="text-white font-semibold">{{ idea.likes_count || 0 }}</h1>
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
  export default {
    props: {
      items: Array, // Список идей
      userId: Number, // ID текущего пользователя
    },
    methods: {
      isLiked(idea) {
        return idea.likes.includes(this.userId);
      },
    },
  };
  </script>
  
  <style scoped>
  .bg-card {
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