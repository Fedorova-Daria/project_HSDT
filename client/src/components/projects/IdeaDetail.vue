<template>
      <div>
    <Header />
    <div
      class="w-4/5 mt-5 m-auto p-6 overflow-auto flex gap-3 items-start z-10"
    >
      <button
        @click="goBack"
        :style="{ backgroundColor: currentBgColor }"
        class="ml-auto font-medium rounded-lg text-sm px-4 py-2 mt-5 duration-300 h-10 w-14 items-center"
      >
        <svg
          width="13"
          height="13"
          viewBox="0 0 17 13"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M5.27934 8.23871C5.35303 8.30737 5.41213 8.39017 5.45312 8.48217C5.49411 8.57417 5.51616 8.67348 5.51793 8.77418C5.51971 8.87489 5.50118 8.97492 5.46346 9.0683C5.42574 9.16169 5.3696 9.24653 5.29838 9.31774C5.22716 9.38896 5.14233 9.44511 5.04894 9.48283C4.95555 9.52055 4.85552 9.53907 4.75482 9.5373C4.65412 9.53552 4.5548 9.51348 4.4628 9.47249C4.3708 9.4315 4.288 9.37239 4.21934 9.29871L0.21934 5.29871C0.0788892 5.15808 -1.99759e-07 4.96746 -2.08447e-07 4.76871C-2.17135e-07 4.56996 0.0788892 4.37933 0.21934 4.23871L4.21934 0.238705C4.288 0.165019 4.3708 0.105917 4.4628 0.064925C4.5548 0.023933 4.65411 0.00189198 4.75482 0.000115187C4.85552 -0.0016616 4.95555 0.0168623 5.04894 0.0545833C5.14233 0.0923043 5.22716 0.148449 5.29838 0.219668C5.3696 0.290887 5.42574 0.375721 5.46346 0.469109C5.50118 0.562497 5.51971 0.662525 5.51793 0.763228C5.51615 0.863931 5.49411 0.963245 5.45312 1.05524C5.41213 1.14724 5.35303 1.23004 5.27934 1.29871L2.55934 4.01871L12.2493 4.01871C12.4483 4.01871 12.639 4.09772 12.7797 4.23838C12.9203 4.37903 12.9993 4.56979 12.9993 4.76871C12.9993 4.96762 12.9203 5.15838 12.7797 5.29904C12.639 5.43969 12.4483 5.51871 12.2493 5.51871L2.55934 5.51871L5.27934 8.23871Z"
            fill="white"
          />
        </svg>
      </button>

      <div
        class="w-1/4 mt-5 bg-card rounded-lg p-6 flex flex-col"
        style="height: 300px"
      >
        <div class="flex-grow overflow-auto">
          <h2 v-if="!isEditing" class="text-2xl font-semibold mb-4 ">
            {{ idea.title || "Загрузка..." }}
          </h2>
          <input
            v-else
            v-model="editedIdea.title"
            class="w-full text-2xl bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
          />

          <h3 class="text-xl font-semibold mb-2">
            Инициатор: {{ idea.initiator || "Неизвестный автор" }}
          </h3>

          <p class="opacity-70">
            Дата создания:
            {{ new Date(idea.created_at).toLocaleDateString("ru-RU") }}
          </p>
        </div>

        <div class="mt-auto flex justify-between">
          <div class="flex items-center justify-start gap-2">
  <span class="likes-count text-dynamic select-none">
    {{ idea.likes ? idea.likes.length.toLocaleString() : 0 }}
  </span>
  <div
    class="heart-container cursor-pointer"
    :style="{ '--heart-color': instituteStyle.likeColor }"
    title="Like"
    @click.stop="updateLike($event, idea)"
  >
    <input
      type="checkbox"
      class="checkbox"
      :id="'like-checkbox-' + idea.id"
      :checked="idea.likes?.includes(userId)"
      @change.stop
      style="display:none"
    />
    <div class="svg-container relative w-[30px] h-[30px]">
      <svg
        width="30" height="30"
        viewBox="0 0 24 24"
        class="svg-outline absolute top-0 left-0"
        xmlns="http://www.w3.org/2000/svg"
        v-show="!isLikedByUser(idea)"
        :stroke="instituteStyle.likeColor"
        fill="none"
        stroke-width="2"
      >
        <path
          d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
        />
      </svg>
      <svg
        width="30" height="30"
        viewBox="0 0 24 24"
        class="svg-filled absolute top-0 left-0"
        xmlns="http://www.w3.org/2000/svg"
        v-show="isLikedByUser(idea)"
        :style="{ fill: instituteStyle.likeColor }"
      >
        <path
          d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"
        />
      </svg>
    </div>
  </div>
