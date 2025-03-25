// auth.js
import axios from "axios";

// Обновить токен
export async function refreshToken() {
  try {
    const refreshToken = localStorage.getItem("refresh"); // Получаем refresh-токен
    if (!refreshToken) throw new Error("Refresh token отсутствует");

    const response = await axios.post(
      "http://localhost:8000/api/users/token/refresh/",
      {
        refresh: refreshToken,
      }
    );

    localStorage.setItem("access", response.data.access); // Обновляем access-токен
    console.log("Токен обновлен:", response.data.access);
    return response.data.access;
  } catch (error) {
    console.error("Ошибка обновления токена:", error);
    alert("Сессия истекла. Авторизуйтесь заново.");
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login"; // Перенаправление на страницу входа
    return null;
  }
}

// Получение актуального токена (с обновлением если нужно)
export async function getAccessToken() {
  let token = localStorage.getItem("access");

  // Если токен истёк, обновляем его
  if (token) {
    const tokenExp = JSON.parse(atob(token.split(".")[1])).exp; // Получаем время истечения токена
    const currentTime = Math.floor(Date.now() / 1000); // Текущее время в секундах
    if (currentTime > tokenExp) {
      console.log("Токен истёк, обновляем...");
      token = await refreshToken(); // Обновляем токен
    }
  }

  return token;
}
