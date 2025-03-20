import axios from "axios";

export async function getUserData() {
  let userData = JSON.parse(localStorage.getItem("userData")) || {
    id: "",
    first_name: "",
    last_name: "",
    email: "",
    bio: "",
    role: "",
    avatar: "https://via.placeholder.com/150",
    group: { id: "", name: "Не указано" },
  };
  // Проверяем, есть ли в LocalStorage данные по ID
  if (!userData.id) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },
      });

      if (response.status === 200) {
        userData = { ...userData, id: response.data.id };
        localStorage.setItem("userData", JSON.stringify(userData));
      }
    } catch (error) {
      console.error("Ошибка при получении данных о пользователе:", error);
    }
  }
  // Если group — это ID (число), загружаем название группы
  if (typeof userData.group === "number") {
    try {
      const groupResponse = await axios.get(
        "http://127.0.0.1:8000/api/core/university_groups/list"
      );

      if (groupResponse.status === 200) {
        const groups = groupResponse.data;
        const userGroup = groups.find((g) => g.id === userData.group);

        if (userGroup) {
          userData.group = { id: userGroup.id, name: userGroup.name };
          localStorage.setItem("userData", JSON.stringify(userData)); // Сохраняем обновлённые данные
        }
      }
    } catch (error) {
      console.error("Ошибка загрузки группы:", error);
    }
  }

  return userData;
}

export function getAccessToken() {
  return localStorage.getItem("access");
}

export function getRefreshToken() {
  return localStorage.getItem("refresh");
}

export function saveUserData(userData) {
  localStorage.setItem("userData", JSON.stringify(userData));
}

export function saveTokens(access, refresh) {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
}

export function clearStorage() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("userData");
}
