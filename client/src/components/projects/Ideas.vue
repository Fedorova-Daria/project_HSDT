<template>
  <div>
    <Header />

    <div class="w-4/5 m-auto mt-6 text-white">
      <button
        @click="openModal"
        class="bg-purple-600 text-white rounded-md mb-5 px-4 py-2 hover:bg-purple-700 transition ml-5 h-10"
      >
        Создать идею
      </button>
      <table
        class="w-full border-collapse shadow-lg rounded-lg overflow-hidden bg-card table-auto"
      >
        <thead>
          <tr class="bg-bgg text-left">
            <th class="px-6 py-3 w-10">#</th>
            <th class="px-6 py-3 w-1/4">Название</th>
            <th class="px-6 py-3 w-1/4">Стеки технологий</th>
            <th class="px-6 py-3 w-1/4">Дата создания</th>
            <th class="px-6 py-3 w-1/8">Статус</th>
            <th class="px-6 py-3 w-1/6"></th>
          </tr>
        </thead>
        <tbody>
          <!-- Добавляем проверку для существования items -->
          <tr
            v-for="item in items"
            :key="item.id"
            class="border-b border-zinc-700 hover:bg-card transition duration-200"
          >
            <td class="px-6 py-4">{{ item.id }}</td>
            <td class="px-6 py-4 font-medium">{{ item.name }}</td>
            <td class="px-6 py-4">
              <div class="flex flex-wrap gap-2">
                <!-- Проверяем, сколько стека технологий -->
                <span
                  v-for="(tech, techIndex) in item.technologies_info.slice(
                    0,
                    3
                  )"
                  :key="techIndex"
                  class="px-2 py-1 bg-purple-600 text-white rounded"
                >
                  {{ tech.name }}
                </span>

                <!-- Если стека технологий больше 3, показываем "+X" -->
                <span
                  v-if="item.technologies_info.length > 3"
                  class="text-xs text-white"
                >
                  +{{ item.technologies_info.length - 3 }}
                </span>
              </div>
            </td>
            <td class="px-6 py-4">{{ item.created_at }}</td>
            <td class="px-6 py-4"></td>

            <td class="px-6 py-4 flex justify-end gap-2">
              <button
                @click="viewItem(item)"
                class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
              >
                Посмотреть
              </button>
              <div class="flex items-center gap-2 min-w-[80px] justify-end">
                <h1 class="text-white font-semibold">{{ likeCount }}</h1>
                <img
                  :src="likedItems[item.id] ? '/liked.svg' : '/like.svg'"
                  alt="Like"
                  class="w-6 h-6 mt-1.5 duration-300 cursor-pointer"
                  :class="{ 'animate-like': isAnimating }"
                  @click.stop="toggleLike(item)"
                  @animationend="isAnimating = false"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Всплывающее окно -->
    <IdeaModal v-if="isModalOpen" @close="closeModal" @submit="addNewIdea" />
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue"; // Импортируем модальное окно

export default {
  components: { IdeaModal, Header },
  data() {
    return {
      isAnimating: false,
      items: [], // Список идей
      isModalOpen: false,
      likedItems: {}, // Объект для хранения лайков по каждому элементу
    };
  },
  methods: {
    async fetchIdeas() {
      try {
        const response = await fetch("http://localhost:8000/api/ideas/");
        if (!response.ok) throw new Error("Ошибка загрузки идей");
        this.items = await response.json();
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    viewItem(item) {
      this.$router.push(`/ideas/${item.id}`);
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    toggleLike(item) {
      this.likedItems = {
        ...this.likedItems, // создаем новый объект с обновленным состоянием лайка
        [item.id]: !this.likedItems[item.id], // Меняем состояние лайка для текущей строки
      };
      this.isAnimating = true;
    },
  },
  mounted() {
    this.fetchIdeas(); // Загружаем идеи при монтировании
  },
};
</script>

<style scoped>
@keyframes likeJump {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.4);
  }
  100% {
    transform: scale(1);
  }
}

.animate-like {
  animation: likeJump 0.3s ease-in-out;
}
</style>
