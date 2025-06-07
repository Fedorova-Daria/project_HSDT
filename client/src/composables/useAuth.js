import api from "@/composables/auth"; // Предварительно настроенный экземпляр axios
import router from "@/router"; // Импортируем роутер для редиректа после регистрации
import UserService from "@/composables/storage.js"; // Экземпляр UserService
import axios from "axios";

export function useAuth() {
  /**
   * Выполняет логин пользователя.
   * Очищает данные перед входом, отправляет запрос на аутентификацию,
   * сохраняет полученные токены и данные пользователя, затем возвращает данные.
   *
   * @param {string} email
   * @param {string} password
   * @returns {Promise<Object>} Объект с access-токеном и данными пользователя.
   */
  const login = async (email, password) => {
    try {
      UserService.clearStorage();
  
      const response = await axios.post("http://127.0.0.1:8000/api/users/login/", { email, password });
  
      // Проверяем наличие токенов
      if (!response.data.access_token || !response.data.refresh_token) {
        throw new Error("Ошибка авторизации: сервер не вернул токены");
      }
  
      const { access_token, refresh_token } = response.data;
      UserService.saveTokens(access_token, refresh_token);
  
      // Запрашиваем данные пользователя
      const userDataResponse = await api.get("/users/me/", {
        headers: { Authorization: `Bearer ${access_token}` },
        withCredentials: true,
      });
  
      const userData = userDataResponse.data;
      UserService.saveUserData(userData);
  
      return { access: access_token, ...userData };
    } catch (error) {
      console.error("Ошибка при входе:", error.response?.data || error);
  
      const message = error.response?.data?.message;
      if (message === "Invalid credentials") {
        throw new Error("Неверный email или пароль");
      }
      if (message === "Email not found") {
        throw new Error("Email не найден");
      }
      throw new Error("Ошибка при входе. Попробуйте позже.");
    }
  };

  /**
   * Регистрирует студента.
   * Отправляет данные регистрации, затем сохраняет токены,
   * если регистрация прошла успешно.
   *
   * @param {Object} params
   * @param {string} params.first_name
   * @param {string} params.last_name
   * @param {string} params.university
   * @param {string} params.email
   * @param {string} params.password
   * @returns {Promise<Object>} Данные, полученные в ответе от сервера.
   */
  const registerStudent = async ({
    first_name,
    last_name,
    university,
    email,
    password,
  }) => {
    try {
      // Отправляем данные по эндпоинту регистрации
      const response = await api.post("/users/registration/", {
        first_name,
        last_name,
        university_group,
        email,
        password,
      });

      console.log("Результат регистрации студента:", response.data);

      if (response.data.success) {
        const { access_token, refresh_token } = response.data;
        // Сохраняем токены
        UserService.saveTokens(access_token, refresh_token);
        
        // После успешной регистрации, выполняем вход
        await loginWithToken(access_token);
        return response.data;
      } else {
        throw new Error(
          "Ошибка при регистрации: " + (response.data.message || "Неизвестная ошибка")
        );
      }
    } catch (error) {
      console.error("Ошибка при регистрации студента:", error);
      if (error.response?.data?.email) {
        throw new Error("Пользователь с таким email уже существует");
      }
      throw new Error("Ошибка при регистрации студента");
    }
  };

  /**
   * Авторизует пользователя с использованием токена.
   * @param {string} accessToken
   */
  const loginWithToken = async (accessToken) => {
    try {
      // Устанавливаем токен в заголовки для использования в запросах
      api.defaults.headers.Authorization = `Bearer ${accessToken}`;

      // Получаем данные пользователя (если необходимо)
      const userResponse = await api.get("/users/me");
      UserService.saveUserData(userResponse.data);

      // Перенаправление на страницу аккаунта или профиля
      router.push("/TYIU/about");

    } catch (error) {
      console.error("Ошибка при авторизации с токеном:", error);
      alert("Ошибка при авторизации, попробуйте войти снова.");
    }
  };

  /**
   * Регистрирует заказчика.
   * Отправляет данные регистрации и, при успешной регистрации, перенаправляет на страницу логина.
   *
   * @param {Object} params
   * @param {string} params.first_name
   * @param {string} params.last_name
   * @param {string} params.company
   * @param {string} params.email
   * @param {string} params.password
   * @param {string} [params.role="CU"] Роль пользователя (по умолчанию "CU" — Customer).
   * @returns {Promise<void>}
   */
  const registerCustomer = async ({
    first_name,
    last_name,
    company,
    email,
    password,
    role = "CU",
  }) => {
    const data = {
      first_name,
      last_name,
      company,
      email,
      password,
      role,
    };

    try {
      await api.post("/users/registration/", data);
      router.push("/login");
    } catch (error) {
      if (error.response?.data?.email) {
        throw new Error("Пользователь с таким email уже существует");
      }
      throw new Error("Ошибка при регистрации заказчика");
    }
  };

  return {
    login,
    registerStudent,
    registerCustomer,
    loginWithToken, // Обязательно возвращаем loginWithToken
  };
}