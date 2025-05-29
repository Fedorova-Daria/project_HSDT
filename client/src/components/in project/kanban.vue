<template>
  <div>
    <Header />

    <div class="flex-1 overflow-auto custom-scrollbar-horizontal">

      <navbar v-if="ideaId" :ideaId="ideaId"/>
      <div class="h-full overflow-hidden p-3 pt-16 w-4/5 m-auto">
        <!-- Описание канбан-доски -->
        <div class="">
          <p class="text-2xl mt-4">
            Это канбан-доска для планирования и работы над проектными задачами.
            Вы можете создавать колонки, перемещать карточки и организовывать
            спринты.
          </p>
        </div>

        <!-- Кнопка добавления новой колонки -->
        <div class="mb-4 flex justify-end relative" ref="dropdownWrapper">
          <button
            @click="toggleDropdownn"
            class="text-always-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">Добавить колонку <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
            </svg>
          </button>

          <!-- Форма добавления новой колонки -->
          <div v-if="showDropdown"
          ref="dropdownButton"
            class="z-10 bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 absolute top-full mr-1.5">
              <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownDefaultButton">
                <li>
                  <a  @click="prepareColumn('default')" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Добавить обычную</a>
                </li>
                <li>
                  <a  @click="prepareColumn('completed')" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Добавить финальную</a>
                </li>
                <li>
                </li>
              </ul>
          </div>
          <div v-if="creatingColumn" class="absolute top-full right-0 mt-14 w-64">
    <input
      v-model="newColumnTitle"
      @keyup.enter="createColumn"
      @blur="cancelCreatingColumn"
      placeholder="Введите название колонки"
      class="w-full px-3 py-2 border rounded shadow-sm focus:outline-none focus:ring text-white bg-zinc-700"
      autofocus
    />
  </div>
        </div>


        <div class="overflow-x-auto pb-4">
    <div class="inline-flex space-x-3">
      <!-- Перетаскиваемые колонки -->
      <draggable
        v-model="columns"
        group="columns"
        item-key="id"
        class="flex space-x-3"
        animation="200"
        :move="onMoveColumn"
        @end="onDragEndColumn(boardId)"
      >
        <template #item="{ element }">
          <div
            class="flex-shrink-0 pb-3 flex flex-col w-80 bg-card rounded-md shadow"
            :style="{ height: '600px' }"
          >
            <!-- Заголовок колонки с редактированием -->
            <div
              class="flex justify-between items-center p-2 border-b border-gray-200 dark:border-zinc-600"
            >
              <input
                v-if="element.editing"
                v-model="element.title"
                @blur="saveColumnTitle(element)"
                @keyup.enter="saveColumnTitle(element)"
                class="w-full px-2 py-1 text-lg font-semibold bg-white dark:bg-zinc-600 rounded border border-gray-300 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                v-focus
              />
              <h3
                v-else
                class="px-3 py-2 font-semibold text-lg cursor-text"
                @dblclick="editColumnTitle(element)"
              >
                {{ element.title }}
                <span v-if="element.locked" class="ml-1 text-indigo-500">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 inline"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </span>
              </h3>
              <div class="relative">
                <button
                  @click.stop="toggleDropdown(element.id)"
                  class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none p-1"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                    />
                  </svg>
                </button>
                <!-- Выпадающее меню -->
                <div
                  v-if="dropdownOpen[element.id]"
                  :ref="'dropdown_' + element.id"
                  class="absolute right-0 mt-1 w-32 bg-input rounded shadow-md py-1 z-10 border border-gray-200 dark:border-gray-500"
                >
                  <button
                    @click="editColumnTitle(element)"
                    class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-gray-500"
                  >
                    Редактировать
                  </button>
                  <button
                    @click="deleteColumn(element.id)"
                    class="block w-full text-left px-3 py-1 text-sm text-red hover:bg-gray-100 dark:hover:bg-gray-500"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </div>
            

            <!-- Задачи внутри колонки -->
            <draggable
              v-model="element.tasks"
              :group="{
                name: 'tasks',
                pull: element.locked ? false : true,
                put: true,
              }"
              item-key="id"
              class="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-3 pb-1 space-y-3"
              animation="200"
              @end="onDragEnd"
              :data-column-id="element.id" 
            >
              <template #item="{ element: task }">
                <div
                  class="block p-3 rounded-md bg-card shadow-lg cursor-pointer hover:shadow-ml transition-shadow mt-2"
                  @click="openModal(task)"
                >
        
                  <!-- Редактируемый заголовок задачи -->
                  <div v-if="task.editing">
                    <textarea
                      v-model="task.title"
                      @blur="saveTask(task)"
                      @input="adjustTextAreaHeight"
                      @keydown.enter="saveTask(task)"
                      class="w-full p-1 border rounded resize-none"
                      rows="1"
                      autofocus
                    />
                  </div>

                  <!-- Если не в режиме редактирования, отображаем обычный заголовок -->
                  <div v-else @dblclick="editTask(task)" class="flex justify-between">
                    <p
                    class="text-sm font-medium leading-snug "
                    :style="{ width: '225px' }"
                    :class="{ 'line-through ': task.column_type === 'completed' }"
                  >
                    {{ task.title }}
                  </p>

                    <!-- Кнопка для выпадающего меню -->
                    <div class="relative">
                      <button
                        @click.stop="toggleDropdownTask(task.id)"
                        class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none p-1"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="h-5 w-5"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                        >
                          <path
                            d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                          />
                        </svg>
                      </button>

                      <!-- Выпадающее меню -->
                      <div
                        v-if="showDropdownTask === task.id"
                        :ref="'dropdown_' + task.id"
                        class="absolute right-0 mt-1 w-32 bg-white dark:bg-gray-600 rounded shadow-md py-1 z-10 border border-gray-200 dark:border-gray-500"
                      >
                        <button
                          @click="editTaskTitle(task.id)"
                          class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-gray-500"
                        >
                          Редактировать
                        </button>
                        <button
                          @click="deleteTask(task.id)"
                          class="block w-full text-left px-3 py-1 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-500"
                        >
                          Удалить
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Остальная информация о задаче -->
                  <div class="flex items-baseline justify-end mt-2">
                    <span
                      class="px-2 py-1 inline-flex items-center bg-indigo-100 dark:bg-indigo-900 rounded text-xs font-medium text-indigo-800 dark:text-indigo-200"
                    >
                      <svg class="h-2 w-2 text-indigo-500 dark:text-indigo-300 mr-2" viewBox="0 0 8 8" fill="currentColor">
                        <circle cx="4" cy="4" r="3" />
                      </svg>
                      {{ getMemberFullName(task.assigned_to) }}
                    </span>
                  </div>
                </div>
              </template>
            </draggable>

            <!-- Модальное окно -->
    <transition name="slide">
      <div v-if="localTask" class="fixed right-0 top-0 h-full w-200 bg-card shadow-lg z-50 p-6 overflow-y-auto">
        <!-- Заголовок -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            <input
              v-model="localTask.title"
              class="w-170 px-2 py-1 text-lg font-semibold bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
            />
          </h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
            ✖
          </button>
        </div>

        <!-- Описание задачи -->
        <textarea
          v-model="localTask.message"
          class="w-[700px] h-[650px] resize-none bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
          placeholder="Введите описание задачи..."
        ></textarea>

        <!-- Выбор исполнителя -->
        <div class="mt-4">
          <label class="block font-medium mb-2">Назначить исполнителя:</label>
          <select v-model="localTask.assigned_to" class="w-full border bg-input bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none">
            <option v-for="member in teamMembers" :key="member.id" :value="member.id">
              {{ member.full_name }}
            </option>
          </select>
        </div>

        <!-- Кнопки -->
        <div class="flex justify-end space-x-3 mt-4">
          <button @click="saveTask(localTask)" class="px-4 py-2 bg-indigo-500 text-always-white rounded hover:bg-indigo-600">
            Сохранить
          </button>
          <button @click="closeModal" class="px-4 py-2 bg-gray-300 text-zinc-700 rounded hover:bg-gray-400">
            Закрыть
          </button>
        </div>
      </div>
    </transition>

            <!-- Кнопка добавления задачи -->
            <div class="px-3 py-2">
              <button
                class="w-full flex items-center justify-center text-zinc-200 hover:text-gray-700 dark:hover:text-zinc-300 p-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-600 transition-colors"
                @click="addTaskToColumn(element)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 mr-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                Добавить задачу
              </button>
            </div>
          </div>
        </template>
      </draggable>
    </div>
  </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Header from "@/components/header.vue";
