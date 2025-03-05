export function getUserData() {
  return (
    JSON.parse(localStorage.getItem("userData")) || {
      first_name: "",
      last_name: "",
      email: "",
      bio: "",
      avatar: "https://via.placeholder.com/150",
      group: { id: "", name: "" }, // Группа теперь объект, а не строка
    }
  );
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
  s;
}

export function clearStorage() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("userData");
}
