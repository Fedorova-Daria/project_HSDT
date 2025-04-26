// teamService.js
import api from "@/composables/auth.js"; // axios-инстанс с интерсепторами, настроенный для работы с токенами
import UserService from "@/composables/storage.js";

/**
 * Отправляет запрос для вступления в команду.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @returns {Promise<Object>} - Объект с данными ответа от сервера.
 */
export async function joinTeam(teamId) {
  try {
    // Получаем токен из хранилища (или декодируем его, если требуется)
    const token = UserService.getAccessToken();
    // Формируем payload с токеном (название поля "token" — пример, уточните у бэкенд-разработчика!)
    const payload = { token };
    // Обратите внимание на завершающий слэш, если требуется
    const response = await api.post(`/teams/${teamId}/join`, payload);
    return response.data;
  } catch (error) {
    console.error("Ошибка подачи заявки:", error.response?.data || error.message);
    throw error;
  }
}

/**
 * Получает список заявок на вступление в команду.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @returns {Promise<Object>} - Объект с данными заявок.
 */
export async function fetchJoinRequests(teamId) {
  try {
    const response = await api.get(`/teams/${teamId}/requests`);
    console.log("Заявки на вступление:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка получения заявок:", error);
    throw error;
  }
}

/**
 * Принимает заявку на вступление в команду.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @param {string|number} requestId - Идентификатор заявки.
 * @returns {Promise<Object>} - Объект с данными ответа от сервера.
 */
export async function acceptRequest(teamId, requestId) {
  try {
    const response = await api.post(`/teams/${teamId}/accept/${requestId}`);
    console.log("Заявка принята:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка принятия заявки:", error);
    throw error;
  }
}

/**
 * Отклоняет заявку на вступление в команду.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @param {string|number} requestId - Идентификатор заявки.
 * @returns {Promise<Object>} - Объект с данными ответа от сервера.
 */
export async function denyRequest(teamId, requestId) {
  try {
    const response = await api.post(`/teams/${teamId}/deny/${requestId}`);
    console.log("Заявка отклонена:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка отклонения заявки:", error);
    throw error;
  }
}

/**
 * Отправляет приглашение пользователю присоединиться к команде.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @param {string|number} userId - Идентификатор пользователя.
 * @returns {Promise<Object>} - Объект с данными ответа от сервера.
 */
export async function inviteUser(teamId, userId) {
  try {
    const response = await api.post(`/teams/${teamId}/invite/${userId}`);
    console.log("Пользователь приглашен:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка приглашения пользователя:", error);
    throw error;
  }
}

/**
 * Удаляет команду.
 *
 * @param {string|number} teamId - Идентификатор команды.
 * @returns {Promise<Object>} - Объект с данными ответа от сервера.
 */
export async function deleteTeam(teamId) {
  try {
    const response = await api.delete(`/teams/${teamId}/delete`);
    console.log("Команда удалена:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка удаления команды:", error);
    throw error;
  }
}
