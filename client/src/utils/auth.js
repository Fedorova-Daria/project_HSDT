import axios from "axios";
import { saveTokens, getAccessToken, getRefreshToken, clearStorage } from "./storage.js";

// Обновление токена
export async function refreshToken() {
  try {
    const refreshToken = getRefreshToken();
    if (!refreshToken) throw new Error("Refresh token отсутствует");

    const response = await axios.post(
      "http://127.0.0.1:8000/api/users/token/refresh/",
      { refresh: refreshToken }
    );

    const newAccessToken = response.data.access;
    saveTokens(newAccessToken, refreshToken); // Сохраняем новый токен

    console.log("Access token успешно обновлен:", newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error("Ошибка обновления токена:", error);
    clearStorage(); // Чистим токены, чтобы избежать ошибок в будущем
    return null;
  }
}

// Получаем актуальный access-токен
export async function fetchAccessToken() {
  let token = getAccessToken();

  if (!token) {
    console.warn("Access token отсутствует. Пытаемся обновить...");
    token = await refreshToken(); // Обновляем токен
    if (!token) {
      console.error("Обновление токена не удалось. Требуется авторизация.");
      return null; // Возвращаем null, если обновление токена не удалось
    }
  }

  try {
    // Проверяем истечение токена
    const tokenPayload = JSON.parse(atob(token.split(".")[1]));
    const tokenExp = tokenPayload.exp; // Время истечения токена
    const currentTime = Math.floor(Date.now() / 1000);

    if (currentTime >= tokenExp) {
      console.log("Access token истёк. Обновляем...");
      token = await refreshToken(); // Попытка обновить токен
    }
  } catch (error) {
    console.error("Ошибка обработки токена:", error);
    return null;
  }

  return token; // Возвращаем актуальный или обновлённый токен
}
