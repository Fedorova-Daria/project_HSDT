<template>
  <div class="min-h-screen text-white flex flex-col">
    <!-- Хедер -->
    <Header />
    <!-- Основной контейнер профиля -->
    <div class="flex w-4/5 mx-auto mt-10 gap-6">
      <!-- Левый блок (Информация о пользователе) -->
      <div class="w-1/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <div class="text-center">
          <img
            class="w-32 h-32 rounded-full border-4 border-purple-400 mx-auto"
            :src="userData.avatar || 'https://via.placeholder.com/150'"
            alt="Аватар пользователя"
          />
          <h1
            v-if="userData.first_name && userData.last_name"
            class="text-2xl font-semibold mt-4"
          >
            {{ userData.first_name }} {{ userData.last_name }}
          </h1>
        </div>

        <div class="mt-5">
          <p class="text-sm flex justify-between text-white">
            <strong>Почта:</strong>
          </p>
          <div
            class="w-auto mt-2 bg-zinc-700 text-white text-sm rounded-lg p-2.5 border border-zinc-600"
          >
            {{ userData.email || "Не указано" }}
          </div>
          <p class="text-sm mt-2 flex justify-between text-white">
            <strong>Группа:</strong>
          </p>
          <div
            class="w-auto mt-2 bg-zinc-700 text-white text-sm rounded-lg p-2.5 border border-zinc-600"
          >
            {{ userData.group?.name || "Не указано" }}
          </div>
        </div>
        <!-- Кнопка для открытия модального окна -->
        <button
          @click="showModal = true"
          class="w-full mt-4 py-2 bg-purple-600 text-white rounded-lg transition duration-300 hover:bg-purple-500 hover:shadow-lg"
        >
          Редактировать профиль
        </button>
      </div>

      <!-- Правый блок (Проекты, команды, стек технологий, оценки) -->
      <div class="w-3/4 bg-zinc-700 p-6 rounded-2xl shadow-lg">
        <h2 class="text-2xl font-semibold mb-4">Информация о пользователе</h2>

        <div class="flex gap-10">
          <!-- Проекты -->
          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">Проекты</h3>
            <div class="mt-2">
              <table
                class="w-full border-collapse shadow-lg rounded-lg overflow-hidden"
              >
                <thead class="bg-zinc-800">
                  <tr>
                    <th class="p-3 text-left text-white">Название</th>
                    <th class="p-3 text-left text-white">Статус</th>
                    <th class="p-3 text-left text-white">Оценка</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="bg-zinc-600 transition-colors">
                    <td class="p-3 border-t border-zinc-200">
                      Проект "Паровозик" (пример)
                    </td>
                    <td class="p-3 border-t border-zinc-200">Окончено</td>
                    <td class="p-3 border-t border-zinc-200">5</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Стек технологий -->

          <div>
            <h3 class="text-xl font-semibold border-b pb-2 mb-3">
              Стеки технологий
            </h3>
            <ul>
              <li class="p-2 bg-gray-700 rounded-md mb-2"></li>
            </ul>
            <p>Нет командной активности</p>
          </div>
        </div>
        <!-- Команды -->
        <h3 class="mt-10 text-xl font-semibold border-b pb-2 mb-3">Команды</h3>
        <div class="mt-2">
          <table
            class="w-full border-collapse shadow-lg rounded-lg overflow-hidden"
          >
            <thead class="bg-border">
              <tr>
                <th class="p-3 text-left text-white">Название команды</th>
                <th class="p-3 text-left text-white">Дата вступления</th>
                <th class="p-3 text-left text-white">Дата ухода</th>
              </tr>
            </thead>
            <tbody>
              <tr class="bg-zinc-600 transition-colors">
                <td class="p-3 border-t border-zinc-200"></td>
                <td class="p-3 border-t border-zinc-200"></td>
                <td class="p-3 border-t border-zinc-200"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Модальное окно -->
    <div
      v-if="showModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-zinc-700 p-6 rounded-lg shadow-lg">
        <h2 class="text-purple-500 text-xl font-bold mb-4">
          Редактировать профиль
        </h2>
        <form
          @submit.prevent="updateProfile"
          class="w-full max-w-md p-6 border border-purple-400 rounded-lg bg-zinc-700 text-white"
        >
          <div class="form-group mb-4">
            <label for="email" class="font-bold text-purple-300">Email:</label>
            <input
              type="email"
              id="email"
              v-model="userData.email"
              required
              class="mt-1 block w-full p-2 border border-purple-400 rounded"
            />
          </div>
          <div class="form-group mb-4">
            <label for="bio" class="font-bold text-purple-300"
              >Немного о себе:</label
            >
            <textarea
              id="bio"
              v-model="userData.bio"
              maxlength="40"
              class="mt-1 block w-full p-2 border border-purple-400 rounded"
            ></textarea>
          </div>
          <button
            type="submit"
            class="w-full mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            Сохранить изменения
          </button>
        </form>

        <button
          @click="showModal = false"
          class="mt-4 p-2 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";
import { saveUserData, getUserData } from "@/utils/localStorage.js"; // Импортируем функцию для получения данных

export default {
  components: { Header },
  data() {
    return {
      // Скажу так, это надо чтобы выгружались данные и не было ошибок изначально, ибо если мы это удалим, то страничка тупо не показывается, так что я оставила ради
      //всего живого в этой странице, ну тупа заглушки такие вот, поэтому все норм)))
      userData: {
        avatar: "https://via.placeholder.com/150",
        first_name: "",
        last_name: "",
        email: "",
        group: { id: "", name: "Не указано" },
      },
      showModal: false,
    };
  },
  async mounted() {
    // теперь загружаем через моунтед потому что идет реально загрузка этих данных и теперь они более правильно загружаются
    this.userData = await getUserData(); // Дожидаемся загрузки данных
    console.log("Данные из localStorage:", this.userData);
  },
  // методы, тут только для обновления профиля и для показа плашки с обновлением данных, надо доделать такую функцию чтобы он запоминал, но это потом...
  methods: {
    updateProfile() {
      saveUserData(this.userData); // Логика для обновления профиля
      alert("Профиль обновлён!");
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
/* Немного мягче фон */
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
</style>
