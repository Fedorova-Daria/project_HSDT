<template>
  <div>
    <header class="flex items-center justify-between px-8 py-4 border border-border">
      <!-- Логотип слева -->
      <div class="flex items-center">
  <h1 :style="{ color: instituteStyle?.textColor }" class="font-display text-3xl">
    <select @change="changeInstitute" v-model="selectedInstitute">
      <option v-for="inst in institutes" :key="inst" :value="inst">
        {{ inst }}
      </option>
    </select>
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
console.log("Selected Institute from localStorage:", localStorage.getItem("institute"));
export default {
  components: { Notifications },
  name: "Header",
  data() {
    return {
      selectedInstitute: localStorage.getItem("institute") || "TYIU",
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
  const latinInstitute = this.instituteMap[this.selectedInstitute] || this.selectedInstitute; 
  if (!latinInstitute) {
    console.error(`Ошибка: Латинское название для "${this.selectedInstitute}" не найдено.`);
    return [];
  }

  if (latinInstitute === "TYIU") {
    return [
      { name: "О нас", link: "/about" },
      { name: "Идеи", link: "/ideas" },
    ];
  } else {
    return [
      { name: "Биржа", link: "/rialto" },
      { name: "Команды", link: "/teams" },
      { name: "Идеи", link: "/ideas" },
    ];
  }
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
    instituteStyle() {
    // Переводим русское название в латинское, если нужно
    const latinInstitute = this.instituteMap[this.selectedInstitute] || this.selectedInstitute; 
    console.log("Selected Institute:", latinInstitute); // Логируем латинскую версию
    const style = instituteStyles[latinInstitute]; // Получаем стиль для латинского названия
    console.log("Selected Institute Style:", style); // Логируем стиль
    return style || instituteStyles["TYIU"]; // Если стиль не найден, возвращаем дефолтный для TYIU
  },
  },
  methods: {
    checkInstitute() {
  const userData = JSON.parse(localStorage.getItem("userData")) || {};
  const institute = userData.institute || "TYIU"; // Получаем институт, если он указан, иначе используем TYIU

  if (institute === "TYIU") {
    this.$router.push("/TYIU/about"); // Перенаправление на страницу TYIU/about
  }
},
changeInstitute(event) {
  const newInstituteRus = event.target.value; // Получаем русское название
  const newInstituteLat = this.instituteMap[newInstituteRus]; // Преобразуем в латинское название

  if (!newInstituteLat) {
    console.error("Ошибка: Латинское название института не найдено.");
    return; // Останавливаем выполнение, если институт не найден
  }

  let userData = JSON.parse(localStorage.getItem("userData")) || {};
  userData.institute = newInstituteLat; // Обновляем институт в данных пользователя
  localStorage.setItem("userData", JSON.stringify(userData)); // Сохраняем обновлённые данные

  this.selectedInstitute = newInstituteLat; // Устанавливаем выбранный институт

  // Перенаправляем пользователя в зависимости от выбранного института
  if (newInstituteLat === "TYIU") {
    this.$router.push("/TYIU/about");
  } else {
    this.$router.push(`/${newInstituteLat}/rialto`);
  }
},
updateInstituteFromRoute() {
  const institute = this.reverseInstituteMap[this.$route.params.institute];
  if (institute) {
    this.selectedInstitute = institute;
  } else {
    this.selectedInstitute = "ТИУ"; // Дефолтный логотип
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
  const userData = JSON.parse(localStorage.getItem("userData")) || {};
  const institute = userData.institute || "TYIU";

  this.selectedInstitute = this.reverseInstituteMap[institute] || institute;
  this.updateInstituteFromRoute(); // Синхронизация с маршрутом
},
};
</script>

<style scoped>
  .group:hover {
    color: var(--hover-color);
  }
</style>