</div>

          <div class="mt-auto flex justify-end gap-5">
            <img
              v-if="isOwner"
              @click="toggleEditing"
              class="w-7 h-7 cursor-pointer"
              :src="isDarkTheme ? '/pencil_light.svg' :'/pencil_dark.svg' "
            />
            <button
              v-if="isEditing && isOwner"
              @click="saveAllChanges"
              class="w-7 h-7 cursor-pointer"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 13 9"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M11.7 0.7C11.3134 0.3134 10.6866 0.313401 10.3 0.7L4.2 6.8L2.1 4.7C1.7134 4.3134 1.0866 4.3134 0.7 4.7V4.7C0.313401 5.0866 0.3134 5.7134 0.699999 6.1L2.78579 8.18579C3.56683 8.96683 4.83316 8.96683 5.61421 8.18579L11.7 2.1C12.0866 1.7134 12.0866 1.0866 11.7 0.7V0.7Z"
                  :fill="pathFillColor"
                />
              </svg>
            </button>
            <button
              v-if="isOwner"
              @click="showConfirmModal = true"
              class="h-6 w-6"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 14 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M5.5 1H8.5C8.63261 1 8.75979 1.05268 8.85355 1.14645C8.94732 1.24021 9 1.36739 9 1.5V2.5H5V1.5C5 1.36739 5.05268 1.24021 5.14645 1.14645C5.24021 1.05268 5.36739 1 5.5 1ZM10 2.5V1.5C10 1.10218 9.84196 0.720644 9.56066 0.43934C9.27936 0.158035 8.89782 0 8.5 0L5.5 0C5.10218 0 4.72064 0.158035 4.43934 0.43934C4.15804 0.720644 4 1.10218 4 1.5V2.5H0.5C0.367392 2.5 0.240215 2.55268 0.146447 2.64645C0.0526784 2.74021 0 2.86739 0 3C0 3.13261 0.0526784 3.25979 0.146447 3.35355C0.240215 3.44732 0.367392 3.5 0.5 3.5H1.038L1.891 14.16C1.93122 14.6612 2.15875 15.1289 2.52827 15.4698C2.8978 15.8108 3.38219 16.0001 3.885 16H10.115C10.6178 16.0001 11.1022 15.8108 11.4717 15.4698C11.8412 15.1289 12.0688 14.6612 12.109 14.16L12.962 3.5H13.5C13.6326 3.5 13.7598 3.44732 13.8536 3.35355C13.9473 3.25979 14 3.13261 14 3C14 2.86739 13.9473 2.74021 13.8536 2.64645C13.7598 2.55268 13.6326 2.5 13.5 2.5H10ZM11.958 3.5L11.112 14.08C11.0919 14.3306 10.9781 14.5644 10.7934 14.7349C10.6086 14.9054 10.3664 15.0001 10.115 15H3.885C3.6336 15.0001 3.3914 14.9054 3.20664 14.7349C3.02188 14.5644 2.90811 14.3306 2.888 14.08L2.042 3.5H11.958ZM4.471 4.5C4.60333 4.49235 4.73329 4.53756 4.8323 4.6257C4.93131 4.71383 4.99127 4.83767 4.999 4.97L5.499 13.47C5.50425 13.6008 5.45802 13.7284 5.37022 13.8255C5.28242 13.9225 5.16006 13.9813 5.02941 13.9892C4.89876 13.997 4.77024 13.9533 4.67144 13.8675C4.57265 13.7816 4.51145 13.6605 4.501 13.53L4 5.03C3.99594 4.96431 4.00489 4.89847 4.02633 4.83625C4.04777 4.77403 4.08129 4.71665 4.12495 4.66741C4.16862 4.61817 4.22158 4.57804 4.28079 4.54931C4.34 4.52058 4.4043 4.50382 4.47 4.5H4.471ZM9.529 4.5C9.5947 4.50382 9.659 4.52058 9.71821 4.54931C9.77742 4.57804 9.83038 4.61817 9.87405 4.66741C9.91771 4.71665 9.95123 4.77403 9.97267 4.83625C9.99411 4.89847 10.0031 4.96431 9.999 5.03L9.499 13.53C9.49633 13.5964 9.48043 13.6617 9.45224 13.7219C9.42405 13.7821 9.38413 13.8361 9.33481 13.8807C9.28549 13.9254 9.22777 13.9597 9.16503 13.9817C9.10228 14.0037 9.03578 14.013 8.9694 14.009C8.90302 14.005 8.8381 13.9878 8.77845 13.9585C8.7188 13.9291 8.6656 13.8881 8.62199 13.8379C8.57837 13.7877 8.5452 13.7293 8.52443 13.6661C8.50365 13.603 8.49569 13.5363 8.501 13.47L9.001 4.97C9.00873 4.83767 9.06869 4.71383 9.1677 4.6257C9.26671 4.53756 9.39667 4.49235 9.529 4.5ZM7 4.5C7.13261 4.5 7.25979 4.55268 7.35355 4.64645C7.44732 4.74021 7.5 4.86739 7.5 5V13.5C7.5 13.6326 7.44732 13.7598 7.35355 13.8536C7.25979 13.9473 7.13261 14 7 14C6.86739 14 6.74021 13.9473 6.64645 13.8536C6.55268 13.7598 6.5 13.6326 6.5 13.5V5C6.5 4.86739 6.55268 4.74021 6.64645 4.64645C6.74021 4.55268 6.86739 4.5 7 4.5Z"
                  :fill="pathFillColor"
                />
              </svg>
            </button>


            <!-- МОДАЛКА подтверждения удаления -->
            <teleport to="body">
            <div v-if="showConfirmModal" class="fixed inset-0 flex items-center justify-center bg-black z-100">
              <div class="bg-card p-6 rounded-xl shadow-xl w-80 text-center">
                <h2 class="text-lg font-semibold mb-3">Удалить проект?</h2>
                <p class="text-sm opacity-60 mb-6">Вы действительно хотите удалить этот проект? Это действие необратимо.</p>
                <div class="flex justify-center gap-4">
                  <button
                    @click="confirmDelete"
                    class=" text-red px-4 py-2 rounded font-semibold"
                  >
                    Да, удалить
                  </button>
                  <button
                    @click="showConfirmModal = false"
                    class="bg-gray-300 hover:bg-gray-400 text-always-black px-4 py-2 rounded font-semibold"
                  >
                    Отмена
                  </button>
                </div>
              </div>
            </div>
            </teleport>
          </div>
        </div>
      </div>
      <div
        class="w-3/4 mt-5 bg-card rounded-lg p-6 overflow-auto z-content"
        style="height: auto; max-height: 100vh; overflow-y: auto"
      >
        <h2 class="text-2xl font-semibold mb-4">Описание идеи</h2>
        <div v-if="isEditing">
          <label for="status" class="font-semibold mb-3">Изменить статус:</label>
          <select
            id="status"
            v-model="editedIdea.status"
            @change="updateStatus"
            class="w-full bg-input rounded-md p-2 mt-3 mb-3"
          >
            <option value="draft">Черновик</option>
            <option value="open">Открытый</option>
          </select>
        </div>
        <p v-if="!isEditing" class="opacity-70">
          {{ idea.description }}
        </p>
        <textarea
          v-else
          v-model="editedIdea.description"
          class="w-full bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
        ></textarea>
        
      </div>
    </div>

    <div class="w-4/5 m-auto flex flex-col gap-4">
