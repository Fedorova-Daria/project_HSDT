<template>
  <div class="bg-lightBackground dark:bg-darkBackground">
    <header
      class="flex items-center justify-between px-8 py-4 shadow-md rounded-4xl relative z-10"
    >
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1
          :style="{ color: instituteStyle?.textColor }"
          class="font-display text-3xl"
        >
          <div class="relative z-50">
            <button
              @click="toggleDropdown"
              class="flex items-center institute-text px-4 py-2 rounded-lg transition hover:shadow-lg duration-300"
            >
              {{ selectedInstitute }}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="ml-2 w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            <ul
              v-if="isDropdownOpen"
              class="absolute left-0 w-50 mt-2 bg-card text-dynamic rounded-lg shadow-lg z-50"
            >
              <li
                v-for="inst in institutes"
                :key="inst"
                @click="changeInstitute(inst)"
                class="py-2 px-4 cursor-pointer dropDown rounded-lg z-10"
              >
                {{ inst }}
              </li>
            </ul>
          </div>
        </h1>
      </div>

      <!-- Навигация -->
      <nav class="flex items-center gap-10">
        <label class="switch">
          <input
            id="checkbox"
            type="checkbox"
            :checked="isDark"
            @change="toggleTheme"
          />
          <span class="slider">
            <div class="star star_1"></div>
            <div class="star star_2"></div>
            <div class="star star_3"></div>
            <svg viewBox="0 0 16 16" class="cloud_1 cloud">
              <path
                transform="matrix(.77976 0 0 .78395-299.99-418.63)"
                fill="#fff"
                d="m391.84 540.91c-.421-.329-.949-.524-1.523-.524-1.351 0-2.451 1.084-2.485 2.435-1.395.526-2.388 1.88-2.388 3.466 0 1.874 1.385 3.423 3.182 3.667v.034h12.73v-.006c1.775-.104 3.182-1.584 3.182-3.395 0-1.747-1.309-3.186-2.994-3.379.007-.106.011-.214.011-.322 0-2.707-2.271-4.901-5.072-4.901-2.073 0-3.856 1.202-4.643 2.925"
              ></path>
            </svg>
          </span>
        </label>

        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="`/${instituteMap[selectedInstitute] || selectedInstitute}${
            item.link
          }`"
          class="relative text-lg font-medium transition-colors duration-300 group text-dynamic"
          :style="{ '--hover-color': instituteStyle?.textColor }"
        >
          {{ item.name }}
          <span
            class="absolute left-1/2 bottom-[-5px] h-[3px] rounded-full transition-all duration-300 w-0 group-hover:w-full group-hover:left-0"
            :style="{ backgroundColor: instituteStyle?.textColor }"
            :class="{
              'w-2/3 left-1/6':
                $route.path ===
                `/${instituteMap[selectedInstitute] || selectedInstitute}${
                  item.link
                }`,
            }"
          ></span>
        </router-link>

        <!-- Кнопка уведомлений -->
        <div class="relative">
          <button class="relative p-1" @click="toggleNotifications">
            <img 
            :src="isDarkTheme ? '/notificate.svg' :'/notificate_dark.svg' "
            alt="notification" 
            class="w-6" />
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
            @close="showNotifications = false"
          />
        </div>

        <!-- Аватарка -->
        <div
          class="relative w-12 h-12 rounded-full overflow-hidden cursor-pointer"
          @click="goToProfile"
          :style="avatarStyle"
        >
          <img
            v-if="userAvatar"
            :src="userAvatar ? `http://127.0.0.1:8000/${userAvatar}` : null"
            alt="User Avatar"
            class="object-cover w-full h-full rounded-full border-2 border-zinc-400"
          />
          <span
            v-else
            class="flex items-center justify-center w-full h-full text-dynamic font-semibold text-xl rounded-full border-2 border-zinc-400"
          >
            {{ userInitials }}
          </span>
        </div>
      </nav>
    </header>
  </div>
</template>

<script>
import { instituteStyles } from "@/assets/instituteStyles.js"; // Импортируем карту стилей
import Notifications from "@/components/notific.vue";
import Cookies from "js-cookie";
import api from "@/composables/auth"; // Предварительно настроенный экземпляр axios
import { useTheme } from "@/composables/useTheme";

