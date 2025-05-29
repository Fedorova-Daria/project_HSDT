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
  // Останавливаем всплытие события (чтобы не возникали дополнительные проблемы)
  event.stopPropagation();
  isAnimatingSetter(true); // Запускаем анимацию лайка

  try {
    // Получаем роль пользователя из userService
    const isExpert = userService.getUserRole() === "EX";

    // Выполняем запрос через api; интерсепторы автоматически добавят актуальный Authorization header
    const response = await api.post(
      `/ideas/${idea.id}/like/`,
      { expert_voted: isExpert },
      { headers: { "Content-Type": "application/json" } }
    );

    // Обновляем массив лайков: если лайк уже поставлен, удаляем id, иначе добавляем его
    const userId = getUserId();
    if (liked) {
      idea.likes = idea.likes.filter((id) => id !== userId);
    } else {
      idea.likes.push(userId);
    }
    // Обновляем общее количество лайков
    idea.likes_count = response.data.likes_count;
    
    // Дополнительно, если пользователь — эксперт, обновляем сведения о голосовании экспертов
    if (isExpert) {
      idea.experts_voted_count = response.data.experts_voted_count;
      idea.approved = response.data.approved;
    }
  } catch (error) {
    console.error("Ошибка при обновлении лайка:", error);

    // Если ошибка 403 и это первая попытка (retry == false), пытаемся обновить токен и повторить запрос
    if (error.response?.status === 403 && !retry) {
      console.log("Попытка обновления токена...");
      const newToken = await userService.refreshToken();
      if (newToken) {
        // После обновления токена повторяем вызов toggleLike, выставляем retry в true чтобы не зациклиться
        await toggleLike(idea, event, liked, isAnimatingSetter, getUserId, true);
      } else {
        console.error("Не удалось обновить токен, требуется повторный вход.");
      }
    }
  } finally {
    // Завершаем анимацию через 300 мс
    setTimeout(() => {
      isAnimatingSetter(false);
    }, 300);
  }
}
// Получить все идеи
export const getAllIdeas = async () => {
    const response = await api.get("/ideas/");
    return response.data;
};

// Получить одну идею по ID
export const getIdeaById = async (id) => {
    const response = await api.get(`/ideas/${id}/`);
    return response.data;
};

// Создать новую идею
export const createIdea = async (ideaData) => {
    const response = await api.post("/ideas/", ideaData);
    return response.data;
};

// Обновить идею
export const updateIdea = async (id, ideaData) => {
    const response = await api.put(`/ideas/${id}/edit/`, ideaData);
    return response.data;
};

// Удалить идею
export const deleteIdea = async (id) => {
  await api.delete(`/ideas/${id}/`);
};