import axios from "axios";

export async function getUserData() {
  let userData = JSON.parse(localStorage.getItem("userData")) || {
    first_name: "",
    last_name: "",
    email: "",
    bio: "",
    avatar: "https://via.placeholder.com/150",
    group: { id: "", name: "Не указано" },
  };

  // Если group — это ID (число), загружаем название группы
  if (typeof userData.group === "number") {
    try {
      const groupResponse = await axios.get(
        "http://127.0.0.1:8000/api/core/groups/list"
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