export default {
  name: "Header",
  inject: ["globalState"],
  components: { Notifications },
  data() {
    return {
      unreadNotificationsCount: 0,
      isDark: false,
      userData:null,
      isDropdownOpen: false,
      localSelectedInstitute: Cookies.get("institute") || "TYIU",
      showNotifications: false, // Управляет видимостью меню уведомлений
      notifications: [], // Хранение списка уведомлений
      user: {}, // Здесь будем хранить данные пользователя
      institutes: ["ВШЦТ", "АРХИД", "ИПТИ", "СТРОИН", "ТИУ"],
      instituteMap: {
        ВШЦТ: "HSDT",
        АРХИД: "ARCHID",
        ИПТИ: "IPTI",
        СТРОИН: "STROIN",
        ТИУ: "TYIU",
      },
      reverseInstituteMap: {
        HSDT: "ВШЦТ",
        ARCHID: "АРХИД",
        IPTI: "ИПТИ",
        STROIN: "СТРОИН",
        TYIU: "ТИУ",
      },
    };
  },
  mounted() {
    this.initTheme();
    this.fetchUserData();
    this.fetchUnreadNotificationsCount();
  },
  computed: {
    isDarkTheme() {
    if (!this.userData) return false;
    return this.userData.mode === 'dark';
  },
  pathFillColor() {
      return this.isDarkTheme ? "white" : "black";
    },
    menuItems() {
      const latinInstitute =
        this.instituteMap[this.localSelectedInstitute] ||
        this.localSelectedInstitute;
      if (!latinInstitute) {
        console.error(
          `Ошибка: Латинское название для "${this.localSelectedInstitute}" не найдено.`
        );
        return [];
      }
      return latinInstitute === "TYIU"
        ? [
            { name: "О нас", link: "/about" },
            { name: "Предложения", link: "/offers" },
          ]
        : [
            { name: "Биржа", link: "/rialto" },
            { name: "Команды", link: "/teams" },
            { name: "Идеи", link: "/ideas" },
          ];
    },
    instituteStyle() {
      const latinInstitute =
        this.instituteMap[this.localSelectedInstitute] ||
        this.localSelectedInstitute;
      return instituteStyles[latinInstitute] || instituteStyles["TYIU"];
    },
    userName() {
      try {
        const storedUser = localStorage.getItem("userData");
        if (storedUser) {
          const user = JSON.parse(storedUser);
          // Если у пользователя есть отдельные поля first_name, last_name,
          // можно объединить их либо взять просто user.name
          return user.first_name && user.last_name
            ? `${user.first_name} ${user.last_name}`
            : user.name || "";
        }
        return "";
      } catch (e) {
        console.error("Ошибка чтения userData:", e);
        return "";
      }
    },
    // Вычисляемое свойство для аватара пользователя
    userAvatar() {
      try {
        const storedUser = localStorage.getItem("userData");
        if (storedUser) {
          const user = JSON.parse(storedUser);
          return user.avatar || "";
        }
        return "";
      } catch (e) {
        return "";
      }
    },
    // Вычисляемое свойство для инициалов пользователя,
    // если аватара нет (используем userName для генерации)
    userInitials() {
      if (!this.userName) return "";
      const splitName = this.userName.split(" ");
      if (splitName.length > 1) {
        // Берём первую букву первого и последнего слова
        return (
          splitName[0].charAt(0) + splitName[splitName.length - 1].charAt(0)
        ).toUpperCase();
      }
      // Если одно слово – первые две буквы
      return this.userName.substring(0, 2).toUpperCase();
    },
    // Вычисляемое свойство для стиля аватарки
    avatarStyle() {
      // Если аватарка задана, можно вернуть стиль с background-image,
      // но если нет, возвращаем, например, цвет фона, зависящий от имени.
      if (this.userAvatar) {
        return {
          backgroundImage: `url(${this.userAvatar})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        };
      }
      // Если аватарки нет, создаём фон (можно сделать градиент, используя длину или хэш имени)
      // Здесь для примера просто задаём фиксированный градиент.
      return {
        background: "linear-gradient(45deg, #ff9a9e, #fad0c4)",
      };
    },
    avatarStyle() {
      const colors = this.instituteStyle?.avatarColors || ["#ccc"]; // Дефолтный цвет
      const colorIndex = this.userName.length % colors.length;
      return { backgroundColor: colors[colorIndex] };
    },
  },
  methods: {
    async fetchUnreadNotificationsCount() {
      const storedUser = localStorage.getItem("userData");
      if (!storedUser) return;

  const user = JSON.parse(storedUser);
    try {
      const response = await api.get(`/notifications/?is_read=false&user=${user.id}`);
      this.unreadNotificationsCount = response.data.length;
    } catch (error) {
      console.error("Ошибка при получении непрочитанных уведомлений:", error);
    }
  },
    async fetchUserData() {
      const response = await api.get('/users/me');
      this.userData = response.data;
      return response.data;
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;

      // Добавляем уведомление при открытии
      if (this.showNotifications) {
        this.notifications.push({
          id: Date.now(),
          title: "Вас пригласили в команду",
          message: 'Вас пригласили в команду "Тест"',
          read: false,
          time: new Date(),
          type: "system",
        });
      }
    },
    handleNotificationClick(notification) {
      console.log("Клик по уведомлению:", notification);
      if (!notification.read) {
        notification.read = true;
      }
      this.$router.push(notification.link);
      this.showNotifications = false; // Закрываем меню после клика
    },
    markAllAsRead() {
      this.notifications.forEach((notification) => {
        notification.read = true;
      });
    },
    initTheme() {
  const { applyTheme } = useTheme();
  const userData = JSON.parse(localStorage.getItem("userData"));
  if (userData && userData.mode) {
    applyTheme(userData.mode);
    this.isDark = userData.mode === "dark"; // 👈 вот это
  }
},

    async toggleTheme() {
  const userData = JSON.parse(localStorage.getItem("userData"));
  if (!userData) return;

  const newMode = userData.mode === "dark" ? "light" : "dark";

  try {
    await api.post("/users/change-theme/", { mode: newMode });
    userData.mode = newMode;
    localStorage.setItem("userData", JSON.stringify(userData));

    const { applyTheme } = useTheme();
    applyTheme(newMode);

    this.isDark = newMode === "dark"; // 👈 вот это
  } catch (error) {
    console.error("Ошибка при смене темы:", error);
  }
},
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
      const routePath =
        newInstituteLat === "TYIU"
          ? "/TYIU/about"
          : `/${newInstituteLat}/rialto`;
      this.$router.push(routePath);
      this.isDropdownOpen = false;
    },
    updateInstituteFromRoute() {
      const instituteFromRoute = this.$route.params.institute;
      const institute =
        this.reverseInstituteMap[instituteFromRoute] || instituteFromRoute;

      if (institute) {
        console.log("Обновление из маршрута:", institute);
        this.localSelectedInstitute = this.instituteMap[institute] || institute; // Локальное состояние
        this.globalState.institute = this.instituteMap[institute] || institute; // Глобальное состояние
      } else {
        console.error("Не удалось определить институт из маршрута.");
      }
    },

    goToProfile() {
      const latinInstitute =
        this.instituteMap[this.selectedInstitute] || this.selectedInstitute;
      this.$router.push(`/${latinInstitute}/profile`);
    },
  },
  watch: {
    "$route.fullPath": "updateInstituteFromRoute", // Теперь следим за полным путём
  },
  created() {
    const userData = JSON.parse(Cookies.get("userData") || "{}");
    const institute = userData.institute || "TYIU";
    // Если данные пользователя (например, имя, фамилия, аватар) сохранены в localStorage,
    // получаем их и преобразуем из JSON.
    const storedUser = localStorage.getItem("userData");
    if (storedUser) {
      this.user = JSON.parse(storedUser);
    } else {
      // В качестве fallback можно получить данные из Cookies или задать пустой объект
      this.user = {};
    }

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
.switch {
  font-size: 10px;
  position: relative;
  display: inline-block;
  width: 4em;
  height: 2.2em;
  border-radius: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--switch-bg, #2a2a2a);
  transition: 0.4s;
  border-radius: 30px;
  overflow: hidden;
}

/* ТЁМНАЯ ТЕМА (input:checked) — луна, звезды */
.switch input:checked + .slider {
  background-color: var(--switch-bg, #2a2a2a); /* тёмный фон */
}
.switch input:checked + .slider:before {
  transform: translateX(1.8em); /* КРУГ вправо */
  box-shadow: inset 8px -4px 0px 0px #fff; /* луна */
}
.switch input:checked ~ .slider .star {
  opacity: 1; /* звезды появляются */
}
.switch input:checked ~ .slider .cloud {
  opacity: 0; /* облака исчезают */
}

/* СВЕТЛАЯ ТЕМА (input НЕ checked) — солнце, облака */
.switch input:not(:checked) + .slider {
  background-color: var(--switch-checked-bg, #00a6ff); /* светлый фон */
}
.switch input:checked + .slider:before {
  transform: translateX(0); /* влево */
  box-shadow: inset 8px -4px 0px 0px #fff; /* луна */
}
.switch input:not(:checked) ~ .slider .star {
  opacity: 0; /* звезды исчезают */
}
.switch input:not(:checked) ~ .slider .cloud {
  opacity: 1; /* облака появляются */
}

.slider:before {
  position: absolute;
  content: "";
  height: 1.2em;
  width: 1.2em;
  border-radius: 20px;
  left: 0.5em;
  bottom: 0.5em;
  transition: 0.4s;
  transition-timing-function: cubic-bezier(0.81, -0.04, 0.38, 1.5);
  transform: translateX(1.8em); /* изначально СПРАВА */
  box-shadow: inset 15px -4px 0px 15px #ffcf48; /* солнце */
}

.star {
  background-color: #fff;
  border-radius: 50%;
  position: absolute;
  width: 5px;
  transition: all 0.4s;
  height: 5px;
}

.star_1 {
  left: 2.5em;
  top: 0.5em;
}
.star_2 {
  left: 2.2em;
  top: 1.2em;
}
.star_3 {
  left: 3em;
  top: 0.9em;
}

.cloud {
  width: 3.5em;
  position: absolute;
  bottom: -1.4em;
  left: -1.1em;
  opacity: 0;
  transition: all 0.4s;
}

.group:hover {
  color: var(--hover-color);
}

.dark-filter {
  filter: invert(1);
}
</style>
