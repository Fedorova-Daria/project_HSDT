import axios from "axios";
import Cookies from "js-cookie";

// Все функции для работы с Cookies и LocalStorage
export async function getUserData() {
  let storedUserData = Cookies.get("userData");

  // Проверяем, если данные есть в cookies, парсим их, если нет, загружаем из localStorage
  if (!storedUserData) {
    storedUserData = localStorage.getItem("userData");
    if (storedUserData) {
      storedUserData = JSON.parse(storedUserData);
    } else {
      // Если данных нет, возвращаем пустой объект и дефолтный институт "TYIU"
      storedUserData = { institute: "TYIU" };
    }
  } else {
    try {
      storedUserData = JSON.parse(storedUserData); // Парсим данные из cookies
    } catch (error) {
      console.error("Ошибка при парсинге userData из cookies:", error);
      storedUserData = { institute: "TYIU" }; // В случае ошибки парсинга, возвращаем дефолтный институт "TYIU"
    }
  }

  // Если ID отсутствует, пробуем загрузить данные с API
  if (!storedUserData.id) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
        headers: { Authorization: `Bearer ${Cookies.get("access_token")}` },
      });

      if (response.status === 200) {
        storedUserData = {
          ...storedUserData,
          id: response.data.id,
          institute: response.data.institute || "TYIU", // Берем институт из API или используем дефолтное значение
        };
        // Обновляем cookies и localStorage
        saveUserData(storedUserData);
      }
    } catch (error) {
      console.error("Ошибка при получении данных о пользователе:", error);
    }
  }

  return storedUserData;
}

// Функция обновления института в Cookies и localStorage
export function updateInstitute(institute) {
  let userData = JSON.parse(Cookies.get("userData")) || {};
  userData.institute = institute;
  Cookies.set("userData", JSON.stringify(userData), { expires: 7 });
  localStorage.setItem("userData", JSON.stringify(userData)); // обновляем localStorage
}

export function getAccessToken() {
  return Cookies.get("access_token"); // или localStorage.getItem('access_token');
}

// Использование access token для запроса
export async function fetchUserData() {
  const accessToken = getAccessToken();
  if (!accessToken) {
    console.error("Access token отсутствует. Пожалуйста, авторизуйтесь.");
    return;
  }

  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    console.log("Данные пользователя:", response.data);
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  }
}

export function getRefreshToken() {
  return Cookies.get("refresh_token");
}

export function saveUserData(userData) {
  // Сохраняем данные в cookies и localStorage
  Cookies.set("userData", JSON.stringify(userData), { expires: 7 });
  localStorage.setItem("userData", JSON.stringify(userData)); // сохраняем в localStorage
}

export function saveTokens(accessToken, refreshToken) {
  Cookies.set('access_token', accessToken, { expires: 7 }); // Токен хранится 1 день
  Cookies.set('refresh_token', refreshToken, { expires: 7 }); // refresh токен хранится 7 дней
}

export function clearStorage() {
  Cookies.remove("access_token");
  Cookies.remove("refresh_token");
  Cookies.remove("userData");
  localStorage.removeItem("userData"); // также удаляем из localStorage
}
