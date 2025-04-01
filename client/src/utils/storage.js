import axios from "axios";
import Cookies from "js-cookie";

// Все функции для работы с Cookies
export async function getUserData() {
  let userData = Cookies.get("userData");

  // Проверяем, если данные есть, парсим их, если нет, создаем пустой объект
  if (userData) {
    try {
      userData = JSON.parse(userData);
    } catch (error) {
      console.error("Ошибка при парсинге userData из cookies:", error);
      userData = {}; // В случае ошибки парсинга, возвращаем пустой объект
    }
  } else {
    userData = {}; // Если данных нет, возвращаем пустой объект
  }

  // Если ID отсутствует, пробуем загрузить данные с API
  if (!userData.id) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
        headers: { Authorization: `Bearer ${Cookies.get("access")}` },
      });

      if (response.status === 200) {
        userData = {
          ...userData,
          id: response.data.id,
          institute: response.data.institute || "TYIU", // Берем институт из API
        };
        Cookies.set("userData", JSON.stringify(userData)); // Сохраняем данные в cookies
      }
    } catch (error) {
      console.error("Ошибка при получении данных о пользователе:", error);
    }
  }

  return userData;
}

// Функция обновления института в Cookies
export function updateInstitute(institute) {
  let userData = JSON.parse(Cookies.get("userData")) || {};
  userData.institute = institute;
  Cookies.set("userData", JSON.stringify(userData), { expires: 7 });
}

export function getAccessToken() {
  return Cookies.get("access");
}

export function getRefreshToken() {
  return Cookies.get("refresh");
}

export function saveUserData(userData) {
  Cookies.set("userData", JSON.stringify(userData), { expires: 7 });
}

export function saveTokens(access, refresh) {
  Cookies.set("access", access, { expires: 1 }); // Токен access хранится на 1 день
  Cookies.set("refresh", refresh, { expires: 7 }); // Токен refresh хранится на 7 дней
}

export function clearStorage() {
  Cookies.remove("access");
  Cookies.remove("refresh");
  Cookies.remove("userData");
}
