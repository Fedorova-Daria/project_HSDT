<template>
    <div>
      <Header />
      <div class="w-4/5 mt-5 m-auto p-6 overflow-auto flex gap-3 items-start z-10">
        <h2 class="text-2xl text-white font-semibold mb-4">Редактирование проекта</h2>
        <form @submit.prevent="updateProject">
          <div class="mb-4">
            <label for="name" class="text-white">Название проекта</label>
            <input type="text" id="name" v-model="form.name" class="w-full p-2 text-white" />
          </div>
          <div class="mb-4">
            <label for="description" class="text-white">Описание</label>
            <textarea id="description" v-model="form.description" class="w-full p-2 text-white"></textarea>
          </div>
          <div class="mb-4">
            <label for="technologies" class="text-white">Технологии</label>
            <input type="text" id="technologies" v-model="form.technologies" class="w-full p-2" />
          </div>
          <div class="mb-4 ">
            <label for="status" class="text-white">Статус</label>
            <select id="status" v-model="form.status" class="w-full p-2 bg-white text-black">
              <option value="active">Активный</option>
              <option value="inactive">Неактивный</option>
            </select>
          </div>
          <button type="submit" class="text-white bg-blue-500 p-2 rounded-lg">Сохранить изменения</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import Header from "@/components/header.vue"
  export default {
    components: { Header },
    data() {
      return {
        form: {
          name: '',
          description: '',
          technologies: '',
          status: 'active'
        }
      };
    },
    mounted() {
      this.fetchProjectDetails();
    },
    methods: {
      async fetchProjectDetails() {
        try {
          const response = await fetch(`http://localhost:8000/api/projects/${this.$route.params.id}/`);
          const data = await response.json();
          this.form = {
            name: data.name,
            description: data.description,
            technologies: data.technologies.join(', '), // Предполагаем, что technologies это массив
            status: data.status
          };
        } catch (error) {
          console.error("Ошибка при загрузке проекта:", error);
        }
      },
      async updateProject() {
        try {
          const updatedData = {
            name: this.form.name,
            description: this.form.description,
            technologies: this.form.technologies.split(', ').map((tech) => parseInt(tech, 10)), // Преобразуем в массив чисел
            status: this.form.status
          };

          const response = await fetch(`http://localhost:8000/api/projects/${this.$route.params.id}/edit/`, {
            method: 'PUT', // или PATCH в зависимости от вашего метода
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access')}`,  // передаем токен из LocalStorage
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData)  // передаем данные проекта
          });

          if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
          }

          const data = await response.json();
          console.log("Проект обновлен:", data);
        } catch (error) {
          console.error("Ошибка при обновлении проекта:", error);
        }
      }
    }
  };
</script>