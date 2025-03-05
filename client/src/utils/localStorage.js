export function getUserData() {
  return (
    JSON.parse(localStorage.getItem("userData")) || {
      name: "",
      surname: "",
      email: "",
      bio: "",
      avatar: "https://via.placeholder.com/150",
      group: "",
    }
  );
}

export function getToken() {
  return localStorage.getItem("token");
}

export function saveUserData(userData) {
  localStorage.setItem("userData", JSON.stringify(userData));
}

export function saveToken(token) {
  localStorage.setItem("token", token);
}

export function clearStorage() {
  localStorage.removeItem("token");
  localStorage.removeItem("userData");
}
