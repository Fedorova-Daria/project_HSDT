<template>
  <div>
    <div
      v-if="showNotifications"
      @click.stop
      ref="notificationsDropdown"
      class="absolute right-0 mt-2 w-72 bg-input rounded-md shadow-lg py-1 border border-gray-700 max-h-96 overflow-y-auto" style="z-index: 99999;"
    >
      <div class="px-4 py-2 flex justify-between items-center">
        <h3 class="font-medium">Уведомления</h3>
        <button
          @click="markAllAsRead"
          class="btn-read-all text-xs"
          :disabled="loading"
        >
          {{ loading ? 'Обработка...' : 'Прочитать все' }}
        </button>
      </div>

      <div v-if="notifications.length > 0">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="px-4 py-3 cursor-pointer bg-card border-b last:border-b-0"
          :class="{ read: !notification.is_read }"
          @click="openModal(notification)"
        >
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-3">
              <div class="h-8 w-8 rounded-full bg-zinc-500 flex items-center justify-center text-white">
                {{ getNotificationIcon(notification.type) }}
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium truncate">
                {{ notification.title }}
              </p>
              <p class="text-xs mt-1">
                {{ notification.message }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{ formatTime(new Date(notification.created_at)) }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="px-4 py-6 text-center">
        <p class="text-gray-400 text-sm">Нет новых уведомлений</p>
      </div>
    </div>

    <!-- Модальное окно -->
    <NotificationModal
      v-if="isModalOpen && selectedNotification"
      :show="isModalOpen"
      :notification="selectedNotification"
      @close="closeModal"
    />
  </div>
</template>

<script>
import api from "@/composables/auth";
import { notificationService } from "@/services/notificationService";
import NotificationModal from "@/components/NotificationModal.vue";
import { instituteStyles } from "@/assets/instituteStyles.js";

export default {
  inject: ["globalState"], 
  components: {NotificationModal},
  props: {
    showNotifications: Boolean,
    notificationButton: {
      type: Object,
      default: null
    }
  },
  emits: ['close'], // ✅ Добавляем эмит для закрытия
  data() {
    return {
      loading: false,
      currentBgColor: "",
      notifications: [],
      pollingInterval: null,
      isModalOpen: false,
      selectedNotification: null,
    };
  },
  computed: {
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
    unreadNotificationsCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
  },
  mounted() {

    this.loadNotifications();
    this.pollingInterval = setInterval(this.loadNotifications, 300000);
    
    // ✅ Добавляем обработчик клика при монтировании
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    clearInterval(this.pollingInterval);
    
    // ✅ Удаляем обработчик при размонтировании
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    // ✅ Новый метод для обработки кликов вне области
    handleClickOutside(event) {
      if (!this.showNotifications) return;
      
      const dropdown = this.$refs.notificationsDropdown;
      const button = this.notificationButton;
      
      // Проверяем, что клик не по dropdown и не по кнопке уведомлений
      if (dropdown && !dropdown.contains(event.target) && 
          (!button || !button.contains(event.target))) {
        this.closeNotifications();
      }
    },
    
    // ✅ Метод для закрытия уведомлений
    closeNotifications() {
      this.$emit('close');
    },

    async markAllAsRead() {
      try {
        await api.post('/notifications/mark_all_as_read/', {
          notification_type: "",
          message: "",
          is_read: true,
          related_team: null,
          related_project: null,
          related_team_join_request: null,
          related_project_application: null,
        });
        this.notifications.forEach(n => n.is_read = true);
      } catch (error) {
        console.error('Ошибка отметки всех уведомлений прочитанными', error);
      }
    },

    async loadNotifications() {
      try {
        const data = await notificationService.getNotifications();
        if (Array.isArray(data)) {
          this.notifications = data;
        } else if (data && Array.isArray(data.notifications)) {
          this.notifications = data.notifications;
        } else {
          this.notifications = [];
        }
      } catch (error) {
        console.error("Не удалось загрузить уведомления:", error);
        this.notifications = [];
      }
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

    openModal(notification) {
      console.log('Открываем модалку с уведомлением:', notification);
      this.selectedNotification = notification;
      this.isModalOpen = true;
    },

    closeModal() {
      this.isModalOpen = false;
      this.selectedNotification = null;
    },
  },
  watch: {
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
    showNotifications(newVal) {
      if (newVal) {
        this.loadNotifications();
      }
    }
  },
};
</script>


<style scoped>
.z-70 {
  z-index: 80; /* Обеспечим, чтобы модалки были выше колонок */
}
.read {
  opacity: 0.6;
}
.btn-read-all {
  margin-top: 10px;
  /* стили для кнопки */
}
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
