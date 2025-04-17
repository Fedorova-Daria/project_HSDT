import UserService from "@/composables/storage.js";
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000,
  withCredentials: true,
});

api.interceptors.request.use(
  async (config) => {
    // Перед каждым запросом принудительно обновляем токен
    // Обратите внимание: метод refreshToken должен посылать запрос к endpoint обновления token
    // и возвращать новый access token. Если обновление не удалось – можно выполнить очистку хранилища или
    // перенаправить пользователя на страницу логина.
    const newToken = await UserService.refreshToken();
    if (newToken) {
      config.headers.Authorization = `Bearer ${newToken}`;
    } else {
      console.error("Не удалось обновить токен");
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Интерсептор ответов остаётся стандартным для обработки ошибок 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await UserService.refreshToken();
      if (newToken) {
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      }
      UserService.clearStorage();
      // Дополнительно, можно перенаправить пользователя на логин.
    }
    return Promise.reject(error);
  }
);

export default api;