import api from "@/composables/auth"; // Импортируем настроенный axios

export const fetchTechnologies = async () => {
  try {
    const response = await api.get("/core/technologies");
    return response.data;  // Возвращаем данные технологий
  } catch (error) {
    console.error("Ошибка при получении технологий:", error);
  }
};