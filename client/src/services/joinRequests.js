import api from "@/composables/auth";
import axios from "axios";
// Получить все заявки на вступление
export const fetchJoinRequestsByTeam = async (teamId) => {
  try {
    const response = await api.get(`/team-join-requests/?team=${teamId}`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при загрузке заявок для команды ${teamId}:`, error.response?.data || error);
    return [];
  }
};

  
  // Отправить заявку на вступление (нужно передать project_id или team_id, в зависимости от реализации)
  export const createJoinRequest = async (payload) => {
    const response = await api.post("/team-join-requests/", payload);
    return response.data;
  };
  
  // Получить конкретную заявку по ID
  export const getJoinRequestById = async (id) => {
    const response = await api.get(`/team-join-requests/${id}`);
    return response.data;
  };
  
  // Принять заявку
  export const acceptJoinRequest = async (id) => {
    const response = await api.post(`/team-join-requests/${id}/accept/`);
    return response.data;
  };
  
  // Отменить заявку (POST)
  export const cancelJoinRequestPost = async (id) => {
    const response = await api.post(`/team-join-requests/${id}/cancel/`);
    return response.data;
  };
  
  // Отменить заявку (DELETE) — возможно для другой роли
  export const cancelJoinRequestDelete = async (id) => {
    const response = await api.delete(`/team-join-requests/${id}/cancel/`);
    return response.data;
  };