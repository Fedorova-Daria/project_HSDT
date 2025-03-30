<template>
  <div
    class="idea-card border border-zinc-700 bg-card rounded-xl p-5 shadow-lg cursor-pointer"
    @click="openIdea"
  >
    <div class="flex justify-between items-center mb-3">
      <h1 class="text-2xl font-semibold text-white">{{ idea.name }}</h1>
      <div class="flex items-center">
        <img
          :src="liked ? '/liked.svg' : '/like.svg'" 
          alt="Like"
          class="w-6 h-6 mr-2 duration-300 cursor-pointer"
          :class="{ 'animate-like': isAnimating }"
          @click.stop="toggleLike"
          @animationend="isAnimating = false"
        />
        <span class="text-white">{{ idea.likes_count }}</span> 
      </div>
    </div>

    <p class="text-gray-300 mb-3">
      {{ idea.short_description || "Описание отсутствует" }}
    </p>

    <div class="mt-auto">
      <h3 class="text-xl text-white mb-3">
        Инициатор: {{ idea.initiator || "Неизвестный автор" }}
      </h3>
    </div>

    <div v-if="userRole === 'EX'" class="text-white mt-2">
      Голосов экспертов: {{ idea.experts_voted_count }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { fetchAccessToken } from "@/utils/auth.js";

export default {
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isAnimating: false, // Для анимации лайка
      userRole: localStorage.getItem("role") || "ST",
      ownerName: "", // Сюда сохраним имя инициатора
    };
  },
  computed: {
    liked() {
      if (!this.idea || !this.idea.likes) return false; // Проверяем, есть ли данные
      let userData = JSON.parse(localStorage.getItem("userData")) || {}; 
      return this.idea.likes.includes(userData.id);  // Проверка на наличие ID пользователя в массиве лайков
    }
  },
  mounted() {
    this.fetchOwnerName(this.idea.owner);  // передаем ID владельца
  },
  methods: {
    async fetchOwnerName(ownerId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/users/${ownerId}/`);
        // Проверяем данные пользователя, и если они есть, формируем имя
        if (response.data.first_name && response.data.last_name) {
          this.idea.initiator = `${response.data.first_name} ${response.data.last_name}`;
        } else {
          this.idea.initiator = "Неизвестный автор";
        }
      } catch (error) {
        console.error("Ошибка при загрузке инициатора:", error);
        this.idea.initiator = "Неизвестный автор";  // Если не удается получить данные
      }
    },
    openIdea() {
      this.$router.push(`/ideas/${this.idea.id}`);
    },
    async toggleLike(event, retry = false) {
      event.stopPropagation();
      this.isAnimating = true;  // Запускаем анимацию лайка

      try {
        let accessToken = localStorage.getItem("access");

        if (!accessToken) {
          accessToken = await fetchAccessToken();
          if (!accessToken) {
            console.error("Не удалось обновить токен. Авторизация требуется.");
            return;
          }
        }

        const response = await axios.post(
          `http://localhost:8000/api/projects/${this.idea.id}/like/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Обновляем состояние лайка и количество лайков
        if (this.liked) {
          this.idea.likes = this.idea.likes.filter(id => id !== this.getUserId());
        } else {
          this.idea.likes.push(this.getUserId());
        }
        this.idea.likes_count = response.data.likes_count;

      } catch (error) {
        console.error("Ошибка при обновлении лайка:", error);

        if (error.response?.status === 403 && !retry) {
          console.log("Попытка обновления токена...");
          const newToken = await fetchAccessToken();
          if (newToken) {
            localStorage.setItem("access", newToken);
            this.toggleLike(event, true);
          } else {
            console.error("Не удалось обновить токен, требуется повторный вход.");
          }
        }
      } finally {
        setTimeout(() => {
          this.isAnimating = false;  // Завершаем анимацию через 300 мс
        }, 300);
      }
    },
    getUserId() {
      let userData = JSON.parse(localStorage.getItem("userData")) || {}; 
      return userData.id;
    }
  },
};
</script>

<style scoped>
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
