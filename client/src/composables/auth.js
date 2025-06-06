import UserService from "@/composables/storage.js";
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000,
  withCredentials: true,  // Обязательно если используешь cookies
});

// Интерсептор запроса
api.interceptors.request.use(
  async (config) => {
    const token = UserService.getToken();  // Получаем токен из хранилища, если он есть
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.error("Токен не найден");
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Интерсептор ответа
api.interceptors.response.use(
  (response) => response,  // Если все в порядке, просто возвращаем ответ
  async (error) => {
    const originalRequest = error.config;

    // Обработка ошибки 401 (неавторизован)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Попробуем обновить токен
        const newToken = await UserService.refreshToken();

        if (newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          // Повторно выполняем запрос с новым токеном
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error("Ошибка при обновлении токена:", refreshError);
        UserService.clearStorage();  // Очистка данных пользователя
        window.location.href = "/login";  // Перенаправление на страницу входа
      }
    }

    return Promise.reject(error);
  }
);

export default api;