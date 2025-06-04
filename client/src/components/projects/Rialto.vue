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
      <select class="ml-5 h-10 py-2 px-3 border bg-white rounded-md border-zinc-400 text-always-black duration-500">
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>

      <select class="ml-5 h-10 py-2 px-3 border bg-white rounded-md text-always-black border-zinc-400 duration-500">
        <option>Все навыки</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>

      <button
      v-if="userRole === 'EX' || userRole === 'CU'"
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
        :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      >
        Создать идею
      </button>
      <button
      @click="openBank"
      v-if="userRole === 'EX'"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
        :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      >
        Банк проектов
      </button>
    </div>

    <!-- Фильтры с анимацией -->
    <div class="flex justify-center space-x-6 relative mt-3">
      <button
        v-for="(filter, index) in filters"
        :key="index"
        @click="setFilter(filter.value)"
        class="relative pb-1 text-lg font-medium transition-colors duration-300"
        :class="{
          'text-white': activeFilter === filter.value,
          'text-zinc-200 opacity-70 hover:text-white': activeFilter !== filter.value,
        }"
      >
        {{ filter.label }}
        <!-- Анимированная полоска -->
        <span
  class="absolute bottom-0 h-0.5 transition-all duration-300 rounded-lg"
  :style="{
    backgroundColor: currentBgColor,
    left: activeFilter === filter.value ? '0' : '50%',
    width: activeFilter === filter.value ? '100%' : '0'
  }"
/>
      </button>
    </div>

    <div v-for="group in filteredIdeas" :key="group.year" class="mb-10 w-4/5 m-auto">
      <h2 class="text-4xl font-bold mb-3 mt-4">
        {{ group.year }} год
      </h2>
      <hr class="divider" />

      <div v-for="semesterKey in ['winter', 'spring']" :key="semesterKey">
        <div v-if="group[semesterKey] && group[semesterKey].length > 0">
        <h3 class="text-2xl font-semibold mb-2 mt-2">
          {{ semesterDisplay(semesterKey) }} семестр
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-5">
          <div v-for="idea in group[semesterKey]" :key="idea.id" class="flip-container w-full h-full">
            <div class="flipper bg-card h-full">
              <div class="front p-6 rounded-lg shadow-lg flex flex-col bg-card h-full">
      <h3 class="text-2xl font-semibold mb-3">
        {{ idea.title }}
      </h3>
      <div class="flex">
  <span class="bg-gray-200 text-sm text-gray-700 px-2 py-1 rounded-full"
  :style="{ backgroundColor: statusStyleMap[idea.status]?.bg || '#eee' }">
    {{ statusStyleMap[idea.status]?.label || idea.status }}
  </span>
</div>

    <!-- Нижняя часть -->
    <div class="mt-auto">
      <div class="flex flex-wrap gap-2 mt-2 mb-4">
    <!-- Выводим первые 10 технологий -->
    <span
      v-for="tech in idea.skills_required.slice(0, 10)"
      :key="tech.id"
      class="bg-gray-200 text-sl text-gray-700 px-2 py-1 rounded-full"
    >
      {{ tech.name }}
    </span>

    <!-- Если технологий больше 10, показываем +N -->
    <span
      v-if="idea.skills_required.length > 10"
      class="bg-gray-300 text-sm text-gray-700 px-2 py-1 rounded-full cursor-default"
    >
      +{{ idea.skills_required.length - 10 }}
    </span>
  </div>

      <h3 class="text-lg text-dynamic mb-1">
        Инициатор: {{ idea.initiator.full_name || "Неизвестный автор" }}
      </h3>

      <div
        v-if="userRole === 'EX' || userRole === 'CU'"
        class="text-sl text-dynamic"
      >
        Голосов экспертов: {{ idea.expert_likes.length }}
      </div>
    </div>
    </div>
              

              <!-- BACK -->
              <div class="back p-6 rounded-lg shadow-lg flex flex-col bg-card h-full">
                <!-- Заголовок и лайки -->
                <div class="flex justify-between items-center mb-3">
                  <h3 class="text-2xl font-semibold">Детали проекта</h3>
                  <div class="flex items-center space-x-2">
                    <span class="likes-count text-dynamic">
                      {{ totalLikes(idea) }}
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
                        :checked="isLikedByUser(idea)"
                        @change.stop
                      />
                      <div class="svg-container">
                        <svg
                          width="30"
                          height="30"
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
                          width="30"
                          height="30"
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

                <!-- Описание -->
                <p class="text-sl mb-4 line-clamp-3">
                  {{ idea.description || "Описание отсутствует" }}
                </p>

                <!-- Кнопка -->
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
              <!-- END .back -->
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
import { toggleLike } from "@/services/projects.js";
import Cookies from "js-cookie";
import api from "@/composables/auth";
import axios from "axios";
import IdeaCard from "@/components/RialtoCard1.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue";
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import UserService from "@/composables/storage.js";
import { debounce } from 'lodash';

