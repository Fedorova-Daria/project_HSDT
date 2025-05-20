<template>
  <div class="bg-lightBackground dark:bg-darkBackground">
    <header
      class="flex items-center justify-between px-8 py-4 border-b border-dynamic"
    >
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1
          :style="{ color: instituteStyle?.textColor }"
          class="font-display text-3xl"
        >
          <div class="relative">
            <button
              @click="toggleDropdown"
              class="flex items-center px-4 py-2 rounded-lg transition hover:shadow-lg"
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
              class="absolute left-0 w-50 mt-2 bg-card text-dynamic rounded-lg shadow-lg z-10"
            >
              <li
                v-for="inst in institutes"
                :key="inst"
                @click="changeInstitute(inst)"
                class="py-2 px-4 cursor-pointer hover:bg-zinc-600 rounded-lg"
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
            :checked="isDarkTheme"
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
            :src="userAvatar"
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
import { instituteStyles } from "@/assets/instituteStyles.js";
import Notifications from "@/components/notific.vue";
import Cookies from "js-cookie";

/** @typedef {'ВШЦТ'|'АРХИД'|'ИПТИ'|'СТРОИН'|'ТИУ'} Institute */

export default {
  name: "Header",
  inject: ["globalState"],
  components: { Notifications },
  data() {
    return {
      isDarkTheme: false,
      isDropdownOpen: false,
      selectedInstitute: Cookies.get("institute") || "TYIU",
      showNotifications: false,
      notifications: [],
      user: {},
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
  computed: {
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
      return (
        instituteStyles[this.instituteMap[this.selectedInstitute]] ||
        instituteStyles["TYIU"]
      );
    },
    unreadNotificationsCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
    userName() {
      try {
        const storedUser = localStorage.getItem("userData") || "{}";
        const user = JSON.parse(storedUser);
        return (
          user?.name ||
          `${user?.first_name || ""} ${user?.last_name || ""}`.trim() ||
          "Гость"
        );
      } catch (e) {
        console.error("Ошибка чтения userData:", e);
        return "Гость";
      }
    },
    userAvatar() {
      try {
        const storedUser = localStorage.getItem("userData") || "{}";
        const user = JSON.parse(storedUser);
        return user?.avatar || "";
      } catch (e) {
        return "";
      }
    },
    userInitials() {
      if (!this.userName) return "";
      const splitName = this.userName.split(" ");
      return splitName.length > 1
        ? `${splitName[0][0]}${
            splitName[splitName.length - 1][0]
          }`.toUpperCase()
        : this.userName.substring(0, 2).toUpperCase();
    },
    avatarStyle() {
      const colors = this.instituteStyle?.avatarColors || ["#ccc"];
      const colorIndex = this.userName.length % colors.length;

      if (this.userAvatar) {
        return {
          backgroundImage: `url(${this.userAvatar})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        };
      }

      return {
        backgroundColor: colors[colorIndex],
        background: "linear-gradient(45deg, #ff9a9e, #fad0c4)",
      };
    },
  },
  methods: {
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
      if (this.showNotifications && this.notifications.length === 0) {
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
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      localStorage.setItem("theme", this.isDarkTheme ? "dark" : "light");
      document.documentElement.classList.toggle("dark-theme", this.isDarkTheme);
      document.documentElement.classList.toggle(
        "light-theme",
        !this.isDarkTheme
      );
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    /** @param {Institute} inst */
    changeInstitute(inst) {
      const routeMap = {
        TYIU: "/about",
        HSDT: "/rialto",
        ARCHID: "/rialto",
        IPTI: "/rialto",
        STROIN: "/rialto",
      };

      const newInstitute = this.instituteMap[inst] || inst;
      this.selectedInstitute = newInstitute;
      this.globalState.institute = newInstitute;

      const userData = JSON.parse(Cookies.get("userData") || "{}");
      userData.institute = newInstitute;
      Cookies.set("userData", JSON.stringify(userData));

      this.$router.push(`/${newInstitute}${routeMap[newInstitute]}`);
      this.isDropdownOpen = false;
    },
    updateInstituteFromRoute() {
      const routeInstitute = this.$route.params.institute;
      this.selectedInstitute =
        this.reverseInstituteMap[routeInstitute] || routeInstitute;
      this.globalState.institute =
        this.instituteMap[this.selectedInstitute] || this.selectedInstitute;
    },
    goToProfile() {
      this.$router.push(
        `/${this.instituteMap[this.selectedInstitute]}/profile`
      );
    },
  },
  watch: {
    "$route.fullPath": "updateInstituteFromRoute",
  },
  created() {
    const savedTheme = localStorage.getItem("theme") || "light";
    this.isDarkTheme = savedTheme === "dark";
    document.documentElement.classList.add(`${savedTheme}-theme`);

    const userData = JSON.parse(Cookies.get("userData") || "{}");
    this.globalState.institute = userData.institute || "TYIU";
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

.switch input:checked + .slider {
  background-color: var(--switch-checked-bg, #00a6ff);
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
  box-shadow: inset 8px -4px 0px 0px #fff;
}

.switch input:checked + .slider:before {
  transform: translateX(1.8em);
  box-shadow: inset 15px -4px 0px 15px #ffcf48;
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

.switch input:checked ~ .slider .star {
  opacity: 0;
}

.cloud {
  width: 3.5em;
  position: absolute;
  bottom: -1.4em;
  left: -1.1em;
  opacity: 0;
  transition: all 0.4s;
}

.switch input:checked ~ .slider .cloud {
  opacity: 1;
}

.group:hover {
  color: var(--hover-color);
}
</style>
