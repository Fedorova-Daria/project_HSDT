<template>
  <div>
    <Header />
    <navbar :ideaId="ideaId"/>

    <div class="p-4 m-auto w-4/5">
      <!-- Выбор команды -->
      <label class="text-white text-lg">Выберите команду:</label>
      <select v-model="selectedTeamId" @change="fetchTeamMembers" class="w-64 p-2 rounded bg-gray-800 text-white">
  <option v-for="team in teams" :key="team.id" :value="team.id">
    {{ team.name }}
  </option>
</select>

      <div v-if="teamMembers[selectedTeamId] && teamMembers[selectedTeamId].length" class="mt-4">
  <h2 class="text-white text-xl mb-2">Участники команды</h2>
  <ul>
    <li v-for="member in teamMembers[selectedTeamId]" :key="member.id" class="p-3 rounded mb-2 flex justify-between items-center">
      <div>
        <p class="text-white font-semibold">{{ member.full_name }}</p>
        <p class="text-gray-300">Средний рейтинг: {{ getParticipantRating(member.id) }}</p>
      </div>
      <!-- Выбор оценки -->
      <div class="radio">
        <input id="rating-5-{{member.id}}" type="radio" name="rating-{{member.id}}" value="5" v-model="selectedRatings[member.id]" />
        <label for="rating-5-{{member.id}}" title="5 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
          </svg>
        </label>

        <input id="rating-4-{{member.id}}" type="radio" name="rating-{{member.id}}" value="4" v-model="selectedRatings[member.id]" />
        <label for="rating-4-{{member.id}}" title="4 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-3-{{member.id}}" type="radio" name="rating-{{member.id}}" value="3" v-model="selectedRatings[member.id]" />
        <label for="rating-3-{{member.id}}" title="3 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-2-{{member.id}}" type="radio" name="rating-{{member.id}}" value="2" v-model="selectedRatings[member.id]"/>
        <label for="rating-2-{{member.id}}" title="2 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-1-{{member.id}}" type="radio" name="rating-{{member.id}}" value="1" v-model="selectedRatings[member.id]" />
        <label for="rating-1-{{member.id}}" title="1 star">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>
      </div>
      <!-- Кнопка "Поставить" -->
<button @click="rateParticipant(worker.id)" class="px-4 py-2 bg-blue-500 text-white rounded">
  Поставить
</button>
    </li>
  </ul>
</div>

<div v-if="freelancers.length" class="mt-6">
  <h2 class="text-white text-xl mb-2">Фрилансеры</h2>
  <ul>
    <li v-for="worker in freelancers" :key="worker.id" class="p-3 rounded mb-2 flex justify-between items-center">
      <div>
        <p class="text-white font-semibold">{{ worker.full_name }}</p>
        <p class="text-gray-300">Средний рейтинг: {{ getParticipantRating(worker.id) }}</p>
      </div>
      <!-- Выбор оценки -->
      <div class="radio">
        <input id="rating-5-{{worker.id}}" type="radio" name="rating-{{worker.id}}" value="5" v-model="selectedRatings[worker.id]" />
        <label for="rating-5-{{worker.id}}" title="5 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-4-{{worker.id}}" type="radio" name="rating-{{worker.id}}" value="4" v-model="selectedRatings[worker.id]" />
        <label for="rating-4-{{worker.id}}" title="4 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-3-{{worker.id}}" type="radio" name="rating-{{worker.id}}" value="3" v-model="selectedRatings[worker.id]" />
        <label for="rating-3-{{worker.id}}" title="3 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-2-{{worker.id}}" type="radio" name="rating-{{worker.id}}" value="2" v-model="selectedRatings[worker.id]" />
        <label for="rating-2-{{worker.id}}" title="2 stars">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>

        <input id="rating-1-{{worker.id}}" type="radio" name="rating-{{worker.id}}" value="1" v-model="selectedRatings[worker.id]" />
        <label for="rating-1-{{worker.id}}" title="1 star">
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
      ></path>
    </svg>
        </label>
      </div>
      <!-- Кнопка "Поставить" -->
<button @click="rateParticipant(worker.id)" class="px-4 py-2 bg-blue-500 text-white rounded">
  Поставить
</button>
    </li>
  </ul>
</div>
    </div>

  </div>
</template>

<script>
import Header from "@/components/header.vue";
import navbar from "@/components/in project/navbar.vue";
import api from "@/composables/auth.js";  

