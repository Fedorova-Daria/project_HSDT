import axios from 'axios';
import { fetchAccessToken } from './auth.js';

export async function joinTeam(teamId) {
  const access_token = await fetchAccessToken();
  if (!access_token) {
    console.error("Авторизация требуется.");
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/teams/${teamId}/join`, {}, {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    console.log('Заявка подана:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка подачи заявки:', error);
    throw error;
  }
}

export async function fetchJoinRequests(teamId) {
    const access_token = await fetchAccessToken();
    if (!access_token) {
      console.error("Авторизация требуется.");
      return;
    }
  
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/teams/${teamId}/requests`, {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      console.log('Заявки на вступление:', response.data);
      return response.data;
    } catch (error) {
      console.error('Ошибка получения заявок:', error);
      throw error;
    }
  }

export async function acceptRequest(teamId, requestId) {
  const access_token = await fetchAccessToken();
  if (!access_token) {
    console.error("Авторизация требуется.");
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/teams/${teamId}/accept/${requestId}`, {}, {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    console.log('Заявка принята:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка принятия заявки:', error);
    throw error;
  }
}

export async function denyRequest(teamId, requestId) {
  const access_token = await fetchAccessToken();
  if (!access_token) {
    console.error("Авторизация требуется.");
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/teams/${teamId}/deny/${requestId}`, {}, {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    console.log('Заявка отклонена:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка отклонения заявки:', error);
    throw error;
  }
}

export async function inviteUserById(teamId, userId) {
    const access_token = await fetchAccessToken();
    if (!access_token) {
      console.error("Авторизация требуется.");
      return;
    }
  
    try {
      const response = await axios.post(`http://127.0.0.1:8000/api/teams/${teamId}/join`, {
        user_id: userId // Передаем ID пользователя в теле запроса
      }, {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      console.log('Приглашение отправлено:', response.data);
      return response.data;
    } catch (error) {
      console.error('Ошибка отправки приглашения:', error.response?.data || error.message);
      throw error;
    }
  }

export async function deleteTeam(teamId) {
  const access_token = await fetchAccessToken();
  if (!access_token) {
    console.error("Авторизация требуется.");
    return;
  }

  try {
    const response = await axios.delete(`http://127.0.0.1:8000/api/teams/${teamId}/delete`, {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    console.log('Команда удалена:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка удаления команды:', error);
    throw error;
  }
}