<div class="w-4/5">
      <button
              @click="handleIdeaToProject"
              :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
              class="text-always-white ml-23 inline-flex items-center focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
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
  </div>
  </template>
  
  <script>
  import api from "@/composables/auth.js"; // axios-инстанс с интерсепторами
  import Header from "@/components/header.vue";
  import { getIdeaById, fetchOwnerName, toggleLike, deleteIdea } from "@/services/ideas.js";
  import { instituteStyles } from "@/assets/instituteStyles.js";

  export default {
    inject: ["globalState"],
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
        currentBgColor: "",
        idea: {}, // Загруженные данные идеи
        userId: JSON.parse(localStorage.getItem("userData") || "{}")?.id,
        showConfirmModal: false,
        userData: null,
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
      likeColor() {
    const inst = this.globalState.institute;
    const style = instituteStyles[inst];
    return style?.likeColor || "red"; // Цвет лайка по умолчанию красный
  },
  isDarkTheme() {
    if (!this.userData) return false;
    return this.userData.mode === 'dark';
  },
  pathFillColor() {
      return this.isDarkTheme ? "white" : "black";
    },
  isLikedByUser() {
    return (idea) => idea.likes?.includes(this.userId);
  },
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
      currentUser() {
        return JSON.parse(localStorage.getItem("userData") || "{}");
      },
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
      isOwner() {
        return this.idea.owner && this.idea.owner === this.currentUser.id;
      },
      hasEditAccess() {
        return this.isOwner;
      },
    },
    mounted() {
    this.currentBgColor = this.instituteStyle.buttonOffColor;
    this.fetchUserData();
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
      instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
    },
    methods: {
      async fetchUserData() {
      const response = await api.get('/users/me');
      this.userData = response.data;
      return response.data;
    },
  /**
   * Переносит идею из API `/ideas/` в проект через API `/projects/` и обновляет статус идеи.
   * @param {String} ideaId - ID идеи.
   * @param {String} customerId - ID кастомера.
   */
   async transferIdeaToProject(ideaId,) {
    try {
      // Шаг 1: Получаем данные идеи из API `/ideas/{ideaId}/`
      const ideaResponse = await api.get(`/ideas/${ideaId}/`);
      const ideaData = ideaResponse.data;

      // Формируем объект проекта
      const projectData = {
  title: ideaData.title || "Название проекта отсутствует",
  description: ideaData.description || "Нет описания",
  status: "under_review",
  owner: ideaData.owner,
  initiator: this.currentUser?.id || null,  // ✅ Используем `this.currentUser`
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
      const project = await this.transferIdeaToProject(this.ideaId);
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
          this.editedIdea.skills_required = [...(this.idea.skills_required || [])];
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
            ...(this.editedIdea.title && { title: this.editedIdea.title }),
            ...(this.editedIdea.description && { description: this.editedIdea.description }),
            ...(this.editedIdea.skills_required && { skills_required: this.editedIdea.skills_required }),
            status: this.editedIdea.status || null,
          };
          console.log("Payload перед отправкой:", payload);
  
          const response = await api.patch(`/ideas/${this.idea.id}/`, payload, {
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
     * Загружает данные идеи по её ID, используя метод из `ideas.js`
     */
    async fetchIdeaDetails(id) {
      try {
        const ideaData = await getIdeaById(id);
        this.idea = ideaData;
        console.log("Полученные данные идеи:", this.idea);

        if (!this.idea.owner) {
          console.warn("Поле owner отсутствует! Проверить API.");
          this.idea.initiator = "Неизвестный автор";
          return;
        }

        // Загружаем имя инициатора через метод `fetchOwnerName`
        await this.loadOwnerName();
      } catch (error) {
        console.error("Ошибка при загрузке идеи:", error.response?.data || error);
      }
    },

    /**
     * Загружает имя владельца идеи, используя метод `fetchOwnerName`
     */
    async loadOwnerName() {
      if (!this.idea.owner) {
        console.warn("ID владельца отсутствует! Установка значения по умолчанию.");
        this.idea.initiator = "Неизвестный автор";
        return;
      }

      console.log("ID владельца идеи:", this.idea.owner);
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
      async updateLike(event, idea) {
  try {
    event.stopPropagation();

    // Вызов сервиса лайка (он должен возвращать обновлённую идею с актуальными likes)
    const updatedIdea = await toggleLike(
      idea,
      event,
      idea.likes.includes(this.userId),
      (state) => (this.isAnimating = state),
      () => this.userId
    );

    // Обновим локальный стейт идеи (лайки обновятся)
    this.updateIdeaLikes(updatedIdea);

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
    confirmDelete() {
    this.handleDeleteIdea(this.ideaId); // вызываем удаление
    this.showConfirmModal = false; // закрываем модалку
  },
    async handleDeleteIdea(ideaId) {
  try {
    await deleteIdea(ideaId);
    this.$router.go(-1);
    this.$toast.success("Проект успешно удалён!");
  } catch (error) {
    console.error("Ошибка при удалении проекта:", error);
    this.$toast.error("Не удалось удалить проект. Попробуйте позже.");
  }
},
  };
  </script>
  
  <style scoped>
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}

.text-red{
  color: red !important;
}
.likes-count {
  display: inline-block;
  width: 4ch;      /* фиксированная ширина в символах — под размер числа */
  text-align: right; /* число прижато вправо */
  white-space: nowrap;
}
.svg-container, svg {
  overflow: visible;
  position: relative;
  width: 30px;  /* размер лайка */
  height: 30px;
}
/* From Uiverse.io by catraco */ 
.heart-container {
  --heart-color: var(--heart-color);
  position: relative;
  width: 30px;
  height: 30px;
  transition: .3s;
}

.heart-container .checkbox {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 20;
  cursor: pointer;
}

.heart-container .svg-celebrate {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;      /* чуть больше лайка, чтобы анимация была заметнее */
  height: 40px;
  transform: translate(-50%, -50%) scale(0); /* центрируем и начинаем с масштаба 0 */
  animation: keyframes-svg-celebrate .5s forwards;
  stroke: var(--heart-color);
  fill: var(--heart-color);
  stroke-width: 2px;
  pointer-events: none;
  display: none;
}

.heart-container .svg-outline,
        .heart-container .svg-filled {
  fill: var(--heart-color);
  position: absolute;
}

.heart-container .svg-filled {
  animation: keyframes-svg-filled 1s;
  display: none;
}

.heart-container .svg-celebrate {
  position: absolute;
  animation: keyframes-svg-celebrate .5s;
  animation-fill-mode: forwards;
  display: none;
  stroke: var(--heart-color);
  fill: var(--heart-color);
  stroke-width: 2px;
}

.heart-container .checkbox:checked~.svg-container .svg-filled {
  display: block
}

.heart-container .checkbox:checked~.svg-container .svg-celebrate {
  display: block
}

@keyframes keyframes-svg-filled {
  0% {
    transform: scale(0);
  }

  25% {
    transform: scale(1.2);
  }

  50% {
    transform: scale(1);
    filter: brightness(1.5);
  }
}

/* Обновленный keyframes с transform scale */

@keyframes keyframes-svg-celebrate {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }

  50% {
    opacity: 1;
    filter: brightness(1.5);
    transform: translate(-50%, -50%) scale(1.4);
  }

  100% {
    transform: translate(-50%, -50%) scale(1.4);
    opacity: 0;
    display: none;
  }
}
@keyframes likeJump {
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

.dark-filter {
  filter: invert(1);
}

.animate-like {
  animation: likeJump 0.3s ease-in-out;
}
.z-content {
  z-index: 1 !important;
}
</style>