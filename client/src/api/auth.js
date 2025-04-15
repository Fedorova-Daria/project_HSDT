import axios from "axios";
import { saveTokens, getAccessToken, getRefreshToken, clearStorage } from "./storage.js";
import Cookies from 'js-cookie'
// Обновление токена
export async function refreshToken() {
  const refresh = Cookies.get('refresh_token');
  if (!refresh) return null;

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/users/token/refresh/', { refresh });
    
    const newAccess = response.data.access;
    const newRefresh = response.data.refresh;

    // Сохраняем новые токены
    Cookies.set('access_token', newAccess, { secure: false, sameSite: 'Lax' });
    if (newRefresh) {
      Cookies.set('refresh_token', newRefresh, { secure: false, sameSite: 'Lax' });
    }

    // Сохраняем новые токены в localStorage
    localStorage.setItem("access_token", newAccess);
    if (newRefresh) {
      localStorage.setItem("refresh_token", newRefresh);
    }

    return newAccess;
  } catch (error) {
    console.error("Ошибка обновления токена:", error.response?.data || error);
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
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