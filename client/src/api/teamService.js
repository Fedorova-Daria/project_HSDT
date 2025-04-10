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
      const response = await axios.get(`/api/teams/${teamId}/requests`, {
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

export async function inviteUser(teamId, userId) {
  const access_token = await fetchAccessToken();
  if (!access_token) {
    console.error("Авторизация требуется.");
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/teams/${teamId}/invite/${userId}`, {}, {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    console.log('Пользователь приглашен:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка приглашения пользователя:', error);
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