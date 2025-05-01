// notificationService.js
import api from "@/composables/auth";

export const notificationService = {
  getNotifications: async () => {
    try {
      const response = await api.get('/notifications/'); // Запрос на получение уведомлений
      return response.data; // Возвращаем уведомления
    } catch (error) {
      console.error('Ошибка при получении уведомлений:', error);
      throw error;
    }
  },
  
  markAsRead: async (notificationId) => {
    try {
      const response = await api.patch(`/notifications/`, { read: true });
      return response.data;
    } catch (error) {
      console.error('Ошибка при пометке уведомления как прочитанное:', error);
      throw error;
    }
  }
};