import axios from "axios";
import { saveTokens, getAccessToken, getRefreshToken, clearStorage } from "./storage.js";

// Обновление токена
export async function refreshToken() {
  try {
    const refreshToken = getRefreshToken();
console.log("refresh token from cookies:", refreshToken); // 🔍 посмотри, что тут
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