export default {
  inject: ["globalState"],
  components: { IdeaCard, IdeaModal, Header },
  data() {
    return {
      userId: JSON.parse(localStorage.getItem("userData") || "{}")?.id,
      isAnimating: false, // Для анимации лайка
      userRole: null,
      currentBgColor: "",
      visibleIdeas: [],  // идеи с visible=true (для Все и Понравившиеся)
      allIdeas: [],      // все идеи (для Мои)
      editedIdea: {},
      isEditing: false,
statusStyleMap: {
  draft: { label: "Черновик", bg: "#f3f4f6" },             // серый
  review: { label: "На проверке", bg: "#fff3cd" },          // жёлтый
  open: { label: "Открыт", bg: "#d4edda" },      // зелёный
  rejected: { label: "Отклонено", bg: "#e2e3e5" },          // серый светлый
  under_revision: {label: "На доработке", bg: "#FDB89A"},
  done: {label: "Сделан", bg: "#A1FFB7"},
  new: {label: "На проверке у дирекции", bg: "#FFE1A1"},
  under_revision_on_admin: {label: "На доработке у дирекции", bg: "#FFA4A1"},
},
      filters: [
      { label: "Все", value: "all" },
      { label: "Понравившиеся", value: "liked" },
      { label: "Мои", value: "mine" }
    ],
    activeFilter: 'all',

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
  mounted() {
  this.loadVisibleIdeas()
  this.loadAllIdeas()
},
  created() {
    this.userRole = UserService.getUserRole();
  },
  computed: {
    filteredIdeas() {
    if (this.activeFilter === 'liked') {
      return this.visibleIdeas.map(group => ({
        year: group.year,
        spring: group.spring.filter(idea => idea.likes?.includes(this.userId)),
        winter: group.winter.filter(idea => idea.likes?.includes(this.userId))
      })).filter(group => group.spring.length || group.winter.length)
    } else if (this.activeFilter === 'mine') {
      // из allIdeas фильтруем по owner (или эксперту)
      return this.allIdeas.map(group => ({
        year: group.year,
        spring: group.spring.filter(idea => 
          (this.userRole === 'CU' && idea.owner?.id === this.userId) ||
          (this.userRole === 'EX' && idea.owner?.id === this.userId)),
        winter: group.winter.filter(idea => 
          (this.userRole === 'CU' && idea.owner?.id === this.userId) ||
          (this.userRole === 'EX' && idea.owner?.id === this.userId))
      })).filter(group => group.spring.length || group.winter.length)
    } else {
      // activeFilter === 'all'
      return this.visibleIdeas
    }
  },
    likeColor() {
    const inst = this.globalState.institute;
    const style = instituteStyles[inst];
    return style?.likeColor || "red"; // Цвет лайка по умолчанию красный
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
  semesterDisplay() {
    return (code) => {
      if (code === 'spring') return 'Весенний';
      if (code === 'winter') return 'Зимний';
      return code;
    };
  }
  },
  methods: {
    totalLikes(idea) {
    const userLikes = idea.likes ? idea.likes.length : 0;  // Количество лайков от пользователей
    const expertLikes = idea.expert_likes ? idea.expert_likes.length : 0;  // Количество лайков от экспертов
    return (userLikes + expertLikes).toLocaleString();  // Суммируем и форматируем
  },
    isLikedByUser(idea) {
  if (!this.userId) return false; // Если нет пользователя, то не лайкнул

  // Проверяем, если пользователь есть в обычных лайках
  if (idea.likes && idea.likes.includes(this.userId)) {
    return true;
  }

  // Проверяем, если пользователь есть в лайках эксперта
  if (idea.expert_likes && Array.isArray(idea.expert_likes)) {
    return idea.expert_likes.some(expert => expert.id === this.userId);
  }

  return false; // Если не найдено
},
    async loadVisibleIdeas() {
    const institute = this.selectedInstitute;
const res = await api.get('/projects/grouped_by_semester/', {
  params: {
    visible: true,
    institute: institute
  }
});
this.visibleIdeas = res.data;
  },
  async loadAllIdeas() {
    const res = await api.get('/projects/grouped_by_semester/')
    this.allIdeas = await res.data;
  },
  setFilter(value) {
    this.activeFilter = value
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
    openBank() {
      const institute = this.selectedInstitute; // Используем selectedInstitute из data()
      if (institute) {
        this.$router.push({ path: `/${institute}/projectbank/` });
      } else {
        console.error("Институт не выбран");
      }
    },
updateLike: debounce(async function (event, idea) {
    try {
      event.stopPropagation();

      const isExpert = this.userRole === "EX";
      const isCustomerOrStudent = this.userRole === "CU" || this.userRole === "ST";

      const updatedIdea = await toggleLike(
        idea,
        event,
        idea.likes.includes(this.userId),
        (state) => (this.isAnimating = state),
        () => this.userId,
        false,
        isExpert,
        isCustomerOrStudent
      );
      this.loadVisibleIdeas();
      // Обновим нужную коллекцию
      const targetArray = this.activeFilter === 'mine' ? this.allIdeas : this.visibleIdeas;

      for (const group of targetArray) {
        for (const sem of ['spring', 'winter']) {
          const index = group[sem].findIndex(i => i.id === updatedIdea.id);
          if (index !== -1) {
            group[sem].splice(index, 1, { ...updatedIdea });
            break;
          }
        }
      }
    } catch (error) {
      console.error("Ошибка при обновлении лайка:", error);
    }
  }),
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
  overflow: visible;
  clip-path: inset(0 round 12px);
  position: relative;
}

.flipper {
  width: 100%;
  height: 100%;
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
  z-index: 1;
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

.divider {
  border: none;
  height: 1px; /* Толщина линии */
  background-color: #5f5f5f; /* Цвет линии */
  margin: 1rem 0; /* Отступы сверху и снизу */
  opacity: 0.8;
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