import api from "@/composables/auth.js";  
import { nextTick } from "vue"; // Импортируем nextTick
import navbar from "@/components/in project/navbar.vue"

export default {
  name: "Kanban",
  components: { draggable, Header, navbar },
  props: {
    ideaId: {
      type: String,
      required: true
    },
    institute: {
      type: String,
      required: true
    }
  },
  directives: {
    focus: {
      inserted(el) {
        el.focus();
      },
    },
  },
  data() {
    return {
      localTask: null, // Локальная копия задачи
      selectedTask: null, // Хранит выбранную задачу
      teamMembers: [], // Список участников команды
      teamId: null,
      creatingColumn: false,
      newColumnTitle: '',
      newColumnType: '', // default или completed
      showDropdownTask: null,
      columns: [],
      showDropdown: false,
      dropdownOpen: {},
      showTaskModal: false,
      editingTask: null, // Для отслеживания редактируемой задачи
    };
  },
  mounted() {
    this.fetchBoardData();
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    async deleteColumn(columnId) {
    // Найти индекс колонки
    const columnIndex = this.columns.findIndex(col => col.id === columnId);
    if (columnIndex === -1) return;

    // Сохранить колонку перед удалением (на случай ошибки)
    const deletedColumn = this.columns[columnIndex];

    // Удалить колонку из UI
    this.columns.splice(columnIndex, 1);

    try {
      await api.delete(`/kanban/columns/${columnId}/`);
      console.log("✅ Колонка удалена:", columnId);
    } catch (error) {
      console.error("❌ Ошибка при удалении колонки:", error);
      // Вернуть колонку обратно в UI, если запрос не удался
      this.columns.splice(columnIndex, 0, deletedColumn);
    }
  },
    getMemberFullName(memberId) {
    const member = this.teamMembers.find((m) => m.id === memberId);
    return member ? member.full_name : "";
  },
    async fetchTeamMembers() {
      try {
        const response = await api.get(`/teams/${this.teamId}`);
        this.teamMembers = response.data.members; // Загружаем список участников
      } catch (error) {
        console.error("❌ Ошибка при загрузке участников команды:", error);
      }
    },
    openModal(task) {
    if (task.editing) {
      console.log("🟢 Заголовок редактируется, модальное окно не открываем.");
      return;
    }
    this.localTask = { ...task }; // Создаем копию задачи
  },
    async saveTask(task) {
      try {
        await api.patch(`/kanban/tasks/${task.id}/`, {
          title: task.title,
          message: task.message,
          assigned_to: task.assigned_to,
        });
        task.editing = false;
        console.log("✅ Задача обновлена:", task);

        // Обновляем задачу в списке
        const column = this.columns.find((col) => col.tasks.some((t) => t.id === task.id));
        if (column) {
          const taskIndex = column.tasks.findIndex((t) => t.id === task.id);
          column.tasks[taskIndex] = task;
        }

        this.closeModal();
      } catch (error) {
        console.error("❌ Ошибка при обновлении задачи:", error);
      }
    },
    closeModal() {
      this.localTask = null; // Закрываем модальное окно
    },
    toggleDropdownn() {
      this.showDropdown = !this.showDropdown;
      this.creatingColumn = false;
    },
    toggleDropdown(id) {
    // Закрываем все, открываем только текущий
    this.dropdownOpen = { [id]: !this.dropdownOpen[id] };
  },
    toggleDropdownTask(taskId) {
      this.showDropdownTask = this.showDropdownTask === taskId ? null : taskId;
    },
    
    async fetchBoardData() {
  try {
    const response = await api.get("/kanban/boards/3/");
    console.log("✅ Response from /kanban/boards/:", response.data);
    this.columns = response.data.columns;
    this.boardId = response.data.id; // сохраняем ID доски
    this.teamId = response.data.team;

    // Добавляем column_type в каждую задачу
    this.columns.forEach(column => {
        column.tasks.forEach(task => {
          task.column_type = column.column_type; // Добавляем тип колонки в задачу
        });
      });
  
    await this.fetchTeamMembers();
  } catch (error) {
    console.error("❌ Error fetching board data:", error);
    console.log("Full error:", error.response);
  }
},
prepareColumn(type) {
    this.newColumnType = type;
    this.creatingColumn = true;
    this.showDropdown = false;
    this.$nextTick(() => {
      // Автофокус на input
      const input = this.$el.querySelector('input[autofocus]');
      if (input) input.focus();
    });
  },
  async createColumn() {
  if (!this.newColumnTitle.trim()) return;

  const newOrder = this.columns.length;

  const data = {
    title: this.newColumnTitle,
    column_type: this.newColumnType,
    order: newOrder,
    board: this.boardId,
  };

  try {
    const response = await api.post('/kanban/columns/', data);
    this.columns.push(response.data); // добавляем в список
    this.newColumnTitle = '';
    this.creatingColumn = false;
  } catch (error) {
    console.error("❌ Ошибка при создании колонки:", error);
  }
},
  cancelCreatingColumn() {
    this.creatingColumn = false;
  },
    onMoveColumn(evt) {
      const { from, to } = evt;
      return !to || to.nodeName !== "DIV" || to.contains(from);
    },
    editTask(task) {
    task.editing = true;
    this.editingTask = task;  // Сохраняем редактируемую задачу
  },
  async addTaskToColumn(column) {
  try {
    const maxOrder = column.tasks.length > 0
      ? Math.max(...column.tasks.map(task => task.order))
      : -1;
    const nextOrder = maxOrder + 1;

    const response = await api.post("/kanban/tasks/", {
      title: "Новая задача",
      message: "",
      order: nextOrder,
      column: column.id,
      assigned_to: null
    });

    const newTask = {
      ...response.data,
      editing: true // для режима редактирования
    };

    // Добавляем в конец массива тасков
    column.tasks.push(newTask);
  } catch (error) {
    console.error("Ошибка при создании задачи", error);
  }
},

async onDragEnd(event) {
  await nextTick();

  // Проверяем структуру event
  console.log("Drag event:", event);

  // Получаем задачу, которая была перемещена
  const task = event.item.__draggable_context.element; // Новый способ получения задачи
  if (!task) {
    console.error("❌ Ошибка: не удалось получить задачу из события.");
    return;
  }

  // Получаем ID новой колонки
  const newColumnId = event.to.getAttribute("data-column-id"); // Получаем ID из атрибута
  if (!newColumnId) {
    console.error("❌ Ошибка: не удалось определить новую колонку.");
    return;
  }

  // Получаем новую колонку
  const newColumn = this.columns.find((col) => col.id == newColumnId);
  if (!newColumn) {
    console.error("❌ Ошибка: колонка не найдена.");
    return;
  }

  // Обновляем тип колонки внутри задачи
  task.column_type = newColumn.column_type; // UI обновляется мгновенно

  // Обновляем порядок задач в новой колонке
  const updatedTasks = newColumn.tasks.map((task, index) => ({
    id: task.id,
    order: index,
    columnId: newColumnId,
    title: task.title,
    label: task.label,
    assigned_to: task.assigned_to || null,
  }));

  console.log("Обновленные задачи:", updatedTasks);

  try {
    await Promise.all(
      updatedTasks.map(async (task) => {
        try {
          await api.post(`/kanban/tasks/${task.id}/reorder/`, {
            order: task.order,
            column: task.columnId,
            title: task.title,
            label: task.label,
            assigned_to: task.assigned_to || null,
          });
          console.log(`✅ Задача ${task.id} обновлена.`);
        } catch (error) {
          console.error(`❌ Ошибка при обновлении задачи ${task.id}:`, error);
        }
      })
    );
  } catch (error) {
    console.error("❌ Ошибка при обновлении задач:", error);
  }
},
    async onDragEndColumn(boardId) {
  // Ждем обновления DOM
  await nextTick();

  // Используем this.columns вместо element
  const updatedColumns = this.columns.map((column, index) => ({
    order: index,
    title: column.title,
    board: boardId,
    id: column.id,
    column_type: column.column_type,
  }));

  console.log("Измененные колонки:", updatedColumns);

  try {
    await Promise.all(
      updatedColumns.map(async (column) => {
        try {
          await api.post(`/kanban/columns/${column.id}/reorder/`, {
            order: column.order,
            title: column.title,
            board: column.board,
            column_type: column.column_type,
          });
          console.log(`✅ Колонка ${column.id} обновлена.`);
        } catch (error) {
          console.error(`❌ Ошибка при обновлении колонки ${column.id}:`, error);
        }
      })
    );
  } catch (error) {
    console.error("❌ Ошибка при обновлении колонок:", error);
  }
},
async deleteTask(taskId) {
    // Найти колонку, содержащую задачу
    const column = this.columns.find(col => col.tasks.some(task => task.id === taskId));
    if (!column) return;

    // Найти индекс задачи
    const taskIndex = column.tasks.findIndex(task => task.id === taskId);
    if (taskIndex === -1) return;

    // Сохранить задачу перед удалением (на случай ошибки)
    const deletedTask = column.tasks[taskIndex];

    // Удалить задачу из UI
    column.tasks.splice(taskIndex, 1);

    try {
      await api.delete(`/kanban/tasks/${taskId}/`);
      console.log("✅ Задача удалена:", taskId);
    } catch (error) {
      console.error("❌ Ошибка при удалении задачи:", error);
      // Вернуть задачу обратно в UI, если запрос не удался
      column.tasks.splice(taskIndex, 0, deletedTask);
    }
  },
  // Изменяем высоту textarea
  adjustTextAreaHeight(event) {
    const textarea = event.target;
    textarea.style.height = 'auto'; // сбрасываем высоту
    textarea.style.height = `${textarea.scrollHeight}px`; // устанавливаем новую высоту
  },
  // Обработка клика вне задачи, чтобы не создавалась новая задача
  handleClickOutside(event) {
  if (this.showDropdownTask !== null) {
    const refName = 'dropdown_' + this.showDropdownTask;
    const dropdown = this.$refs[refName];
    const button = this.$refs.dropdownButton;

    // иногда $refs возвращает массив, особенно с v-for
    const dropdownEl = Array.isArray(dropdown) ? dropdown[0] : dropdown;

    if (dropdownEl && !dropdownEl.contains(event.target)) {
      this.showDropdownTask = null;
    }
    if (dropdown && !dropdown.contains(event.target) && button && !button.contains(event.target)) {
      this.showDropdown  = false; // Закрываем меню
    }
  }
},
handleClickOutside(event) {
      const dropdown = this.$refs.dropdownWrapper;
      if (dropdown && !dropdown.contains(event.target)) {
        this.showDropdown = false;
      }
    },
  cancelCreation() {
    // Логика для отмены создания задачи
    if (this.editingTask) {
      this.editingTask.editing = false;
      this.editingTask = null;
    }
  },
  },
};
</script>

<style scoped>
.text-red{
  color: red !important;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
.custom-scrollbar-horizontal::-webkit-scrollbar {
  height: 6px;
}
.custom-scrollbar-horizontal::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}
.custom-scrollbar-horizontal::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.custom-scrollbar-horizontal::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
