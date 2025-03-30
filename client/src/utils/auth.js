import axios from "axios";
import { saveTokens, getAccessToken, getRefreshToken, getUserData, clearStorage } from "./localStorage.js"; // Убедись, что путь правильный

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
    saveTokens(newAccessToken, refreshToken); // Сохраняем новый access-токен

    console.log("Токен обновлен:", newAccessToken);

    // 🔹 **Обновляем данные пользователя после рефреша токена**
    await getUserData();

    return newAccessToken;
  } catch (error) {
    console.error("Ошибка обновления токена:", error);

    // Просто очищаем storage, но НЕ редиректим на /login
    clearStorage();

    return null; // Возвращаем null, чтобы обработка шла дальше
  }
}

// Функция для получения актуального access-токена
export async function fetchAccessToken() {
  let token = getAccessToken();

  if (!token) {
    console.warn("Access token отсутствует, требуется авторизация.");
    return null;
  }

  try {
    // Разбираем токен безопасно
    const tokenPayload = JSON.parse(atob(token.split(".")[1]));
    const tokenExp = tokenPayload.exp; // Время истечения токена
    const currentTime = Math.floor(Date.now() / 1000); // Текущее время

    if (currentTime >= tokenExp) {
      console.log("Access token истёк, обновляем...");
      token = await refreshToken(); // Обновляем токен
    }
  } catch (error) {
    console.error("Ошибка обработки access token:", error);
    return null;
  }

  return token; // Возвращаем актуальный или обновлённый токен
}