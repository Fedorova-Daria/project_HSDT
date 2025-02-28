<template>
  <div class="flex items-center justify-center h-screen bg-zinc-700">
    <div
      class="w-full max-w-md p-6 border border-purple-400 rounded-lg bg-zinc-700 text-white"
    >
      <h1 class="text-purple-500 text-2xl font-bold mb-4">
        Профиль пользователя
      </h1>
      <form @submit.prevent="updateProfile">
        <div class="form-group mb-4">
          <label for="email" class="font-bold text-purple-300">Email:</label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            required
            class="mt-1 block w-full p-2 border border-purple-400 rounded"
          />
        </div>
        <div class="form-group mb-4">
          <label for="phone" class="font-bold text-purple-300">Телефон:</label>
          <input
            type="tel"
            id="phone"
            v-model="user.phone"
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
            v-model="user.bio"
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
        <button
          type="button"
          @click="goToProfile"
          class="w-full mt-2 p-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Отмена редактирования
        </button>
      </form>

      <h2 class="text-purple-500 text-xl font-bold mt-6">
        Информация о пользователе
      </h2>

      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Телефон:</strong> {{ user.phone }}</p>
      <p><strong>Немного о себе:</strong> {{ user.bio }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: "",
        surname: "",
        email: "",
        phone: "",
        bio: "",
        techStack: "",
      },
    };
  },
  methods: {
    updateProfile() {
      console.log("Профиль обновлен:", this.user);
      alert("Профиль успешно обновлен!");
    },
    cancelEdit() {
      this.user = {
        name: "",
        surname: "",
        email: "",
        phone: "",
        bio: "",
        techStack: "",
      };
    },
    goToProfile() {
      this.$router.push("/profile");
    },
  },
};
</script>
