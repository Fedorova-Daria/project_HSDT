<template>
    <div>
      <Header/>
      <div class="w-4/5 mt-5 m-auto p-6 overflow-auto flex gap-3 items-start z-10">
        <button   @click="goBack"
      class="ml-auto bg-buttonoff hover:bg-buttonon text-white font-medium rounded-lg text-sm px-4 py-2 mt-5 duration-300 h-10"
    >
    <svg width="13" height="10" viewBox="0 0 13 10" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M5.27934 8.23871C5.35303 8.30737 5.41213 8.39017 5.45312 8.48217C5.49411 8.57417 5.51616 8.67348 5.51793 8.77418C5.51971 8.87489 5.50118 8.97492 5.46346 9.0683C5.42574 9.16169 5.3696 9.24653 5.29838 9.31774C5.22716 9.38896 5.14233 9.44511 5.04894 9.48283C4.95555 9.52055 4.85552 9.53907 4.75482 9.5373C4.65412 9.53552 4.5548 9.51348 4.4628 9.47249C4.3708 9.4315 4.288 9.37239 4.21934 9.29871L0.21934 5.29871C0.0788892 5.15808 -1.99759e-07 4.96746 -2.08447e-07 4.76871C-2.17135e-07 4.56996 0.0788892 4.37933 0.21934 4.23871L4.21934 0.238705C4.288 0.165019 4.3708 0.105917 4.4628 0.064925C4.5548 0.023933 4.65411 0.00189198 4.75482 0.000115187C4.85552 -0.0016616 4.95555 0.0168623 5.04894 0.0545833C5.14233 0.0923043 5.22716 0.148449 5.29838 0.219668C5.3696 0.290887 5.42574 0.375721 5.46346 0.469109C5.50118 0.562497 5.51971 0.662525 5.51793 0.763228C5.51615 0.863931 5.49411 0.963245 5.45312 1.05524C5.41213 1.14724 5.35303 1.23004 5.27934 1.29871L2.55934 4.01871L12.2493 4.01871C12.4483 4.01871 12.639 4.09772 12.7797 4.23838C12.9203 4.37903 12.9993 4.56979 12.9993 4.76871C12.9993 4.96762 12.9203 5.15838 12.7797 5.29904C12.639 5.43969 12.4483 5.51871 12.2493 5.51871L2.55934 5.51871L5.27934 8.23871Z" fill="white"/>
  </svg>
    </button>
  
  
        <div class="w-1/4 mt-5 bg-card rounded-lg p-6 flex flex-col" style="height: 300px;">
    <div class="flex-grow overflow-auto">
  
      <h2 v-if="!isEditing" class="text-2xl text-white font-semibold mb-4">
      {{ idea.title || "Загрузка..." }}
    </h2>
    <input
      v-else
      v-model="editedIdea.title"
      class="w-full text-2xl text-black bg-gray-100 rounded-md p-2"
    />
  
      <h3 class="text-xl text-white font-semibold mb-2">
        Инициатор: {{ idea.initiator || "Неизвестный автор" }}
      </h3>
  
      <p class="text-gray-400">Дата создания: {{ new Date(idea.created_at).toLocaleDateString("ru-RU") }}</p>
    </div>
  
    <!-- Блок с иконками теперь прижат к низу -->
    <div class="mt-auto flex justify-between">
      <div class="flex justify-start gap-2">
        <span class="text-white">{{ idea.likes ? idea.likes.length : 0 }}</span>
        <img
    :src="liked ? '/liked.svg' : '/like.svg'"
    alt="Like"
    class="w-6 h-6 mr-2 duration-300 cursor-pointer"
    :class="{ 'animate-like': isAnimating }"
    @click.stop="updateLike"
  />
      </div>
      
  <div class="mt-auto flex justify-end gap-5">
      <img v-if="isOwner" @click="toggleEditing" class="w-6 h-6 cursor-pointer" src="/pencil1.svg"/>
      <button
      v-if="isEditing && isOwner"
      @click="saveAllChanges"
      class="w-6 h-6 cursor-pointer"
    ><svg width="23" height="23" viewBox="0 0 12 9" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M11.7 0.7C11.3134 0.3134 10.6866 0.313401 10.3 0.7L4.2 6.8L2.1 4.7C1.7134 4.3134 1.0866 4.3134 0.7 4.7V4.7C0.313401 5.0866 0.3134 5.7134 0.699999 6.1L2.78579 8.18579C3.56683 8.96683 4.83316 8.96683 5.61421 8.18579L11.7 2.1C12.0866 1.7134 12.0866 1.0866 11.7 0.7V0.7Z" fill="white"/>
  </svg>
  </button>
      <button  v-if="isOwner" class="h-6 w-6"><svg width="22" height="22" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M5.5 1H8.5C8.63261 1 8.75979 1.05268 8.85355 1.14645C8.94732 1.24021 9 1.36739 9 1.5V2.5H5V1.5C5 1.36739 5.05268 1.24021 5.14645 1.14645C5.24021 1.05268 5.36739 1 5.5 1ZM10 2.5V1.5C10 1.10218 9.84196 0.720644 9.56066 0.43934C9.27936 0.158035 8.89782 0 8.5 0L5.5 0C5.10218 0 4.72064 0.158035 4.43934 0.43934C4.15804 0.720644 4 1.10218 4 1.5V2.5H0.5C0.367392 2.5 0.240215 2.55268 0.146447 2.64645C0.0526784 2.74021 0 2.86739 0 3C0 3.13261 0.0526784 3.25979 0.146447 3.35355C0.240215 3.44732 0.367392 3.5 0.5 3.5H1.038L1.891 14.16C1.93122 14.6612 2.15875 15.1289 2.52827 15.4698C2.8978 15.8108 3.38219 16.0001 3.885 16H10.115C10.6178 16.0001 11.1022 15.8108 11.4717 15.4698C11.8412 15.1289 12.0688 14.6612 12.109 14.16L12.962 3.5H13.5C13.6326 3.5 13.7598 3.44732 13.8536 3.35355C13.9473 3.25979 14 3.13261 14 3C14 2.86739 13.9473 2.74021 13.8536 2.64645C13.7598 2.55268 13.6326 2.5 13.5 2.5H10ZM11.958 3.5L11.112 14.08C11.0919 14.3306 10.9781 14.5644 10.7934 14.7349C10.6086 14.9054 10.3664 15.0001 10.115 15H3.885C3.6336 15.0001 3.3914 14.9054 3.20664 14.7349C3.02188 14.5644 2.90811 14.3306 2.888 14.08L2.042 3.5H11.958ZM4.471 4.5C4.60333 4.49235 4.73329 4.53756 4.8323 4.6257C4.93131 4.71383 4.99127 4.83767 4.999 4.97L5.499 13.47C5.50425 13.6008 5.45802 13.7284 5.37022 13.8255C5.28242 13.9225 5.16006 13.9813 5.02941 13.9892C4.89876 13.997 4.77024 13.9533 4.67144 13.8675C4.57265 13.7816 4.51145 13.6605 4.501 13.53L4 5.03C3.99594 4.96431 4.00489 4.89847 4.02633 4.83625C4.04777 4.77403 4.08129 4.71665 4.12495 4.66741C4.16862 4.61817 4.22158 4.57804 4.28079 4.54931C4.34 4.52058 4.4043 4.50382 4.47 4.5H4.471ZM9.529 4.5C9.5947 4.50382 9.659 4.52058 9.71821 4.54931C9.77742 4.57804 9.83038 4.61817 9.87405 4.66741C9.91771 4.71665 9.95123 4.77403 9.97267 4.83625C9.99411 4.89847 10.0031 4.96431 9.999 5.03L9.499 13.53C9.49633 13.5964 9.48043 13.6617 9.45224 13.7219C9.42405 13.7821 9.38413 13.8361 9.33481 13.8807C9.28549 13.9254 9.22777 13.9597 9.16503 13.9817C9.10228 14.0037 9.03578 14.013 8.9694 14.009C8.90302 14.005 8.8381 13.9878 8.77845 13.9585C8.7188 13.9291 8.6656 13.8881 8.62199 13.8379C8.57837 13.7877 8.5452 13.7293 8.52443 13.6661C8.50365 13.603 8.49569 13.5363 8.501 13.47L9.001 4.97C9.00873 4.83767 9.06869 4.71383 9.1677 4.6257C9.26671 4.53756 9.39667 4.49235 9.529 4.5ZM7 4.5C7.13261 4.5 7.25979 4.55268 7.35355 4.64645C7.44732 4.74021 7.5 4.86739 7.5 5V13.5C7.5 13.6326 7.44732 13.7598 7.35355 13.8536C7.25979 13.9473 7.13261 14 7 14C6.86739 14 6.74021 13.9473 6.64645 13.8536C6.55268 13.7598 6.5 13.6326 6.5 13.5V5C6.5 4.86739 6.55268 4.74021 6.64645 4.64645C6.74021 4.55268 6.86739 4.5 7 4.5Z" fill="white"/>
  </svg>
  </button>
  </div>
    </div>
  </div>
      <div class="w-3/4 mt-5 bg-card rounded-lg p-6 overflow-auto"  style="height: auto; max-height: 100vh; overflow-y: auto;">
        <h2 class="text-2xl text-white font-semibold mb-4">Описание идеи</h2>
    <p v-if="!isEditing" class="text-gray-400">
      {{ idea.description }}
    </p>
    <textarea
      v-else
      v-model="editedIdea.description"
      class="w-full bg-gray-100 rounded-md p-2"
    ></textarea>
    <div v-if="isEditing">
    <label for="status">Статус:</label>
    <select
      id="status"
      v-model="editedIdea.status"
      @change="updateStatus"
      class="w-full bg-gray-100 rounded-md p-2"
    >
      <option value="">Не задан</option>
      <option value="active">Активный</option>
      <option value="completed">Завершён</option>
      <option value="paused">Приостановлен</option>
    </select>
    </div>
      </div>
      </div>
      <div class="w-4/5 m-auto">
      <button
              @click="handleIdeaToProject"
              class="text-white ml-20 inline-flex items-center bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-800"
            >
              <svg
                class="me-1 -ms-1 w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Взять как проект
            </button>
          </div>
    </div>
  </template>
  
  <script>
  import api from "@/composables/auth.js"; // axios-инстанс с интерсепторами
  import Header from "@/components/header.vue";
  import { fetchOwnerName, toggleLike } from "@/services/projects.js";
  import Cookies from "js-cookie";
  
  export default {
    name: "IdeaDetails",
    components: { Header },
    props: {
      ideaId: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        idea: {}, // Загруженные данные идеи
        editedIdea: {
          name: "",
          description: "",
          technologies: [],
          is_hiring: false,
          status: "", // Статус идеи
        },
        isEditing: false,  // Режим редактирования включен/выключен
        isAnimating: false, // Состояние анимации лайка
      };
    },
    computed: {
      /**
       * Получаем данные пользователя из Cookies один раз.
       */
      currentUser() {
        return JSON.parse(Cookies.get("userData") || "{}");
      },
      /**
     * Определяет, поставил ли пользователь лайк.
     */
    liked() {
      if (!this.idea || !this.idea.likes || !this.currentUser || !this.currentUser.id) return false;
  
      // Загружаем состояние лайка из localStorage
      const userId = this.currentUser.id;
      const likedInStorage = localStorage.getItem(`liked_${this.idea.id}_${userId}`);
      
      if (likedInStorage !== null) {
        // Если лайк был сохранен в localStorage, используем это состояние
        return likedInStorage === 'true';
      }
  
      // Если лайк не сохранен, проверяем, есть ли id текущего пользователя в массиве лайков
      return this.idea.likes.includes(userId);
    },
      /**
       * Определяет, является ли текущий пользователь владельцем идеи.
       */
      isOwner() {
        return this.idea.owner && this.idea.owner === this.currentUser.id;
      },
      /**
       * Права на редактирование доступны владельцу.
       */
      hasEditAccess() {
        return this.isOwner;
      },
    },
    watch: {
      ideaId: {
        immediate: true,
        handler(newId) {
          console.log("Получен новый ideaId:", newId);
          if (newId) {
            this.fetchIdeaDetails(newId);
          }
        },
      },
    },
    methods: {
  /**
   * Переносит идею из API `/ideas/` в проект через API `/projects/` и обновляет статус идеи.
   * @param {String} ideaId - ID идеи.
   * @param {String} customerId - ID кастомера.
   */
   async transferIdeaToProject(ideaId, customerId) {
    try {
      // Шаг 1: Получаем данные идеи из API `/ideas/{ideaId}/`
      const ideaResponse = await api.get(`/ideas/${ideaId}/`);
      const ideaData = ideaResponse.data;

      // Формируем объект проекта
      const projectData = {
        title: ideaData.title || "Название проекта отсутствует",
        description: ideaData.description || "Нет описания",
        status: ideaData.status || "Draft",
        visible: true,
        duration: ["semester", "year"].includes(ideaData.duration) ? ideaData.duration : "semester",
        customer: customerId,
        selected_team: null,
        skills_required: ideaData.technologies?.map((tech) => tech.id).filter(Boolean) || [],
      };

      // Шаг 2: Создаём проект через API `/projects/`
      const projectResponse = await api.post(`/projects/`, projectData, {
        headers: { "Content-Type": "application/json" },
      });
      console.log("Проект успешно создан:", projectResponse.data);

      // Шаг 3: Обновляем статус идеи
      const updatedStatus = { status: "under_review" };
      await api.patch(`/ideas/${ideaId}/`, updatedStatus, {
        headers: { "Content-Type": "application/json" },
      });
      console.log("Статус идеи обновлён на 'under_review'");

      // Уведомление об успехе
      this.$toast.success("Идея успешно перенесена в проект и статус обновлён!");
      return projectResponse.data;
    } catch (error) {
      console.error("Ошибка при переносе идеи в проект:", error.response?.data || error);

      // Уведомление об ошибке
      const errorMessage = Object.values(error.response?.data || {})
        .flat()
        .join(", ") || "Не удалось перенести идею в проект.";
      this.$toast.error(errorMessage);
      throw error;
    }
  },
  /**
   * Обрабатывает перенос идеи в проект.
   */
  async handleIdeaToProject() {
    try {
      const customerId = this.currentUser.id; // ID текущего пользователя (кастомер)
      const project = await this.transferIdeaToProject(this.ideaId, customerId);
      console.log("Проект создан и статус идеи обновлён:", project);
    } catch (error) {
      console.error("Ошибка при обработке переноса:", error);
    }
  },
      /**
       * Переключает режим редактирования. При входе в режим редактирования копирует текущие данные идеи.
       */
      toggleEditing() {
        if (!this.hasEditAccess) {
          alert("У вас нет прав на редактирование этой идеи!");
          return;
        }
        this.isEditing = !this.isEditing;
        if (this.isEditing) {
          // Копирование данных идеи для редактирования
          this.editedIdea.title = this.idea.title;
          this.editedIdea.description = this.idea.description;
          // Копирование массивов копированием через spread необходимо для независимости
          this.editedIdea.technologies = [...(this.idea.technologies || [])];
          this.editedIdea.is_hiring = this.idea.is_hiring || false;
          this.editedIdea.status = this.idea.status ?? "";
        }
      },
      /**
       * Сохраняет изменения идеи через API.
       * Используется axios-инстанс из auth.js, поэтому токен обновляется автоматически.
       */
      async saveAllChanges() {
        try {
          // Формируем payload, исключая пустые строки для статуса
          const payload = {
            ...(this.editedIdea.title && { name: this.editedIdea.title }),
            ...(this.editedIdea.description && { description: this.editedIdea.description }),
            ...(this.editedIdea.technologies && { technologies: this.editedIdea.technologies }),
            is_hiring: this.editedIdea.is_hiring,
            status: this.editedIdea.status || null,
          };
          console.log("Payload перед отправкой:", payload);
  
          const response = await api.patch(`/ideas/${this.idea.id}/edit/`, payload, {
            headers: { "Content-Type": "application/json" },
          });
          console.log("Изменения сохранены:", response.data);
          // Можно обновить или перезагрузить данные идеи после сохранения:
          this.fetchIdeaDetails(this.idea.id);
        } catch (error) {
          console.error("Ошибка при сохранении:", error.response?.data || error);
        }
      },
      /**
       * Загружает данные идеи по её ID через api-инстанс.
       */
      async fetchIdeaDetails(id) {
        try {
          const response = await api.get(`/ideas/${id}/`);
          this.idea = response.data;
          console.log("Полученные данные проекта:", this.idea);
  
          if (!this.idea.owner) {
            console.warn("Поле owner отсутствует в данных проекта! Проверить API.");
            this.idea.initiator = "Неизвестный автор";
            return;
          }
          await this.loadOwnerName();
        } catch (error) {
          console.error("Ошибка при загрузке проекта:", error.response?.data || error);
        }
      },
      /**
       * Загружает имя владельца идеи и записывает его в свойства идеи.
       */
      async loadOwnerName() {
        if (!this.idea.owner) {
          console.warn("ID владельца отсутствует! Установка значения по умолчанию.");
          this.idea.initiator = "Неизвестный автор";
          return;
        }
        console.log("ID владельца проекта:", this.idea.owner);
        try {
          await fetchOwnerName(this.idea, this.idea.owner);
        } catch (error) {
          console.error("Ошибка при загрузке имени владельца:", error);
          this.idea.initiator = "Неизвестный автор";
        }
      },
      /**
       * Обновляет лайк для идеи, используя утилиту toggleLike.
       *
       * @param {Event} event - Событие, например, click.
       */
      async updateLike(event) {
        try {
          await toggleLike(
            this.idea,
            event,
            this.liked,
            (state) => (this.isAnimating = state),
            () => this.currentUser.id
          );
        } catch (error) {
          console.error("Ошибка при обновлении лайка:", error);
        }
      },
      /**
       * Переходит на предыдущую страницу.
       */
      goBack() {
        this.$router.go(-1);
      },
    },
  };
  </script>
  
  <style scoped>@keyframes likeJump {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.4);
    }
    100% {
      transform: scale(1);
    }
  }
  
  .animate-like {
    animation: likeJump 0.3s ease-in-out;
  }</style>