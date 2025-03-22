<template>
  <div>
    <Header />

    <div class="w-4/5 m-auto mt-6 text-white">
      <div class="flex m-auto mt-5 text-zinc-700">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none focus:border-purple-400 duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
  class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
>
  <option value="" disabled selected class="text-gray-500">Выберите институт</option>
  <option>ВШЦТ</option>
  <option>ИПТИ</option>
  <option>СТРОИН</option>
  <option>АРХИД</option>
</select>

<select
  class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
>
  <option value="" disabled selected class="text-gray-500">Сортировать по</option>
  <option>По новизне</option>
  <option>По популярности</option>
</select>


      <!-- Кнопка "Создать идею", отображается только если роль пользователя - "заказчик" -->
      <!-- Кнопка "Создать идею" теперь открывает модальное окно -->
      <button
        @click="openModal"
        class="bg-purple-600 text-white rounded-md px-4 py-2 hover:bg-purple-700 transition ml-5 h-10"
      >
        Создать идею
      </button>
    </div>
      <table
        class="w-full mt-5 border-collapse shadow-lg rounded-lg overflow-hidden bg-card table-auto"
      >
        <thead>
          <tr class="bg-card text-left">
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
                 @click="openIdeaDetail(item.id)"
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
    <transition
    name="slide"
    @before-enter="beforeEnter"
    @after-enter="afterEnter"
    @before-leave="beforeLeave"
    @after-leave="afterLeave"
  >
    <IdeaDetail
      v-show="selectedIdeaId"
      :ideaId="selectedIdeaId"
      @close="closeIdeaDetail"
    />
  </transition>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue"; // Импортируем модальное окно
import IdeaDetail from "@/components/projects/IdeaDetail.vue";
export default {
  components: { IdeaDetail, IdeaModal, Header },
  data() {
    return {
      isAnimating: false,
      items: [], // Список идей
      isModalOpen: false,
      likedItems: {}, // Объект для хранения лайков по каждому элементу
      selectedIdeaId: null, // id выбранной идеи
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
    openIdeaDetail(id) {
      this.selectedIdeaId = id;
    },
    closeIdeaDetail() {
      // Закрываем модальное окно и сбрасываем выбранное id
      this.selectedIdeaId = null;
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