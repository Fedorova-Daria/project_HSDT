<template>
  <div class="relative min-h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <!-- <ParallaxBackground />-->

    <!-- Затемнение фона (увеличена прозрачность) -->
    <!--<div class="absolute inset-0 bg-black opacity-50 -z-10"></div>-->

    <Header />

    <div class="w-4/5 m-auto mt-6 text-white relative z-0">
      <div class="flex m-auto mt-5 text-zinc-700">
        <div class="relative">
          <img class="absolute left-2 top-2" src="/search.svg" /> 
          <input
            v-model="searchQuery"
            class="w-full max-w-md border bg-white rounded-md py-2 pl-10 pr-4 outline-none duration-500"
            type="text"
            placeholder="Поиск..."
          />
        </div>
        <select v-model="sortOption"
          class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
        >
          <option value="" disabled selected class="text-gray-500">
            Сортировать по
          </option>
          <option value="new">По новизне</option>
          <option  value="popular">По популярности</option>
        </select>

        <button
          v-if="userRole === 'ST'"
          @click="openModal"
          class="text-always-white rounded-md px-4 py-2 transition ml-5 h-10"
          :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
        >
          Создать идею
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
            'text-zinc-200 opacity-70 hover:text-white':
              activeFilter !== filter.value,
          }"
        >
          {{ filter.label }}
          <!-- Анимированная полоска -->
          <span
            class="absolute left-1/2 bottom-0 h-0.5 transition-all duration-300 rounded-lg"
            :style="{ backgroundColor: currentBgColor }"
            :class="{
              'w-full left-0': activeFilter === filter.value,
              'w-0': activeFilter !== filter.value,
            }"
          >
          </span>
        </button>
      </div>

      <IdeasTable
        :items="finalFilteredItems"
        :userId="userData.id"
        @toggle-like="updateLike"
        @open-idea="openIdea"
      />
    </div>

    <!-- Всплывающее окно -->
    <IdeaModal
      v-if="isModalOpen"
      @close="closeModal"
      @submit="submitIdea(status)"
    />
  </div>
</template>

<script>
import IdeasTable from "@/components/projects/IdeasTable.vue";
import Header from "@/components/header.vue";
import IdeaModal from "@/components/projects/IdeaModal.vue";
import { fetchOwnerName, toggleLike } from "@/services/ideas.js";
import { instituteStyles } from "@/assets/instituteStyles.js";
import api from "@/composables/auth";
import Cookies from "js-cookie";
import ParallaxBackground from "@/components/ParallaxBackground.vue";
import UserService from "@/composables/storage.js";

