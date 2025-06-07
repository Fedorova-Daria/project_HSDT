// notificationService.js
import api from "@/composables/auth";

export const notificationService = {
  getNotifications: async () => {
    try {
      const response = await api.get('/notifications/?is_read=false'); // Запрос на получение уведомлений
      return response.data; // Возвращаем уведомления
    } catch (error) {
      console.error('Ошибка при получении уведомлений:', error);
      throw error;
    }
  },
  
  markAsReading: async (notificationId) => {
    try {
      const response = await api.patch(`/notifications/${notificationId}/`, { status: 'reading' }); // Изменяем статус на 'reading'
      return response.data;
    } catch (error) {
      console.error('Ошибка при изменении статуса уведомления на "reading":', error);
      throw error;
    }
  },
  getNotificationById: async (notificationId) => {
    try {
      const response = await api.get(`/notifications/${notificationId}/`);
      return response.data;
    } catch (error) {
      console.error('Ошибка при загрузке данных уведомления:', error);
      throw error;
    }
  }
};