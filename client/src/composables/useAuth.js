import api from "@/api/axiosInstance.js";
import { saveTokens, saveUserData, clearStorage } from "@/api/storage.js";
import axios from "axios";
export function useAuth() {
   // 🔐 Логин
   const login = async (email, password) => {
    try {
      clearStorage();  // Очистка перед логином
  
      const response = await axios.post("http://127.0.0.1:8000/api/users/login/", {
        email,
        password,
      });
  
      // Извлекаем токены из ответа
      const { access_token, refresh_token } = response.data;
      
      // Сохраняем токены
      saveTokens(access_token, refresh_token);
  
      // Пример запроса, использующего токен
      const userDataResponse = await axios.get("http://127.0.0.1:8000/api/users/me/", {
        headers: {
          Authorization: `Bearer ${access_token}`, // используем токен, полученный из ответа
        },
      });
  
      const userData = userDataResponse.data;
      saveUserData(userData);
  
      return {
        access: access_token,
        ...userData,
      };
    } catch (error) {
      const message = error.response?.data?.message;
      if (message === "Invalid credentials") throw new Error("Неверный email или пароль");
      if (message === "Email not found") throw new Error("Email не найден");
      throw new Error("Ошибка при входе");
    }
  };

  // 👨‍🎓 Регистрация студента
  const registerStudent = async ({
    first_name,
    last_name,
    group,
    email,
    password,
    role = "ST",
  }) => {
    const data = {
      first_name,
      last_name,
      group,
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
      throw new Error("Ошибка при регистрации студента");
    }
  };

  // 🧑‍💼 Регистрация заказчика
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
