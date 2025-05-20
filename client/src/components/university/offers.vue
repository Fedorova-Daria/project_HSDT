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
        class="rounded-md px-4 py-2 transition ml-5 h-10 text-white"
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
        :style="{ '--border-color': instituteStyle.textColor }"
      >
        <div class="flipper">
          <!-- Лицевая сторона -->
          <div class="front bg-white p-6 rounded-lg shadow-lg">
            <h3 class="text-xl font-semibold mb-2 truncate-text">
              {{ offer.name }}
            </h3>
            <div class="flex items-center mb-4">
              <span class="text-sm text-gray-500">{{
                offer.author || "Автор не указан"
              }}</span>
            </div>
            <p class="text-gray-600 text-sm mb-4 truncate-text">
              {{ offer.description || "Описание отсутствует" }}
            </p>
            <div class="flex items-center justify-between">
              <span class="text-dynamic font-medium">
                {{ offer.likes?.length || 0 }} лайков
              </span>
              <img
                :src="offer.isLiked ? '/liked.svg' : '/like.svg'"
                class="w-6 h-6 cursor-pointer duration-300"
                :class="{ 'animate-like': offer.isAnimating }"
                @click="toggleLike(offer)"
              />
            </div>
          </div>

          <!-- Обратная сторона -->
          <div class="back bg-white p-6 rounded-lg shadow-lg flex flex-col">
            <h3 class="text-xl font-semibold mb-4">Детали предложения</h3>
            <p class="text-gray-600 text-sm mb-4">
              {{ offer.details || "Нет дополнительной информации" }}
            </p>

            <div class="mt-auto space-y-2">
              <div class="flex items-center text-sm">
                <span class="mr-2">📅</span>
                {{ offer.date || "Срок не указан" }}
              </div>
              <button
                @click="openOffer(offer)"
                class="w-full rounded-md px-4 py-2 transition text-white"
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
import { toggleLike } from "@/services/projects.js";
import Cookies from "js-cookie";

export default {
  inject: ["globalState"],
  components: { OfferModal, Header },
  data() {
    return {
      userRole: null,
      currentBgColor: "",
      offers: [],
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
      return this.offers.filter((offer) =>
        offer.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchCustomeroffers() {
      try {
        const response = await api.get("/offers/");
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

    async toggleLike(offer) {
      try {
        const userData = JSON.parse(Cookies.get("userData") || "{}");
        const response = await toggleLike(offer.id, userData.id);

        offer.isAnimating = true;
        offer.likes = response.data.likes;
        offer.isLiked = !offer.isLiked;

        setTimeout(() => {
          offer.isAnimating = false;
        }, 300);
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
}

.back {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
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
