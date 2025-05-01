// projectRequests.js

import api from "@/composables/auth";

/**
 * Создать заявку на работу над проектом.
 * @param {Object} applicationData - Данные заявки:
 *   {
 *     applicant_type: "freelancer" | "team",
 *     project: <Id>,
 *     freelancer: <Id> // если заявка подается отдельным человеком,
 *     team: <Id>       // если заявку подает owner команды (команды получаются через GET /teams/)
 *   }
 * @returns {Promise<Object>} - Данные созданной заявки.
 */
export const createProjectApplication = async (applicationData) => {
  try {
    const response = await api.post("/project-applications/", applicationData);
    return response.data;
  } catch (error) {
    console.error("Ошибка при создании заявки:", error);
    throw error;
  }
};

/**
 * Получить все заявки на работу над проектами.
 * Ответ содержит массив объектов заявки с полями:
 * { id, applicant_type, status [ pending, accepted, rejected, cancelled ], created_at, project, freelancer, team }
 * @returns {Promise<Array>} - Массив заявок.
 */
export const getProjectApplications = async () => {
  try {
    const response = await api.get("/project-applications/");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении заявок:", error);
    throw error;
  }
};

/**
 * Получить заявку по ID.
 * @param {Number | String} id - Идентификатор заявки.
 * @returns {Promise<Object>} - Данные заявки.
 */
export const getProjectApplicationById = async (id) => {
  try {
    const response = await api.get(`/project-applications/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при получении заявки с id ${id}:`, error);
    throw error;
  }
};

/**
 * Отменить заявку по ID через метод DELETE.
 * Используется для того, чтобы человек мог отменить свою заявку.
 * @param {Number | String} id - Идентификатор заявки.
 * @returns {Promise<Object>} - Результат запроса.
 */
export const deleteProjectApplication = async (id) => {
  try {
    const response = await api.delete(`/project-applications/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при отмене заявки с id ${id}:`, error);
    throw error;
  }
};

/**
 * Принять заявку.
 * Выполняется POST-запрос на /project-applications/{id}/accept/.
 * Передаваемые данные аналогичны параметрам при создании заявки:
 * { applicant_type, project, freelancer, team }
 * @param {Number | String} id - Идентификатор заявки.
 * @param {Object} acceptData - Данные для принятия заявки.
 * @returns {Promise<Object>} - Результат запроса.
 */
export const acceptProjectApplication = async (id, acceptData) => {
  try {
    const response = await api.post(`/project-applications/${id}/accept/`, acceptData);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при принятии заявки с id ${id}:`, error);
    throw error;
  }
};

/**
 * Отменить заявку через POST-запрос на /project-applications/{id}/cancel/.
 * @param {Number | String} id - Идентификатор заявки.
 * @param {Object} [cancelData={}] - Дополнительные данные для отмены, если требуются.
 * @returns {Promise<Object>} - Результат запроса.
 */
export const cancelProjectApplication = async (id, cancelData = {}) => {
  try {
    const response = await api.post(`/project-applications/${id}/cancel/`, cancelData);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при отмене заявки с id ${id}:`, error);
    throw error;
  }
};