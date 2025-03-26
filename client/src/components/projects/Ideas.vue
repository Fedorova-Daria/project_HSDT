<template>
  <div class="relative min-h-screen overflow-hidden">
    <!-- Размытый фон с параллакс-эффектом -->
    <img
      ref="backgroundImage"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105 -z-10"
      src="/bgg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />

    <!-- Затемнение фона (увеличена прозрачность) -->
    <div class="absolute inset-0 bg-black opacity-50 -z-10"></div>

    <Header />

    <div class="w-4/5 m-auto mt-6 text-white relative z-0">
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
<option value="" disabled selected class="text-gray-500">
            Выберите институт
          </option>
  <option>ВШЦТ</option>
  <option>ИПТИ</option>
  <option>СТРОИН</option>
  <option>АРХИД</option>
</select>

<select
  class="ml-5 h-10 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
>
<option value="" disabled selected class="text-gray-500">
            Сортировать по
          </option>
  <option>По новизне</option>
  <option>По популярности</option>
</select>


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
                 @click="openIdea(item)"
                class="px-4 py-2 text-sm font-medium bg-buttonoff hover:bg-buttonon rounded transition"
              >
                Посмотреть
              </button>
              <div class="flex items-center gap-2 min-w-[80px] justify-end">
                <h1 class="text-white font-semibold">{{ item.likeCount || 0 }}</h1>
                <img
  :src="likedItems[item.id] ? '/liked.svg' : '/like.svg'"
  :class="{ 'animate-like': item.isAnimating }"
  @click.stop="toggleLike(item)"
  @animationend="item.isAnimating = false"
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
export default {
  components: { IdeaModal, Header },
  data() {
    return {
      isAnimating: false,
      items: [], // Список идей
      isModalOpen: false,
      likedItems: {}, // Объект для хранения лайков по каждому элементу
      // Данные для параллакс-эффекта
      offsetX: 0,
      offsetY: 0,
      targetX: 0,
      targetY: 0,
      mouseX: 0,
      mouseY: 0,
      windowWidth: 0,
      windowHeight: 0,
      animationFrame: null,
    };
  },
  methods: {
    // Инициализация параллакс-эффекта
    initParallax() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
      window.addEventListener("mousemove", this.handleMouseMove);
      window.addEventListener("resize", this.handleResize);
      this.animate();
    },

    handleMouseMove(e) {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;

      // Вычисляем смещение относительно центра экрана (от -1 до 1)
      const x = (e.clientX / this.windowWidth - 0.5) * 2;
      const y = (e.clientY / this.windowHeight - 0.5) * 2;

      // Устанавливаем целевые координаты с коэффициентом
      const coefficient = 30;
      this.targetX = x * coefficient;
      this.targetY = y * coefficient;
    },

    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },

    animate() {
      // Интерполяция с коэффициентом плавности
      const smoothness = 0.08;
      this.offsetX += (this.targetX - this.offsetX) * smoothness;
      this.offsetY += (this.targetY - this.offsetY) * smoothness;

      this.animationFrame = requestAnimationFrame(this.animate);
    },

    cleanupParallax() {
      window.removeEventListener("mousemove", this.handleMouseMove);
      window.removeEventListener("resize", this.handleResize);
      if (this.animationFrame) {
        cancelAnimationFrame(this.animationFrame);
      }
    },

    async fetchIdeas() {
      try {
        const response = await fetch("http://localhost:8000/api/ideas/");
        if (!response.ok) throw new Error("Ошибка загрузки идей");
        this.items = await response.json();
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },
    openIdea(item) {
  this.$router.push({ path: `/ideas/${item.id}` });
},
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    toggleLike(item) {
  this.$set(this.likedItems, item.id, !this.likedItems[item.id]);
  this.$set(item, "isAnimating", true);
},
  },
  mounted() {
    this.fetchIdeas(); // Загружаем идеи при монтировании
    this.initParallax();
  },

  beforeDestroy() {
    this.cleanupParallax();
  },
};
</script>

<style scoped>
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
  background-color: rgba(0, 0, 0, 0.8);
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
  background-color: rgba(30, 30, 30, 0.8);
  backdrop-filter: blur(5px);
}

/* Стили для кнопок */
.bg-buttonoff {
  background-color: rgba(107, 33, 168, 0.7);
}
.bg-buttonoff:hover {
  background-color: rgba(107, 33, 168, 0.9);
}
</style>
