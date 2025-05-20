import axios from "axios";
import Cookies from "js-cookie";

/**
 * Безопасно парсит JSON-строку.
 * @param {string} jsonString - Строка в формате JSON.
 * @param {*} fallback - Значение по умолчанию, если парсинг не удался.
 * @returns {*} Распарсенное значение или fallback.
 */
function safeParse(jsonString, fallback = null) {
  if (!jsonString) {
    return fallback;
  }
  try {
    return JSON.parse(jsonString);
  } catch (error) {
    console.error("Ошибка при парсинге JSON:", error);
    return fallback;
  }
}

/**
 * Класс UserService инкапсулирует всю логику работы с данными пользователя:
 * – сохранение и получение данных из Cookies и localStorage;
 * – запрос данных пользователя с API;
 * – обновление пользовательских данных;
 * – работа с access и refresh токенами.
 */
class UserService {
  constructor() {
    // Значения по умолчанию
    this.defaultData = { institute: "TYIU" };
    // Базовый URL API (настрой под своё окружение)
    this.apiBaseUrl = "http://127.0.0.1:8000/api";
  }

  /**
   * Извлекает сохранённые данные пользователя из Cookies или localStorage.
   *
   * @returns {Object} Объект с данными пользователя или дефолтными значениями.
   */
  getStoredUserData() {
    return (
      safeParse(Cookies.get("userData")) ||
      safeParse(localStorage.getItem("userData")) || { ...this.defaultData }
    );
  }

  /**
   * Сохраняет данные пользователя в Cookies и localStorage.
   *
   * @param {Object} userData - Объект с данными пользователя.
   */
  saveUserData(userData) {
    const dataString = JSON.stringify(userData);
    Cookies.set("userData", dataString, { expires: 7 });
    localStorage.setItem("userData", dataString);
  }

  /**
   * Получает актуальные данные пользователя.
   * Если идентификатор (id) отсутствует, запрашивает данные с API.
   *
   * @returns {Promise<Object>} Объект с данными пользователя.
   */
  async getUserData() {
    let userData = this.getStoredUserData();

    if (!userData.id) {
      const token = this.getAccessToken();
      if (!token) {
        console.error("Access token отсутствует. Необходима авторизация.");
        return userData;
      }
      try {
        const response = await axios.get(`${this.apiBaseUrl}/users/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 200 && response.data) {
          userData = {
            ...userData,
            id: response.data.id,
            email: response.data.email,
            username: response.data.username,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            company_name: response.data.company_name,
            university_group: response.data.university_group || null,
            role: response.data.role,
            phone: response.data.phone || null,
            bio: response.data.bio || null,
            skills: response.data.skills || [],
            avatar: response.data.avatar || null,
            created_at: response.data.created_at,
            institute: response.data.institute || this.defaultData.institute,
          };
          this.saveUserData(userData);
        }
      } catch (error) {
        console.error("Ошибка при получении данных о пользователе:", error);
      }
    }

    return userData;
  }

  /**
   * Обновляет значение института в сохранённых данных пользователя.
   *
   * @param {string} institute - Новое значение института.
   */
  updateInstitute(institute) {
    const userData = this.getStoredUserData();
    userData.institute = institute;
    this.saveUserData(userData);
  }

  /**
   * Возвращает access token, сохранённый в Cookies.
   *
   * @returns {string|undefined} Access token.
   */
  getAccessToken() {
    return Cookies.get("access_token");
  }

  /**
   * Возвращает refresh token из Cookies.
   *
   * @returns {string|null} Refresh token или null, если отсутствует.
   */
  getRefreshToken() {
    const token = Cookies.get("refresh_token");
    return token || null;
  }

  /**
   * Обновляет access token, используя refresh token.
   * Выполняет запрос к API для обновления токена, сохраняет и возвращает новый access token.
   *
   * @returns {Promise<string|null>} Новый access token, или null, если обновление не удалось.
   */
  async refreshToken() {
    try {
      const refresh = this.getRefreshToken();
      if (!refresh) {
        throw new Error("Refresh token отсутствует");
      }
      const response = await axios.post(
        `${this.apiBaseUrl}/users/token/refresh/`,
        { refresh }
      );
      if (response.status === 200 && response.data) {
        const newAccessToken = response.data.access;
        // Если API возвращает новый refresh token – сохраняем его, иначе оставляем текущий
        const newRefreshToken = response.data.refresh || refresh;
        this.saveTokens(newAccessToken, newRefreshToken);
        return newAccessToken;
      } else {
        throw new Error("Не удалось обновить токен");
      }
    } catch (error) {
      console.error(
        "Ошибка при обновлении токена:",
        error.response?.data || error.message
      );
      return null;
    }
  }

  /**
   * Сохраняет access и refresh токены в Cookies.
   *
   * @param {string} accessToken - Токен доступа.
   * @param {string} refreshToken - Refresh токен.
   */
  saveTokens(accessToken, refreshToken) {
    if (!refreshToken) {
      console.error("Попытка сохранить refresh token: получено undefined");
    }
    Cookies.set("access_token", accessToken, { expires: 7, sameSite: "Lax" });
    Cookies.set("refresh_token", refreshToken, { expires: 7, sameSite: "Lax" });
  }

  /**
   * Очищает все данные пользователя из Cookies и localStorage.
   */
  clearStorage() {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    Cookies.remove("userData");
    localStorage.removeItem("userData");
  }

  /**
   * Возвращает роль пользователя из сохранённых данных.
   *
   * @returns {string|null} Роль пользователя или null, если отсутствует.
   */
  getUserRole() {
    const userData = safeParse(Cookies.get("userData"), {}) || {};
    return userData.role || null;
  }

  /**
   * Демонстрационная функция для запроса и логирования данных пользователя.
   */
  async fetchUserDataAndLog() {
    const token = this.getAccessToken();
    if (!token) {
      console.error("Access token отсутствует. Невозможно получить данные.");
      return;
    }
    try {
      const response = await axios.get(`${this.apiBaseUrl}/users/me/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log("Данные пользователя:", response.data);
    } catch (error) {
      console.error("Ошибка при получении данных пользователя:", error);
    }
  }
}

// Экспортируем одиночный экземпляр для использования в приложении.
const userService = new UserService();
export default userService;
