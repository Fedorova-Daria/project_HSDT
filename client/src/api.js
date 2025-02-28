import axios from "axios";

async function fetchGroups() {
  try {
    const response = await axios.get("URL_ТВОЕГО_API");
    const groups = response.data;
    console.log(groups); // Можно вывести в консоль для проверки

    // Здесь ты можешь обработать полученные данные, например, обновить состояние или передать в компонент
  } catch (error) {
    console.error("Ошибка при загрузке групп:", error);
  }
}