export default {
  inject: ["globalState"], // Подключаем глобальное состояние
  components: { IdeaModal, Header, IdeasTable, ParallaxBackground },
  data() {
    return {
      sortOption: "",
      currentBgColor: "",
      searchQuery: '',
      userRole: null,
      userData: {}, // Изначально пустой объект
      isAnimating: false,
      items: [], // Список идей
      filteredItems: [], // Отфильтрованные идеи
      filters: [], // Изначально пустой массив
      activeFilter: "all", // Начальный фильтр
      isModalOpen: false,
      likedItems: {}, // Объект для хранения лайков по каждому элементу
    };
  },
  computed: {
    finalFilteredItems() {
    let result = this.filteredItems.filter((idea) =>
      idea.title.toLowerCase().includes(this.searchQuery.toLowerCase())
    );

    if (this.sortOption === "new") {
      result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    } else if (this.sortOption === "popular") {
      result.sort((a, b) => b.likes.length - a.likes.length);
    }

    return result;
  },
    liked() {
      return (idea) => {
        const userData = this.userData; // Используем загруженные userData
        return idea.likes.includes(userData.id);
      };
    },
    selectedInstitute() {
      return this.globalState.institute; // Глобальное состояние для чтения
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute]; // Используем глобальное состояние
      return style || { buttonOffColor: "#ccc" }; // Дефолтный стиль
    },
  },
  created() {
    this.userRole = UserService.getUserRole(); // Устанавливаем значение из Cookies
    // Динамически формируем фильтры на основе роли
    if (["CU", "EX"].includes(this.userRole)) {
      this.filters = [
        { label: "Все", value: "all" },
        { label: "Любимые", value: "favorites" },
      ];
    } else if (this.userRole === "ST") {
      this.filters = [
        { label: "Все", value: "all" },
        { label: "Мои", value: "my" },
        { label: "Любимые", value: "favorites" },
        { label: "Черновики", value: "drafts" },
      ];
    }
  },
  methods: {
    // Устанавливаем активный фильтр
    setFilter(filter) {
      this.activeFilter = filter;
      this.filterItems(); // Заменили applyFilter на filterItems
    },
    // Применяем фильтрацию
    filterItems() {
      // Используем activeFilter, а не filter, так как filter - это параметр метода setFilter
      if (this.activeFilter === "all") {
        this.filteredItems = this.items.filter(
          (idea) => idea.status !== "draft"
        );
      } else if (this.activeFilter === "my") {
        this.filteredItems = this.items.filter(
          (idea) => idea.owner === this.userData.id
        );
      } else if (this.activeFilter === "favorites") {
        this.filteredItems = this.items.filter((idea) =>
          idea.likes.includes(this.userData.id)
        );
      } else if (this.activeFilter === "drafts") {
        this.filteredItems = this.items.filter(
          (idea) => idea.status === "draft" && idea.owner === this.userData.id
        );
      } else {
        this.filteredItems = []; // Если роль неизвестна, ничего не показываем
      }
    },
    async fetchIdeas() {
      try {
        const response = await api.get("/ideas/");
        this.items = response.data;
        this.filterItems(); // Применяем фильтрацию сразу после загрузки идей
        // Загружаем инициаторов для каждой идеи
        for (const idea of this.items) {
          if (idea.owner) {
            await fetchOwnerName(idea, idea.owner);
          }
        }
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    async updateLike(idea, event) {
      try {
        // Передаем все необходимые параметры в утилиту
        await toggleLike(
          idea, // текущая идея
          event, // событие клика
          this.liked(idea), // текущее состояние лайка
          (state) => (this.isAnimating = state), // установка анимации
          () => this.userData.id // получение userId из загруженных данных
        );
      } catch (error) {
        console.error("Ошибка при обновлении лайка:", error);
      }
    },
    openIdea(idea) {
      const institute = this.selectedInstitute; // Используем selectedInstitute из data()
      if (institute) {
        this.$router.push({ path: `/${institute}/idea/${idea.id}` });
      } else {
        console.error("Институт не выбран");
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
  mounted() {
    this.fetchIdeas(); // Загружаем идеи при монтировании

    // Загружаем данные пользователя, если они есть в cookies
    const storedUser = Cookies.get("userData");
    if (storedUser) {
      try {
        this.userData = JSON.parse(storedUser); // Пробуем распарсить userData
      } catch (error) {
        console.error("Ошибка при парсинге userData:", error);
        this.userData = {}; // Если ошибка, устанавливаем пустой объект
      }
    } else {
      console.warn("User data not found in cookies.");
      this.userData = {}; // Если данных нет, устанавливаем пустой объект
    }
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
button span {
  transform: translateX(-50%);
}
/* Стили для параллакс-эффекта */
.transform-gpu {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

.filter {
  filter: blur(8px);
}

/* Затемнение фона (увеличено до opacity-50) */
.bg-black {
  background-color: rgba(0, 0, 0, 0.5);
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

/* Убедитесь, что контент поверх фона */
.relative.z-10 {
  position: relative;
  z-index: 10;
}

/* Стили для карточек */
.bg-card {
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: all 0.2s ease;
}

/* Стили для кнопок */
.bg-buttonoff {
  background-color: rgba(107, 33, 168, 0.7);
}
.bg-buttonoff:hover {
  background-color: rgba(107, 33, 168, 0.9);
}
</style>
