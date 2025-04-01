import { createStore } from 'vuex';
import axios from 'axios';
import { fetchAccessToken } from './utils/auth.js'; // Подключаем fetchAccessToken из вашего файла auth.js

const store = createStore({
  state: {
    likedItems: {},
    ideas: [],  // Здесь храните все идеи, если это нужно для вашего проекта
  },
  mutations: {
    updateLike(state, { ideaId, liked, likesCount }) {
      // Обновляем состояние лайка для конкретной идеи
      state.likedItems[ideaId] = liked;
      
      // Обновляем количество лайков для этой идеи
      const idea = state.ideas.find(i => i.id === ideaId);
      if (idea) {
        idea.likes_count = likesCount;
      }
    },
  },
  actions: {
    async toggleLike({ commit, state }, { event, idea, retry = false }) {
      if (!event || !idea) {
        console.error("Не переданы параметры: event или idea");
        return;
      }
    
      event.stopPropagation();  // Останавливаем распространение события
    
      try {
        let accessToken = await fetchAccessToken();
    
        if (!accessToken) {
          console.error("Не удалось обновить токен. Авторизация требуется.");
          return;
        }
    
        const response = await axios.post(
          `http://localhost:8000/api/projects/${idea.id}/like/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
          }
        );
    
        const liked = !state.likedItems[idea.id];
        const likesCount = response.data.likes_count;
    
        commit('updateLike', { ideaId: idea.id, liked, likesCount });
    
        if (liked) {
          idea.likes.push(idea.userId); 
        } else {
          idea.likes = idea.likes.filter(id => id !== idea.userId);
        }
      } catch (error) {
        console.error("Ошибка при обновлении лайка:", error);
    
        if (error.response?.status === 403 && !retry) {
          console.log("Попытка обновления токена...");
          const newToken = await fetchAccessToken();
          if (newToken) {
            localStorage.setItem("access", newToken);
            await commit('toggleLike', { event, idea, retry: true });
          } else {
            console.error("Не удалось обновить токен, требуется повторный вход.");
          }
        }
      }
    },
  },
});

export default store;