export default {
  name: "ProjectStats",
  components: { Header, navbar },
  props: {
    ideaId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
        selectedRatings: {},
        selectedTeamId: null, // Выбранная команда
        workers: [], 
        teams: [], 
        teamMembers: {}, 
        participantsRatings: {}, 
        participantsDetails: {}, 
        freelancers: []
    };
  },
  methods: {
    async fetchProjectData() {
  try {
    const response = await api.get(`/projects/${this.ideaId}/`);
    this.workers = response.data.workers;
    this.teams = response.data.teams; // Тут только ID команд

    await this.fetchTeamsInfo(); // Загружаем полные данные команд
    await this.fetchParticipantsDetails();
  } catch (error) {
    console.error("Ошибка загрузки проекта:", error);
  }
},
async fetchTeamsInfo() {
  try {
    const teamDetails = await Promise.all(
      this.teams.map(async (teamId) => { // teamId — уже ID команды
        const response = await api.get(`/teams/${teamId}`); // Передаем чистый ID
        return response.data;
      })
    );
    this.teams = teamDetails; // Теперь массив содержит объекты команд
  } catch (error) {
    console.error("❌ Ошибка загрузки информации о командах:", error);
  }
},
async fetchTeamMembers() {
  if (!this.selectedTeamId) return;

  try {
    const response = await api.get(`/teams/${this.selectedTeamId}`);
    this.teamMembers[this.selectedTeamId] = response.data.members || []; 
  } catch (error) {
    console.error("❌ Ошибка загрузки участников команды:", error);
  }
},
    onTeamChange() {
      if (!this.selectedTeamId) return;
      this.fetchTeamMembers(this.selectedTeamId);
      this.loadBoardForTeam(this.selectedTeamId);
    },

    async loadBoardForTeam(teamId) {
      try {
        const response = await api.get(`/kanban/boards/?team=${teamId}`);
        this.columns = response.data.columns;
      } catch (error) {
        console.error("Ошибка загрузки доски команды:", error);
      }
    },

    async fetchParticipantsDetails() {
      try {
        const response = await api.get(`/projects/${this.ideaId}/participants-details/`);
        this.participantsDetails = response.data;
      } catch (error) {
        console.error("Ошибка получения рейтинга участников:", error);
      }
    },

    async rateParticipant(userId) {
    if (!this.selectedRatings[userId]) {
      console.error(`❌ Оценка для пользователя ${userId} не выбрана`);
      return;
    }

    try {
      await api.post("/participant-ratings/", {
        rated_user: userId,
        rating: this.selectedRatings[userId], // Используем сохраненную оценку
        project: this.ideaId,
      });

      console.log(`✅ Оценка ${this.selectedRatings[userId]} успешно поставлена участнику ${userId}`);

      await this.fetchParticipantsDetails(); // Обновляем рейтинг
      this.selectedRatings[userId] = null; // Сбрасываем после отправки
    } catch (error) {
      console.error("❌ Ошибка при выставлении оценки:", error);
    }
  },
async fetchFreelancers() {
  try {
    const response = await api.get(`/projects/${this.ideaId}/`);
    
    // Загружаем фрилансеров из "workers"
    this.freelancers = response.data.workers.map(worker => ({
      id: worker.id,
      full_name: worker.full_name,
    }));

    console.log("✅ Загружены фрилансеры:", this.freelancers);
  } catch (error) {
    console.error("❌ Ошибка загрузки фрилансеров:", error);
  }
},
    getParticipantRating(userId) {
  if (!this.participantsDetails || !this.participantsDetails.workers) {
    return "Нет данных";
  }
  
  const worker = this.participantsDetails.workers.find(w => w.id === userId);
  return worker ? worker.average_rating : "Нет данных";
},
  },

  mounted() {
    this.fetchProjectData();
    this.fetchFreelancers();
  }
};
</script>

<style scoped>


/* From Uiverse.io by LeonKohli */ 
.radio {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-direction: row-reverse;
}

.radio > input {
  position: absolute;
  appearance: none;
}

.radio > label {
  cursor: pointer;
  font-size: 30px;
  position: relative;
  display: inline-block;
  transition: transform 0.3s ease;
}

.radio > label > svg {
  fill: #666;
  transition: fill 0.3s ease;
}

.radio > label::before,
.radio > label::after {
  content: "";
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: #ff9e0b;
  border-radius: 50%;
  opacity: 0;
  transform: scale(0);
  transition:
    transform 0.4s ease,
    opacity 0.4s ease;
  animation: particle-explosion 1s ease-out;
}

.radio > label::before {
  top: -15px;
  left: 50%;
  transform: translateX(-50%) scale(0);
}

.radio > label::after {
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%) scale(0);
}

.radio > label:hover::before,
.radio > label:hover::after {
  opacity: 1;
  transform: translateX(-50%) scale(1.5);
}

.radio > label:hover {
  transform: scale(1.2);
  animation: pulse 0.6s infinite alternate;
}

.radio > label:hover > svg,
.radio > label:hover ~ label > svg {
  fill: #ff9e0b;
  filter: drop-shadow(0 0 15px rgba(255, 158, 11, 0.9));
  animation: shimmer 1s ease infinite alternate;
}

.radio > input:checked + label > svg,
.radio > input:checked + label ~ label > svg {
  fill: #ff9e0b;
  filter: drop-shadow(0 0 15px rgba(255, 158, 11, 0.9));
  animation: pulse 0.8s infinite alternate;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.1);
  }
}

@keyframes particle-explosion {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
  100% {
    opacity: 0;
    transform: scale(0.5);
  }
}

@keyframes shimmer {
  0% {
    filter: drop-shadow(0 0 10px rgba(255, 158, 11, 0.5));
  }
  100% {
    filter: drop-shadow(0 0 20px rgba(255, 158, 11, 1));
  }
}

.radio > input:checked + label:hover > svg,
.radio > input:checked + label:hover ~ label > svg {
  fill: #e58e09;
}

.radio > label:hover > svg,
.radio > label:hover ~ label > svg {
  fill: #ff9e0b;
}

.radio input:checked ~ label svg {
  fill: #ffa723;
}
</style>