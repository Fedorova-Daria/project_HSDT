import api from "@/composables/auth"; // Используем уже настроенный axios

export const createIdeaOrProject = async (formData) => {
  const userData = JSON.parse(localStorage.getItem('userData'));
  const userRole = userData ? userData.role : null;
  const customer = userData ? userData.id : null;  // Получаем id пользователя из localStorage

  // Заполняем поле customer только если роль пользователя 'CU' или 'EX'
  if ((userRole === 'CU' || userRole === 'EX') && !formData.customer) {
    formData.customer = customer;
  }

  // Сбор данных в нужный формат
  const dataToSend = {
    title: formData.title,
    description: formData.description,
    status: formData.status,
    visible: formData.visible ?? false,
    technologies: (formData.technologies || []).map(Number),
    // Не включаем likes и expert_likes
  };
  
   // Добавляем поле customer только для ролей 'CU' и 'EX'
   if (userRole === 'CU' || userRole === 'EX') {
    dataToSend.customer = customer;
  }

  // Если роль студента (ST), исключаем поле customer
  if (userRole === 'ST') {
    delete dataToSend.customer;
  }

  console.log("Отправляемые данные:", dataToSend); // Логирование данных перед отправкой

  try {
    if (userRole === 'ST') {
      // Если роль студента (ST), создаем идею
      const response = await api.post("/ideas/", dataToSend);
      return response.data;
    } else if (userRole === 'CU' || userRole === 'EX') {
      // Если роль заказчика (CU) или эксперта (EX), создаем проект
      const response = await api.post("/projects/", dataToSend);
      return response.data;
    } else {
      throw new Error("Неверная роль пользователя");
    }
  } catch (error) {
    console.error("Ошибка при создании:", error.response ? error.response.data : error.message);
    throw error; // Перебрасываем ошибку
  }
};