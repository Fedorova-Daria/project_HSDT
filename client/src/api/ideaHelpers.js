import axios from "axios";
import { fetchAccessToken } from "@/api/auth.js";
import Cookies from "js-cookie";
// Получение имени инициатора
export async function fetchOwnerName(target, ownerId) {
  try {
    const response = await axios.get(`http://localhost:8000/api/users/${ownerId}/`);
    // Проверяем данные пользователя, и если они есть, формируем имя
    if (response.data.first_name && response.data.last_name) {
      target.initiator = `${response.data.first_name} ${response.data.last_name}`;
    } else {
      target.initiator = "Неизвестный автор";
    }
  } catch (error) {
    console.error("Ошибка при загрузке инициатора:", error);
    target.initiator = "Неизвестный автор"; // Если не удается получить данные
  }
}

// Обновление лайка с учётом роли эксперта
export async function toggleLike(
  idea,
  event,
  liked,
  isAnimatingSetter,
  getUserId,
  retry = false
) {
  event.stopPropagation();
  isAnimatingSetter(true); // Запускаем анимацию лайка

  try {
    let accessToken = Cookies.get("access");

    if (!accessToken) {
      accessToken = await fetchAccessToken();
      if (!accessToken) {
        console.error("Не удалось обновить токен. Авторизация требуется.");
        return;
      }
    }

    // Получение роли пользователя из Cookies
    const userData = JSON.parse(Cookies.get("userData")) || {};
    const isExpert = userData.role === "expert"; // Проверяем, является ли пользователь экспертом

    const response = await axios.post(
      `http://localhost:8000/api/projects/${idea.id}/like/`,
      {
        expert_voted: isExpert, // Передаём статус голосования эксперта
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      }
    );

    // Обновляем состояние лайка и количество лайков
    if (liked) {
      idea.likes = idea.likes.filter((id) => id !== getUserId());
    } else {
      idea.likes.push(getUserId());
    }
    idea.likes_count = response.data.likes_count;

    // Если пользователь является экспертом, обновляем дополнительные данные
    if (isExpert) {
      idea.experts_voted_count = response.data.experts_voted_count;
      idea.approved = response.data.approved;
    }
  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);

    if (error.response?.status === 403 && !retry) {
      console.log("Попытка обновления токена...");
      const newToken = await fetchAccessToken();
      if (newToken) {
        Cookies.set("access", newToken);
        await toggleLike(idea, event, liked, isAnimatingSetter, getUserId, true);
      } else {
        console.error("Не удалось обновить токен, требуется повторный вход.");
      }
    }
  } finally {
    setTimeout(() => {
      isAnimatingSetter(false); // Завершаем анимацию через 300 мс
    }, 300);
  }
}