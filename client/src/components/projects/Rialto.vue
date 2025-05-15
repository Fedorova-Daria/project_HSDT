<template>
  <div>
    <Header @institute-changed="onInstituteChanged" />

    <h1 class="font-display w-4/5 m-auto mt-20 text-dynamic text-5xl">
      Биржа проектов {{ instituteName }}
    </h1>

    <div class="flex w-4/5 m-auto mt-5">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          v-model="searchQuery"
          class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none border-zinc-400 duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md border-zinc-400 duration-500"
      >
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>

      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md border-zinc-400 duration-500"
      >
        <option>Все стеки технологий</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>

      <button
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-white"
        :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      >
        Создать идею
      </button>
    </div>

    <div
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-4/5 m-auto mt-20"
    >
      <div
        v-for="idea in filteredIdeas"
        :key="idea.id"
        class="flip-container"
        :style="{ '--border-color': instituteStyle.textColor }"
      >
        <div class="flipper">
          <IdeaCard :idea="idea" class="front" />
          <div class="back bg-white p-6 rounded-lg shadow-lg flex">
            <div class="flex justify-between items-center mb-3">
              <h3
                class="flex justify-between items-center mb-3 text-2xl font-semibold"
              >
                Детали проекта
              </h3>
              <div class="flex items-center">
                <span class="text-dynamic">{{
                  idea.likes ? idea.likes.length : 0
                }}</span>
                <img
                  :src="liked ? '/liked.svg' : '/like.svg'"
                  alt="Like"
                  class="w-6 h-6 mr-2 duration-300 cursor-pointer"
                  :class="{ 'animate-like': isAnimating }"
                  @click.stop="updateLike"
                />
              </div>
            </div>
            <p class="text-gray-600 text-sm mb-4">
              {{ idea.description || "Описание отсутствует" }}
            </p>
            <div class="space-y-2 text-sm">
              <div class="flex items-center">
                <span class="mr-2">👤</span>
                <span>{{ idea.author || "Автор не указан" }}</span>
              </div>
              <div class="flex items-center">
                <span class="mr-2">📞</span>
                <span>{{ idea.contacts || "Контакты не указаны" }}</span>
              </div>
              <div class="flex items-center">
                <span class="mr-2">💻</span>
                <span
                  >Стек:
                  {{ idea.technologies?.join(", ") || "Не указан" }}</span
                >
                <button
                  @click="openIdea(idea)"
                  class="rounded-md px-4 py-2 transition ml-5 h-10 text-white"
                  :style="{ backgroundColor: currentBgColor }"
                  @mouseover="currentBgColor = instituteStyle.buttonOnColor"
                  @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
                >
                  Узнать подробнее
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <IdeaModal v-if="isModalOpen" @close="closeModal" @submit="addNewIdea" />
  </div>
</template>

<script>
import toggleLike from "@/services/projects.js";
import Cookies from "js-cookie";
import axios from "axios";
import IdeaCard from "@/components/RialtoCard1.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue";
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import UserService from "@/composables/storage.js";

export default {
  inject: ["globalState"],
  components: { IdeaCard, IdeaModal, Header },
  props: {
    idea: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isAnimating: false, // Для анимации лайка
      userRole: null,
      currentBgColor: "",
      ideas: [],
      editedIdea: {},
      isEditing: false,

      searchQuery: "",
      isModalOpen: false,
      hover: false,
      instituteNames: {
        HSDT: "ВШЦТ",
        ARCHID: "АРХИД",
        IPTI: "ИПТИ",
        STROIN: "СТРОИН",
        TYIU: "ТИУ",
      },
    };
  },
  created() {
    this.userRole = UserService.getUserRole();
    this.fetchCustomerIdeas();
  },
  computed: {
    liked() {
      if (!this.idea || !this.idea.likes) return false;
      const userData = JSON.parse(Cookies.get("userData") || "{}");
      return this.idea.likes.includes(userData.id);
    },
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
    instituteName() {
      return (
        this.instituteNames[this.selectedInstitute] || "Неизвестный институт"
      );
    },
    filteredIdeas() {
      if (!this.searchQuery) return this.ideas;
      return this.ideas.filter((idea) =>
        idea.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchCustomerIdeas() {
      try {
        const response = await axios.get("http://localhost:8000/api/projects/");
        this.ideas = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    updateIdeaLikes(updatedIdea) {
      const index = this.ideas.findIndex((idea) => idea.id === updatedIdea.id);
      if (index !== -1) {
        this.ideas[index] = { ...updatedIdea };
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    addNewIdea(newIdea) {
      console.log("Новая идея:", newIdea);
      this.isModalOpen = false;
    },
    onInstituteChanged(newInstitute) {
      this.globalState.institute = newInstitute;
    },
    openIdea(idea) {
      const institute = this.selectedInstitute; // Используем selectedInstitute из data()
      if (institute) {
        this.$router.push({ path: `/${institute}/project/${idea.id}` });
      } else {
        console.error("Институт не выбран");
      }
    },
    async updateLike(event) {
      try {
        await toggleLike(
          this.idea,
          event,
          this.liked,
          (state) => (this.isAnimating = state),
          () => this.currentUser?.id
        );
      } catch (error) {
        console.error("Ошибка при обновлении лайка:", error);
      }
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
};
</script>

<style scoped>
.flip-container {
  perspective: 1000px;
  min-height: 300px;
  will-change: transform;
}

.flipper {
  transition: transform 0.6s ease-in-out;
  transform-style: preserve-3d;
  position: relative;
}

.flip-container:hover .flipper {
  transform: rotateY(180deg);
  transition-delay: 0.2s;
}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 300px;
  backface-visibility: hidden;
  top: 0;
  left: 0;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  border: 2px solid var(--border-color, #e9ecef);
  transition: all 0.3s ease;
}

.front {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  transform: rotateY(0deg);
  z-index: 2;
}

.back {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transform: rotateY(180deg);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.flip-container:not(:hover) .flipper {
  transition: transform 0.6s ease-in-out 0.1s;
}

@media (max-width: 768px) {
  .flip-container {
    perspective: 500px;
  }

  .flipper {
    transition-duration: 0.4s;
  }
}

.text-dynamic {
  color: v-bind("instituteStyle.textColor");
}

.border-zinc-400 {
  border-color: rgba(161, 161, 170, 0.5);
}

.hover\:bg-opacity-80:hover {
  opacity: 0.8;
}
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
