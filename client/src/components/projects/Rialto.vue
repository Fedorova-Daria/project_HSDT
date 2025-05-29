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
          class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none text-always-black border-zinc-400 duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md border-zinc-400 text-always-black duration-500"
      >
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>

      <select
        class="ml-5 h-10 py-2 px-3 border bg-white rounded-md text-always-black border-zinc-400 duration-500"
      >
        <option>Все навыки</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>

      <button
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
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
      >
        <div class="flipper bg-card">
          <IdeaCard :idea="idea" class="front " />
          <div class="back p-6 rounded-lg shadow-lg flex flex-col bg-card">
  <!-- Заголовок и лайки -->
  <div class="flex justify-between items-center mb-3">
    <h3 class="text-2xl font-semibold">
      Детали проекта
    </h3>
    <div class="flex items-center space-x-2">
      <span class="likes-count text-dynamic">
        {{ idea.likes ? idea.likes.length.toLocaleString() : 0 }}
      </span>


      <div
  class="heart-container"
  :style="{ '--heart-color': instituteStyle.likeColor }"
  title="Like"
  @click.stop="updateLike($event, idea)"
>
  <input
    type="checkbox"
    class="checkbox"
    :id="'like-checkbox-' + idea.id"
    :checked="idea.likes?.includes(userId)"
    @change.stop
  />
  <div class="svg-container">
    <svg
       width="30" height="30"
      viewBox="0 0 24 24"
      class="svg-outline"
      xmlns="http://www.w3.org/2000/svg"
      v-show="!isLikedByUser(idea)"
    >
      <path
        d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
        :stroke="likeColor"
      />
    </svg>
    <svg
     width="30" height="30"
      viewBox="0 0 24 24"
      class="svg-filled"
      xmlns="http://www.w3.org/2000/svg"
      v-show="isLikedByUser(idea)"
      :style="{ '--heart-color': instituteStyle.likeColor }"
    >
      <path
        d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"
      />
    </svg>
    <svg class="svg-celebrate" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="10,10 20,20"></polygon>
                    <polygon points="10,50 20,50"></polygon>
                    <polygon points="20,80 30,70"></polygon>
                    <polygon points="90,10 80,20"></polygon>
                    <polygon points="90,50 80,50"></polygon>
                    <polygon points="80,80 70,70"></polygon>
                </svg>
  </div>
</div>
    </div>
  </div>

  <!-- Описание — сразу под заголовком -->
  <p class="text-sl mb-4 line-clamp-3">
    {{ idea.description || "Описание отсутствует" }}
  </p>

  <!-- Кнопка "Узнать подробнее" — внизу -->
  <div class="mt-auto flex justify-end items-center">
    <button
      @click="openIdea(idea)"
      class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
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

    <IdeaModal v-if="isModalOpen" @close="closeModal" @submit="addNewIdea" />
  </div>
</template>

<script>
import { toggleLike } from "@/services/projects.js";
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
  data() {
    return {
      userId: JSON.parse(localStorage.getItem("userData") || "{}")?.id,
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
    likeColor() {
    const inst = this.globalState.institute;
    const style = instituteStyles[inst];
    return style?.likeColor || "red"; // Цвет лайка по умолчанию красный
  },

  isLikedByUser() {
    return (idea) => idea.likes?.includes(this.userId);
  },
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
    async updateLike(event, idea) {
  try {
    event.stopPropagation();

    // Вызов сервиса лайка (он должен возвращать обновлённую идею с актуальными likes)
    const updatedIdea = await toggleLike(
      idea,
      event,
      idea.likes.includes(this.userId),
      (state) => (this.isAnimating = state),
      () => this.userId
    );

    // Обновим локальный стейт идеи (лайки обновятся)
    this.updateIdeaLikes(updatedIdea);

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
.svg-container, svg {
  overflow: visible;
}
/* From Uiverse.io by catraco */ 
.heart-container {
  --heart-color: var(--heart-color);
  position: relative;
  width: 50px;
  height: 50px;
  transition: .3s;
}

.heart-container .checkbox {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 20;
  cursor: pointer;
}

.heart-container .svg-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.heart-container .svg-outline,
        .heart-container .svg-filled {
  fill: var(--heart-color);
  position: absolute;
}

.heart-container .svg-filled {
  animation: keyframes-svg-filled 1s;
  display: none;
}

.heart-container .svg-celebrate {
  position: absolute;
  animation: keyframes-svg-celebrate .5s;
  animation-fill-mode: forwards;
  display: none;
  stroke: var(--heart-color);
  fill: var(--heart-color);
  stroke-width: 2px;
}

.heart-container .checkbox:checked~.svg-container .svg-filled {
  display: block
}

.heart-container .checkbox:checked~.svg-container .svg-celebrate {
  display: block
}

@keyframes keyframes-svg-filled {
  0% {
    transform: scale(0);
  }

  25% {
    transform: scale(1.2);
  }

  50% {
    transform: scale(1);
    filter: brightness(1.5);
  }
}

@keyframes keyframes-svg-celebrate {
  0% {
    transform: scale(0);
  }

  50% {
    opacity: 1;
    filter: brightness(1.5);
  }

  100% {
    transform: scale(1.4);
    opacity: 0;
    display: none;
  }
}



.flip-container {
  perspective: 1000px;
  min-height: 250px;
  will-change: transform;
}

.flipper {
  transition: transform 0.6s ease-in-out;
}

.flip-container:hover .flipper {
  transform: rotateY(180deg);
  transition-delay: 0.2s;
}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 250px;
  backface-visibility: hidden;
  top: 0;
  left: 0;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.front {
  transform: rotateY(0deg);
  z-index: 2;
}

.back {
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

.likes-count {
  display: inline-block;
  width: 4ch;      /* фиксированная ширина в символах — под размер числа */
  text-align: right; /* число прижато вправо */
  white-space: nowrap;
}
</style>
