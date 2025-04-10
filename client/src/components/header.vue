<template>
  <div>
    <header class="flex items-center justify-between px-8 py-4 border border-border">
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1 :style="{ color: instituteStyle?.textColor }" class="font-display text-3xl">
          <div class="relative">
            <button @click="toggleDropdown" class="flex items-center px-4 py-2 rounded-lg">
              {{ selectedInstitute }}
              <svg xmlns="http://www.w3.org/2000/svg" class="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <ul v-if="isDropdownOpen" class="absolute left-0 w-50 mt-2 bg-card text-white rounded-lg shadow-lg z-10">
              <li v-for="inst in institutes" :key="inst" @click="changeInstitute(inst)" class="py-2 px-4 cursor-pointer hover:bg-zinc-600 rounded-lg">
                {{ inst }}
              </li>
            </ul>
          </div>
        </h1>
      </div>


      <!-- Навигация -->
      <nav class="flex items-center gap-10">
        
        <router-link
  v-for="item in menuItems"
  :key="item.name"
  :to="`/${instituteMap[selectedInstitute] || selectedInstitute}${item.link}`"
  class="relative text-lg font-medium transition-colors duration-300 group text-white"
  :style="{ '--hover-color': instituteStyle?.textColor }"
>
  {{ item.name }}
  <span
    class="absolute left-1/2 bottom-[-5px] h-[3px] rounded-full transition-all duration-300 w-0 group-hover:w-full group-hover:left-0"
    :style="{ backgroundColor: instituteStyle?.textColor }"
    :class="{ 'w-2/3 left-1/6': $route.path === `/${instituteMap[selectedInstitute] || selectedInstitute}${item.link}` }"
  ></span>
</router-link>


        <!-- Кнопка уведомлений -->
        <div class="relative">
          <button class="relative p-1" @click="toggleNotifications">
            <img src="/notificate.svg" alt="notification" class="w-6" />
            <span
              v-if="unreadNotificationsCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center"
            >
              {{
                unreadNotificationsCount > 9 ? "9+" : unreadNotificationsCount
              }}
            </span>
          </button>

          <!-- Выпадающее меню уведомлений -->
          <Notifications
            v-if="showNotifications"
            :showNotifications="showNotifications"
            :notifications="notifications"
            @close="showNotifications = false"
            @markAllRead="markAllAsRead"
            @notificationClick="handleNotificationClick"
          />
        </div>

        <!-- Аватарка -->
        <div class="relative w-12 h-12">
  <div
    @click="goToProfile"
    class="w-full h-full rounded-full border-2 border-zinc-700 transition-all duration-300 cursor-pointer flex items-center justify-center hover:border-[var(--hover-color)]"
    :style="{ ...avatarStyle, '--hover-color': instituteStyle?.textColor }"
  >
    <span class="text-white font-semibold text-xl">{{ userInitials }}</span>
  </div>
</div>
      </nav>
    </header>
  </div>
</template>

<script>
import { instituteStyles } from '@/assets/instituteStyles.js'; // Импортируем карту стилей
import Notifications from "@/components/notific.vue";
import Cookies from "js-cookie";

export default {
  name: "Header",
  inject: ["globalState"], 
  components: { Notifications },
  data() {
    return {
      isDropdownOpen: false,
      localSelectedInstitute: Cookies.get("institute") || "TYIU",
      showNotifications: false,
      notifications: [],
      userName: "Иван Иванов",
      institutes: ["ВШЦТ", "АРХИД", "ИПТИ", "СТРОИН", "ТИУ"],
      instituteMap: { 
        "ВШЦТ": "HSDT",
        "АРХИД": "ARCHID",
        "ИПТИ": "IPTI",
        "СТРОИН": "STROIN",
        "ТИУ": "TYIU",
      },
      reverseInstituteMap: {
        "HSDT": "ВШЦТ",
        "ARCHID": "АРХИД",
        "IPTI": "ИПТИ",
        "STROIN": "СТРОИН",
        "TYIU": "ТИУ",
      },
      
    };
  },
  computed: {
    menuItems() {
    const latinInstitute = this.instituteMap[this.localSelectedInstitute] || this.localSelectedInstitute;
    if (!latinInstitute) {
      console.error(`Ошибка: Латинское название для "${this.localSelectedInstitute}" не найдено.`);
      return [];
    }
    return latinInstitute === "TYIU"
      ? [{ name: "О нас", link: "/about" }, { name: "Идеи", link: "/ideas" }]
      : [{ name: "Биржа", link: "/rialto" }, { name: "Команды", link: "/teams" }, { name: "Идеи", link: "/ideas" }];
  },
  instituteStyle() {
    const latinInstitute = this.instituteMap[this.localSelectedInstitute] || this.localSelectedInstitute;
    return instituteStyles[latinInstitute] || instituteStyles["TYIU"];
  },
    unreadNotificationsCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
    userInitials() {
      return this.userName
        .split(" ")
        .map((name) => name[0])
        .join("")
        .toUpperCase();
    },
    avatarStyle() {
  const colors = this.instituteStyle?.avatarColors || ["#ccc"]; // Дефолтный цвет
  const colorIndex = this.userName.length % colors.length;
  return { backgroundColor: colors[colorIndex] };
},
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    checkInstitute() {
      const userData = JSON.parse(Cookies.get("userData") || "{}");
  const institute = userData.institute || "TYIU"; // Получаем институт, если он указан, иначе используем TYIU

  if (institute === "TYIU") {
    this.$router.push("/TYIU/about"); // Перенаправление на страницу TYIU/about
  }
},
changeInstitute(inst) {
      const newInstituteLat = this.instituteMap[inst] || inst;
      if (!newInstituteLat) {
        console.error(`Ошибка: Латинское название для "${inst}" не найдено.`);
        return;
      }
      this.localSelectedInstitute = newInstituteLat;
      this.globalState.institute = newInstituteLat;
      let userData = JSON.parse(Cookies.get("userData") || "{}");
      userData.institute = newInstituteLat;
      Cookies.set("userData", JSON.stringify(userData));
      const routePath = newInstituteLat === "TYIU" ? "/TYIU/about" : `/${newInstituteLat}/rialto`;
      this.$router.push(routePath);
      this.isDropdownOpen = false;
    },
updateInstituteFromRoute() {
  const instituteFromRoute = this.$route.params.institute;
  const institute = this.reverseInstituteMap[instituteFromRoute] || instituteFromRoute;

  if (institute) {
    console.log("Обновление из маршрута:", institute);
    this.localSelectedInstitute = this.instituteMap[institute] || institute; // Локальное состояние
    this.globalState.institute = this.instituteMap[institute] || institute; // Глобальное состояние
  } else {
    console.error("Не удалось определить институт из маршрута.");
  }
},
  goToProfile() {
    const latinInstitute = this.instituteMap[this.selectedInstitute] || this.selectedInstitute;
    this.$router.push(`/${latinInstitute}/profile`);
  }
  },
  watch: {
  "$route.fullPath": "updateInstituteFromRoute", // Теперь следим за полным путём
},
created() {
  const userData = JSON.parse(Cookies.get("userData") || "{}");
  const institute = userData.institute || "TYIU";

  console.log("Институт из Cookies:", institute);

  // Синхронизируем глобальное состояние
  this.globalState.institute = institute;

  // Устанавливаем `selectedInstitute` для локального отображения
  this.selectedInstitute = this.reverseInstituteMap[institute] || institute;
  this.updateInstituteFromRoute();
},
};
</script>

<style scoped>
  .group:hover {
    color: var(--hover-color);
  }
</style>