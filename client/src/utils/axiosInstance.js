import axios from "axios";
import { fetchAccessToken, refreshToken } from "./auth.js";  // Импортируем функции для работы с токенами
import { clearStorage } from "./storage.js";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Перехватчик запросов для добавления токена
api.interceptors.request.use(
  async (config) => {
    let token = await fetchAccessToken(); // Проверяем и обновляем токен

    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Добавляем токен в заголовки запроса
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
  (response) => response, // Если все хорошо, просто возвращаем ответ
  async (error) => {
    if (error.response?.status === 401) {
      console.warn("Ошибка 401, пытаемся обновить токен.");

      // Пытаемся обновить токен с помощью refresh-токена
      const newAccessToken = await refreshToken(); // Здесь вызывается функция обновления токена

      if (newAccessToken) {
        // Если новый токен был получен, повторяем запрос с новым токеном
        error.config.headers["Authorization"] = `Bearer ${newAccessToken}`;

        // Повторно выполняем запрос с новым токеном
        return axios(error.config);
      } else {
        console.warn("Не удалось обновить токен, очищаем токены.");
        clearStorage(); // Если обновить токен не удалось, очищаем все токены и данные
      }
    }

    return Promise.reject(error); // Если ошибка не 401, отклоняем запрос
  }
);

export default api;