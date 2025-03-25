<template>
  <div>
    <header
      class="flex items-center justify-between px-8 py-4 border border-border"
    >
      <!-- Логотип слева -->
      <div class="flex items-center">
        <h1 class="font-display text-fiolText text-3xl">ВШЦТ</h1>
      </div>
      <!-- Навигация -->
      <nav class="flex items-center gap-10">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.link"
          class="relative text-lg font-medium transition-colors duration-300 group text-white hover:text-fiolText"
          :class="{ 'text-fiolText': $route.path === item.link }"
        >
          {{ item.name }}
          <span
            class="absolute left-1/2 bottom-[-5px] h-[3px] bg-fiolText rounded-full transition-all duration-300 w-0 group-hover:w-full group-hover:left-0"
            :class="{ 'w-2/3 left-1/6': $route.path === item.link }"
          ></span>
        </router-link>

        <!-- Улучшенная кнопка уведомлений -->
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
          <div
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-72 bg-gray-800 rounded-md shadow-lg py-1 z-50 border border-gray-700 max-h-96 overflow-y-auto"
            v-click-outside="closeNotifications"
          >
            <div
              class="px-4 py-2 border-b border-gray-700 flex justify-between items-center"
            >
              <h3 class="font-medium text-white">Уведомления</h3>
              <button
                @click="markAllAsRead"
                class="text-xs text-purple-400 hover:text-purple-300"
                :disabled="unreadNotificationsCount === 0"
              >
                Прочитать все
              </button>
            </div>
            <div v-if="notifications.length > 0">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="px-4 py-3 hover:bg-gray-700 cursor-pointer border-b border-gray-700 last:border-b-0"
                :class="{ 'bg-gray-700/50': !notification.read }"
                @click="handleNotificationClick(notification)"
              >
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-3">
                    <div
                      class="h-8 w-8 rounded-full bg-purple-500 flex items-center justify-center text-white"
                    >
                      {{ getNotificationIcon(notification.type) }}
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-white truncate">
                      {{ notification.title }}
                    </p>
                    <p class="text-xs text-gray-400 mt-1">
                      {{ notification.message }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ formatTime(notification.time) }}
                    </p>
                  </div>
                  <div v-if="!notification.read" class="ml-2">
                    <span
                      class="h-2 w-2 rounded-full bg-purple-500 block"
                    ></span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="px-4 py-6 text-center">
              <p class="text-gray-400 text-sm">Нет новых уведомлений</p>
            </div>
          </div>
        </div>

        <!-- Аватарка с заглушкой -->
        <div class="relative w-12 h-12">
          <div
            @click="goToProfile"
            class="w-full h-full rounded-full border-2 border-zinc-700 hover:border-purple-400 transition-all duration-300 cursor-pointer flex items-center justify-center"
            :style="avatarStyle"
          >
            <span class="text-white font-semibold text-xl">{{
              userInitials
            }}</span>
          </div>
        </div>
      </nav>
    </header>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      menuItems: [
        { name: "Биржа", link: "/rialto" },
        { name: "Команды", link: "/teams" },
        { name: "Идеи", link: "/ideas" },
      ],
      showNotifications: false,
      userName: "Иван Иванов",
      notifications: [
        {
          id: 1,
          type: "message",
          title: "Новое сообщение",
          message: "У вас новое сообщение от команды Ты - ЕБЛАН?",
          time: new Date(Date.now() - 1000 * 60 * 5),
          read: false,
          link: "/messages/1",
        },
        {
          id: 2,
          type: "system",
          title: "Обновление системы",
          message: "Запланировано обновление на 15:00",
          time: new Date(Date.now() - 1000 * 60 * 60 * 2),
          read: true,
          link: "/updates",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
        {
          id: 3,
          type: "event",
          title: "Новое событие",
          message: "Завтра в 18:00 собрание команды",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
          read: false,
          link: "/events/3",
        },
      ],
      colors: ["#FF6B6B", "#48BB78", "#4299E1", "#9F7AEA", "#ED8936"],
    };
  },
  computed: {
    userInitials() {
      return this.userName
        .split(" ")
        .map((name) => name[0])
        .join("")
        .toUpperCase();
    },
    unreadNotificationsCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
    avatarStyle() {
      const colorIndex = this.userName.length % this.colors.length;
      return {
        backgroundColor: this.colors[colorIndex],
      };
    },
  },
  methods: {
    goToProfile() {
      this.$router.push("/profile");
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
    },
    closeNotifications() {
      this.showNotifications = false;
    },
    markAllAsRead() {
      this.notifications = this.notifications.map((n) => ({
        ...n,
        read: true,
      }));
    },
    handleNotificationClick(notification) {
      if (!notification.read) {
        notification.read = true;
      }
      this.$router.push(notification.link);
      this.showNotifications = false;
    },
    getNotificationIcon(type) {
      const icons = {
        message: "✉️",
        system: "⚙️",
        event: "📅",
        warning: "⚠️",
        success: "✅",
      };
      return icons[type] || "🔔";
    },
    formatTime(date) {
      const now = new Date();
      const diffInSeconds = Math.floor((now - date) / 1000);

      if (diffInSeconds < 60) return "только что";

      const diffInMinutes = Math.floor(diffInSeconds / 60);
      if (diffInMinutes < 60) return `${diffInMinutes} мин. назад`;

      const diffInHours = Math.floor(diffInMinutes / 60);
      if (diffInHours < 24) return `${diffInHours} ч. назад`;

      const diffInDays = Math.floor(diffInHours / 24);
      if (diffInDays === 1) return "вчера";

      return date.toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "short",
      });
    },
  },
  directives: {
    "click-outside": {
      bind(el, binding, vnode) {
        el.clickOutsideEvent = function (event) {
          if (!(el === event.target || el.contains(event.target))) {
            vnode.context[binding.expression](event);
          }
        };
        document.body.addEventListener("click", el.clickOutsideEvent);
      },
      unbind(el) {
        document.body.removeEventListener("click", el.clickOutsideEvent);
      },
    },
  },
};
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: #2d3748;
}
::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #718096;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
