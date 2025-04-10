import axios from "axios";
import { fetchAccessToken, refreshToken } from "./auth.js";  // Импортируем функции для работы с токенами
import { clearStorage } from "./storage.js";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Перехватчик запросов для добавления токена
api.interceptors.request.use(
  async (config) => {
    if (config.skipAuth) return config;

    const access_token = await fetchAccessToken(); // Получаем актуальный токен

    if (access_token) {
      config.headers.Authorization = `Bearer ${access_token}`;
    } else {
      console.warn("Нет access токена, запрос может не пройти.");
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик для обработки ошибок ответов
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Ставим флаг, чтобы не зациклиться

      console.warn("Ошибка 401, пытаемся обновить токен.");

      const newAccessToken = await refreshToken();

      if (newAccessToken) {
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return api(originalRequest); // Повторяем с новым токеном
      } else {
        console.warn("Не удалось обновить токен, очищаем токены.");
        clearStorage();
      }
    }

    return Promise.reject(error);
  }
);

export default api;