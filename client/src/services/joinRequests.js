import api from "@/composables/auth";
// Получить все заявки на вступление
export const fetchJoinRequests = async () => {
    const response = await api.get("/join-requests/");
    return response.data;
  };
  
  // Отправить заявку на вступление (нужно передать project_id или team_id, в зависимости от реализации)
  export const createJoinRequest = async (payload) => {
    const response = await api.post("/join-requests/", payload);
    return response.data;
  };
  
  // Получить конкретную заявку по ID
  export const getJoinRequestById = async (id) => {
    const response = await api.get(`/join-requests/${id}/`);
    return response.data;
  };
  
  // Принять заявку
  export const acceptJoinRequest = async (id) => {
    const response = await api.post(`/join-requests/${id}/accept/`);
    return response.data;
  };
  
  // Отменить заявку (POST)
  export const cancelJoinRequestPost = async (id) => {
    const response = await api.post(`/join-requests/${id}/cancel/`);
    return response.data;
  };
  
  // Отменить заявку (DELETE) — возможно для другой роли
  export const cancelJoinRequestDelete = async (id) => {
    const response = await api.delete(`/join-requests/${id}/cancel/`);
    return response.data;
  };