import api from "@/composables/auth";
import userService from "@/composables/storage.js"; // Единичный экземпляр UserService для работы с токенами и данными пользователя

/**
 * Получает имя инициатора (владельца идеи) по его ID.
 * Записывает в target.initiator строку "Имя Фамилия" или "Неизвестный автор", если данные отсутствуют.
 *
 * @param {Object} target - Объект, куда будет записано инициаторское имя.
 * @param {number|string} ownerId - ID пользователя.
 */
export async function fetchOwnerName(target, ownerId) {
  try {
    // Запрос через api — интерсепторы автоматически подставят актуальный токен
    const response = await api.get(`/users/${ownerId}/`);
    const { first_name, last_name } = response.data;
    target.initiator = (first_name && last_name)
      ? `${first_name} ${last_name}`
      : "Неизвестный автор";
  } catch (error) {
    console.error("Ошибка при загрузке инициатора:", error);
    target.initiator = "Неизвестный автор";
  }
}

/**
 * Обновляет лайк для идеи.
 * С учетом того, является ли пользователь экспертом (используем userService для получения роли),
 * выполняет запрос через api. В случае ошибки 403 (например, если токен устарел) — пытается обновить токен
 * и повторить запрос (однократно, чтобы избежать бесконечных циклов).
 *
 * @param {Object} idea - Объект идеи, который нужно обновить (содержит id, likes, likes_count и т.д.).
 * @param {Event} event - Событие, для остановки всплытия (например, click).
 * @param {boolean} liked - Текущее состояние: поставлен ли лайк пользователем.
 * @param {Function} isAnimatingSetter - Функция для установки состояния анимации (начало/конец анимации).
 * @param {Function} getUserId - Функция, возвращающая ID текущего пользователя.
 * @param {boolean} retry - Флаг, чтобы избежать бесконечных повторных попыток обновления токена.
 */
export async function toggleLike(
  idea,
  event,
  liked,
  isAnimatingSetter,
  getUserId,
  retry = false
) {
  event.stopPropagation();
  isAnimatingSetter(true);

  try {
    const role = userService.getUserRole();
    const isExpert = role === "EX";
    const isCustomerOrStudent = role === "CU" || role === "ST";

    const endpoint = isExpert
      ? `/projects/${idea.id}/expert_like/`
      : `/projects/${idea.id}/like/`;

    const payload = isExpert ? { expert_voted: true } : {};

    const response = await api.post(
      endpoint,
      payload,
      { headers: { "Content-Type": "application/json" } }
    );

    const userId = getUserId();

    // Обновляем лайки на основе их состояния на сервере
    if (liked) {
      idea.likes = idea.likes.filter((id) => id !== userId); // Убираем лайк
    } else {
      idea.likes.push(userId); // Добавляем лайк
    }

    // Обновляем количество лайков с сервера
    idea.likes_count = response.data.likes_count;

    if (isExpert) {
      idea.experts_voted_count = response.data.experts_voted_count;
      idea.approved = response.data.approved;
    }

    return idea; // Возвращаем обновленный объект идеи

  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);
    if (error.response?.status === 403 && !retry) {
      const newToken = await userService.refreshToken();
      if (newToken) {
        return await toggleLike(idea, event, liked, isAnimatingSetter, getUserId, true);
      } else {
        console.error("Не удалось обновить токен, требуется повторный вход.");
      }
    }
  } finally {
    setTimeout(() => {
      isAnimatingSetter(false);
    }, 300);
  }
}

export async function toggleOfferLike(
  offer,
  event,
  liked,
  isAnimatingSetter,
  getUserId,
  retry = false
) {
  event.stopPropagation();
  isAnimatingSetter(true);

  try {
    // исправлено: строка в кавычках
    const response = await api.post(`/offers/${offer.id}/like/`, null, {
      headers: { "Content-Type": "application/json" },
    });

    const userId = getUserId();
    if (liked) {
      offer.likes = offer.likes.filter((id) => id !== userId);
      localStorage.setItem(`liked_${offer.id}_${userId}`, "false");
    } else {
      offer.likes.push(userId);
      localStorage.setItem(`liked_${offer.id}_${userId}`, "true");
    }

    offer.likes_count = response.data.likes_count;

  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);

    if (error.response?.status === 403 && !retry) {
      const newToken = await userService.refreshToken();
      if (newToken) {
        await toggleOfferLike(offer, event, liked, isAnimatingSetter, getUserId, true);
      } else {
        console.error("Не удалось обновить токен, требуется повторный вход.");
      }
    }
  } finally {
    setTimeout(() => {
      isAnimatingSetter(false);
    }, 300);
  }
}
// Получить все проекты
export const getAllProjects = async () => {
  const response = await api.get("/projects/");
  return response.data;
};

// Получить проект по ID
export const getProjectById = async (id) => {
  const response = await api.get(`/projects/${id}/`);
  return response.data;
};

// Создать новый проект
export const createProject = async (projectData) => {
  const response = await api.post("/projects/", projectData);
  return response.data;
};

// Обновить проект
export const updateProject = async (id, projectData) => {
  const response = await api.put(`/projects/${id}/`, projectData);
  return response.data;
};

// Удалить проект
export const deleteProject = async (id) => {
  await api.delete(`/projects/${id}/`);
};