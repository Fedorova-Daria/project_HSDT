import api from "@/composables/auth"; // Предварительно настроенный экземпляр axios
import router from "@/router"; // Импортируем роутер для редиректа после регистрации
import UserService from "@/composables/storage.js"; // Экземпляр UserService

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
      // Очистка предыдущих данных, если они есть
      UserService.clearStorage();

      // Запрос аутентификации
      const response = await api.post("/users/login/", { email, password });
      const { access_token, refresh_token } = response.data;

      // Сохраняем полученные токены через UserService
      UserService.saveTokens(access_token, refresh_token);

      // Получаем расширенные данные пользователя
      const userDataResponse = await api.get("/users/me/", {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      const userData = userDataResponse.data;

      // Сохраняем данные пользователя для дальнейшего использования
      UserService.saveUserData(userData);

      return { access: access_token, ...userData };
    } catch (error) {
      const message = error.response?.data?.message;
      if (message === "Invalid credentials") {
        throw new Error("Неверный email или пароль");
      }
      if (message === "Email not found") {
        throw new Error("Email не найден");
      }
      throw new Error("Ошибка при входе");
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
        university,
        email,
        password,
      });

      console.log("Результат регистрации студента:", response.data);

      if (response.data.success) {
        const { access_token, refresh_token } = response.data;
        UserService.saveTokens(access_token, refresh_token);
        // Дополнительно можно сразу сохранить данные пользователя,
        // если они передаются в ответе, или запросить их потом отдельно.
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
  };
}
