import axios from "axios";
import { fetchAccessToken} from "./auth.js";
import { clearStorage } from "./storage.js";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Добавляем перехватчик запросов
api.interceptors.request.use(
  async (config) => {
    let token = await fetchAccessToken(); // Проверяем и обновляем токен

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.warn("Нет access токена, запрос может не пройти.");
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик для обработки 401 (если refresh тоже истёк)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      console.warn("Ошибка 401, очищаем токены.");
      clearStorage();
    }
    return Promise.reject(error);
  }
);

export default api;