import axios from "axios";
import { saveTokens, getAccessToken, getRefreshToken, clearStorage } from "./storage.js";

// Обновление токена
export async function refreshToken() {
  try {
    const refreshToken = Cookies.get("refresh_token"); // Напрямую берём токен из Cookies
    if (!refreshToken) {
      throw new Error("Refresh token отсутствует");
    }

    const response = await axios.post("/api/users/token/refresh/", { refresh: refreshToken });
    const newAccessToken = response.data.access;

    Cookies.set("access_token", newAccessToken, { expires: 7 });
    console.log("Токен успешно обновлён:", newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error("Ошибка обновления токена:", error.response?.data || error.message);
    return null;
  }
}

// Получаем актуальный access-токен
export async function fetchAccessToken() {
  let access_token = getAccessToken();

  if (!access_token) {
    console.warn("Access token отсутствует. Пытаемся обновить...");
    access_token = await refreshToken(); // Обновляем токен
    if (!access_token) {
      console.error("Обновление токена не удалось. Требуется авторизация.");
      return null;
    }
  }

  try {
    // ⛔ Проверка валидности структуры токена
    const parts = access_token.split("."); // Теперь используется access_token
    if (parts.length !== 3) throw new Error("Невалидный формат JWT токена");

    const tokenPayload = JSON.parse(atob(parts[1]));
    const tokenExp = tokenPayload.exp;
    const currentTime = Math.floor(Date.now() / 1000);

    if (currentTime >= tokenExp) {
      console.log("Access token истёк. Обновляем...");
      access_token = await refreshToken(); // Используем access_token, а не token
    }
  } catch (error) {
    console.error("Ошибка обработки токена:", error);
    return null;
  }

  return access_token; // Возвращаем актуальный access_token
}

let intervalId;

export function startBackgroundTokenRefresh() {
  intervalId = setInterval(async () => {
    const newAccessToken = await refreshToken();
    if (newAccessToken) {
      console.log("Токен обновлён на фоне:", newAccessToken);
    } else {
      console.error("Не удалось обновить токен, требуется повторная авторизация.");
    }
  }, 5 * 60 * 1000); // Проверяем каждые 5 минут
}

export function stopBackgroundTokenRefresh() {
  if (intervalId) {
    clearInterval(intervalId);
    console.log("Фоновое обновление токенов остановлено.");
  }
}