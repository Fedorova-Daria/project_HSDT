<template>
  <div>
    <Header @institute-changed="onInstituteChanged" />

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
      <button
        @click="openModal"
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-always-white"
        :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      >
        Создать предложение
      </button>
    </div>

    <!-- Обновленные карточки -->
    <div
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-4/5 m-auto mt-10"
    >
      <div
        v-for="offer in filteredoffers"
        :key="offer.id"
        class="flip-container"
      >
        <div class="flipper">
  <!-- Лицевая сторона -->
  <div class="front bg-card p-6 rounded-lg shadow-lg flex flex-col h-full">
    <h3 class="text-xl font-semibold mb-2 truncate-text">
      {{ offer.title }}
    </h3>

    <div class="flex items-center mb-4">
      <span class="text-sm opacity-70 ">
        {{ offer.owner.full_name || "Автор не указан" }}
      </span>
    </div>

    <div class="flex items-center mb-4 gap-4">
      <span class="text-sm p-1 rounded-2xl px-2 text-always-black"
      :style="{ backgroundColor: statusStyleMap[offer.status]?.bg || '#eee' }"
      >
        {{ statusStyleMap[offer.status]?.label || offer.status }}
      </span>
      <span class="text-sm p-1 rounded-2xl px-2 bg-zinc-500 font-semibold text-always-white"
      >
        {{ offer.offer_type || "Прочее" }}
      </span>
    </div>

    <p class="opacity-70 text-sm mb-4 truncate-text">
      {{ offer.description || "Описание отсутствует" }}
    </p>

    <!-- Лайки внизу карточки -->
    <div class="mt-auto pt-4 flex items-center justify-between border-t border-gray-200">
      <span class="text-dynamic font-medium">
        {{ offer.likes?.length || 0 }} лайков
      </span>
    </div>
  </div>


          <!-- Обратная сторона -->
          <div class="back bg-card p-6 rounded-lg shadow-lg flex flex-col">
            <div class="flex justify-between">
  <h3 class="text-xl font-semibold mb-4 flex justify-between">Детали предложения</h3>
  <!-- Лайк -->
  <div
    class="heart-container mb-4 self-start"
    :style="{ '--heart-color': instituteStyle.likeColor }"
    title="Like"
    @click.stop="toggleLike($event, offer)"
  >
    <input
      type="checkbox"
      class="checkbox"
      :id="'like-checkbox-' + offer.id"
      :checked="checkIfLiked(offer)"
      @change.stop
    />
    <div class="svg-container" :class="{ animate: offer.isAnimating }">
      <svg
        width="30"
        height="30"
        viewBox="0 0 24 24"
        class="svg-outline"
        xmlns="http://www.w3.org/2000/svg"
        v-show="!checkIfLiked(offer)"
      >
        <path
          d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
          :stroke="instituteStyle.likeColor"
        />
      </svg>
      <svg
        width="30"
        height="30"
        viewBox="0 0 24 24"
        class="svg-filled"
        xmlns="http://www.w3.org/2000/svg"
        v-show="checkIfLiked(offer)"
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
  <p class="text-gray-600 text-sm mb-4 line-clamp-5">
    {{ offer.description || "Нет дополнительной информации" }}
  </p>

  

  <div class="mt-auto space-y-2">
    <button
      @click="openOffer(offer)"
      class="w-full rounded-md px-4 py-2 transition text-always-white"
      :style="{ backgroundColor: currentBgColor }"
      @mouseover="currentBgColor = instituteStyle.buttonOnColor"
      @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
    >
      Подробнее
    </button>
  </div>
</div>
        </div>
      </div>
    </div>

    <OfferModal v-if="isModalOpen" @close="closeModal" @submit="addNewoffer" />
  </div>
</template>

<script>
import OfferModal from "@/components/university/offerModal.vue";
import Header from "@/components/header.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";
import UserService from "@/composables/storage.js";
import api from "@/composables/auth";
import { toggleOfferLike } from "@/services/projects.js";
import Cookies from "js-cookie";

export default {
  inject: ["globalState"],
  components: { OfferModal, Header },
  data() {
    return {
        searchQuery: '',
      statusStyleMap: {
  draft: { label: "Черновик", bg: "#f3f4f6" },             // серый
  review: { label: "На проверке", bg: "#fff3cd" },          // жёлтый
  open: { label: "Опубликовано", bg: "#d4edda" },      // зелёный
  rejected: { label: "Отклонено", bg: "#e2e3e5" },          // серый светлый
},
      userRole: null,
      currentBgColor: "",
      offers: [],
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
    this.fetchCustomeroffers();
  },
  computed: {
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
    filteredoffers() {
  if (!this.searchQuery) return this.offers;
  const query = this.searchQuery.toLowerCase();

  return this.offers.filter(offer =>
    offer &&
    (
      (typeof offer.title === 'string' && offer.title.toLowerCase().includes(query)) ||
      (typeof offer.description === 'string' && offer.description.toLowerCase().includes(query))
    )
  );
},
  },
  methods: {
    async fetchCustomeroffers() {
      try {
        const response = await api.get("/offers/?status=review");
        this.offers = response.data.map((offer) => ({
          ...offer,
          isLiked: this.checkIfLiked(offer),
          isAnimating: false,
        }));
      } catch (error) {
        console.error("Ошибка при загрузке идей:", error);
      }
    },

    checkIfLiked(offer) {
      const userData = JSON.parse(Cookies.get("userData") || "{}");
      return offer.likes?.includes(userData.id) || false;
    },

    async toggleLike(event, offer) {
  try {
    const userData = JSON.parse(Cookies.get("userData") || "{}");

    await toggleOfferLike(
      offer,
      event,
      this.checkIfLiked(offer),
      (value) => (offer.isAnimating = value),
      () => userData.id
    );

    offer.isLiked = !offer.isLiked;

  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);
  }
},

    openOffer(offer) {
      this.$router.push({
        name: "OfferDetail",
        params: {
          institute: this.selectedInstitute,
          id: offer.id,
        },
      });
    },

    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    addNewoffer(newoffer) {
      console.log("Новая идея:", newoffer);
      this.isModalOpen = false;
    },
    onInstituteChanged(newInstitute) {
      this.globalState.institute = newInstitute;
    },
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
    selectedInstitute(newValue) {
      console.log("Глобальное состояние института обновлено:", newValue);
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
  transition: all 0.3s ease;
}

.front {
  transform: rotateY(0deg);
}

.back {
  transform: rotateY(180deg);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.truncate-text {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
}

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

.hover\:bg-opacity-80:hover {
  opacity: 0.8;
}
</style>
