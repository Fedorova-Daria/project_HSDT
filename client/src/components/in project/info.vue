<template>
    <div>
        <Header />
        <navbar :ideaId="ideaId"/>
        <div
      class="w-4/5 mt-5 m-auto p-6 overflow-auto flex gap-3 items-start z-10"
    >
        <div
        class="w-1/4 mt-5 bg-card rounded-lg p-6 flex flex-col"
        style="height: 300px"
      >
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

          <p class="text-gray-400">
            Дата создания:
            {{ new Date(idea.created_at).toLocaleDateString("ru-RU") }}
          </p>
        </div>

        <div class="mt-auto flex justify-between">
          <div class="flex justify-start gap-2">
            
          </div>

          <div class="mt-auto flex justify-end gap-5">
            <img
              v-if="isOwner"
              @click="toggleEditing"
              class="w-6 h-6 cursor-pointer"
              src="/pencil1.svg"
            />
            <button
              v-if="isEditing && isOwner"
              @click="saveAllChanges"
              class="w-6 h-6 cursor-pointer"
            >
              <svg
                width="23"
                height="23"
                viewBox="0 0 12 9"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M11.7 0.7C11.3134 0.3134 10.6866 0.313401 10.3 0.7L4.2 6.8L2.1 4.7C1.7134 4.3134 1.0866 4.3134 0.7 4.7V4.7C0.313401 5.0866 0.3134 5.7134 0.699999 6.1L2.78579 8.18579C3.56683 8.96683 4.83316 8.96683 5.61421 8.18579L11.7 2.1C12.0866 1.7134 12.0866 1.0866 11.7 0.7V0.7Z"
                  fill="white"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div
        class="w-3/4 mt-5 bg-card rounded-lg p-6 overflow-auto"
        style="height: auto; max-height: 100vh; overflow-y: auto"
      >
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
    </div>
</template>

<script>
import Header from "@/components/header.vue";
import navbar from "@/components/in project/navbar.vue";
import { fetchOwnerName } from "@/services/projects.js";
import Cookies from "js-cookie";
import api from "@/composables/auth.js";
export default {
  name: "info",
  components: { Header, navbar },
  props: {
    ideaId: {
      type: String,
      required: true
    }
},
    data() {
    return {
      errorModalVisible: false,
      errorModalMessage: "",
      idea: {},
      editedIdea: {},
      isEditing: false,
    };
  },
  computed: {
    currentUser() {
      return JSON.parse(Cookies.get("userData") || "{}");
    },
    isOwner() {
      return this.idea.owner?.id === this.currentUser?.id;
    },
    hasEditAccess() {
      return this.isOwner;
    },
  },
  watch: {
    ideaId: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchIdeaDetails(newId);
        }
      },
    },
  },
  methods: {
    toggleEditing() {
      if (!this.hasEditAccess) {
        alert("У вас нет прав на редактирование этой идеи!");
        return;
      }
      this.isEditing = !this.isEditing;
      if (this.isEditing) {
        this.prepareEditedIdea();
      }
    },
    prepareEditedIdea() {
      const { name, description, technologies, is_hiring, status } = this.idea;
      this.editedIdea = {
        name,
        description,
        technologies: [...(technologies || [])],
        is_hiring: is_hiring || false,
        status: status || "",
      };
    },
    async saveAllChanges() {
      try {
        if (!this.editedIdea.name || !this.editedIdea.description) {
          alert("Название и описание обязательны для заполнения.");
          return;
        }

        const payload = {
          name: this.editedIdea.name,
          description: this.editedIdea.description,
          technologies: this.editedIdea.technologies,
          is_hiring: this.editedIdea.is_hiring,
          status: this.editedIdea.status || null,
        };

        const response = await api.patch(
          `/projects/${this.idea.id}/edit/`,
          payload
        );
        console.log("Изменения сохранены:", response.data);
        this.fetchIdeaDetails(this.idea.id);
        this.isEditing = false;
      } catch (error) {
        console.error(
          "Ошибка при сохранении изменений:",
          error.response?.data || error
        );
      }
    },
    async fetchIdeaDetails(id) {
      try {
        const response = await api.get(`/projects/${id}/`);
        this.idea = response.data;
        console.log("Данные проекта:", this.idea);

        if (!this.idea.owner) {
          console.warn(
            "Поле owner отсутствует в данных проекта! Проверить API."
          );
          this.idea.initiator = "Неизвестный автор";
        } else {
          await this.loadOwnerName();
        }
      } catch (error) {
        console.error(
          "Ошибка при загрузке проекта:",
          error.response?.data || error
        );
      }
    },
    async loadOwnerName() {
      const ownerId = this.idea.owner?.id;
      if (!ownerId) {
        console.warn("ID владельца отсутствует!");
        this.idea.initiator = "Неизвестный автор";
        return;
      }
      try {
        await fetchOwnerName(this.idea, ownerId);
      } catch (error) {
        console.error("Ошибка при загрузке имени владельца:", error);
        this.idea.initiator = "Неизвестный автор";
      }
    },
  },
};
</script>

