<template>
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
</template>

<script>
export default {
  props: {
    notifications: Array,
    showNotifications: Boolean,
  },
  computed: {
    unreadNotificationsCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
  },
  methods: {
    closeNotifications() {
      this.$emit("close");
    },
    markAllAsRead() {
      this.$emit("markAllRead");
    },
    handleNotificationClick(notification) {
      if (!notification.read) {
        notification.read = true;
      }
      this.$router.push(notification.link);
      this.closeNotifications();
      this.$emit("notificationClick", notification);
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
      beforeMount(el, binding) {
        el.clickOutsideEvent = function (event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event);
          }
        };
        document.body.addEventListener("click", el.clickOutsideEvent);
      },
      unmounted(el) {
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