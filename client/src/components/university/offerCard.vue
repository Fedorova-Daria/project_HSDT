<template>
  <div
    class="offer-card border bg-card rounded-2xl p-5 shadow-lg cursor-pointer"
    @click="openoffer(offer)"
  >
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-dynamic">{{ offer.title }}</h1>
      <div class="flex items-center">
        <img
  :src="liked ? '/liked.svg' : '/like.svg'"
  alt="Like"
  class="w-6 h-6 mr-2 duration-300 cursor-pointer"
  :class="{ 'animate-like': isAnimating }"
  @click.stop="updateLike"
/>
        <span class="text-dynamic">{{ offer.likes.length }}</span> 
      </div>
    </div>

    <p class="texth2-dynamic mb-3 truncate-text">
  {{ offer.description || "Описание отсутствует" }}
</p>

    <div class="mt-auto">
      <h3 class="text-xl text-dynamic mb-3">
        Инициатор: {{ offer.initiator || "Неизвестный автор" }}
      </h3>
    </div>

    <div v-if="userRole === 'EX' && userRole === 'CU'" class="text-dynamic mt-2">
      Голосов экспертов: {{ offer.expert_likes.length }}
    </div>
  </div>
</template>

<script>
import { fetchOwnerName, toggleOfferLike } from "@/services/projects.js";
import Cookies from "js-cookie";
import UserService from "@/composables/storage.js";
export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  props: {
    offer: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isAnimating: false, // Для анимации лайка
      userRole: null, // Здесь инициализируем userRole
    };
  },
  created() {
    this.userRole = UserService.getUserRole(); // Устанавливаем значение из Cookies
  },
  computed: {
    liked() {
    if (!this.offer || !this.offer.likes) return false;
    const userData = JSON.parse(Cookies.get("userData") || "{}");
    return this.offer.likes.includes(userData.id);
    },
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    expertsVotesCount() {
      // Реактивно вычисляем количество голосов экспертов
      return this.offer.experts_voted_count || 0;
    },
  },
  mounted() {
    this.loadOwnerName(); // Загружаем инициатора на этапе монтирования
  },
  methods: {
    openoffer(offer) {
  const institute = this.selectedInstitute; // Используем selectedInstitute из data()
  if (institute) {
    this.$router.push({ path: `/${institute}/offer/${offer.id}` });
  } else {
    console.error("Институт не выбран");
  }
  },
    async loadOwnerName() {
      try {
        // Передаем текущую идею и ID владельца в функцию из утилит
        await fetchOwnerName(this.offer, this.offer.owner);
      } catch (error) {
        console.error("Ошибка при загрузке имени владельца:", error);
      }
    },
    async updateLike(event) {
  try {
    await toggleOfferLike(
      this.offer,
      event,
      this.liked,
      (state) => (this.isAnimating = state),
      () => JSON.parse(Cookies.get("userData") || "{}")?.id
    );
  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);
  }
}
  },
};
</script>

<style scoped>
.truncate-text {
  display: -webkit-box; /* Используем flex-контейнер */
  -webkit-line-clamp: 2; /* Ограничиваем текст двумя строками */
  -webkit-box-orient: vertical; /* Задаём направление контейнера */
  overflow: hidden; /* Скрываем выходящий текст */
  text-overflow: ellipsis; /* Добавляем "..." для обрезанного текста */
  word-wrap: break-word; /* Перенос слов при необходимости */
}
/* Анимация лайка */
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
