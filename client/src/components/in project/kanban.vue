<template>
  <div>
    <Header />

    <div class="flex-1 overflow-auto custom-scrollbar-horizontal">
      <!-- Компактная кнопка для раскрытия панели -->
      <div class="fixed left-0 top-1/2 transform -translate-y-1/2 z-50 group">
        <div
          class="w-10 h-10 flex items-center justify-center rounded-r-md bg-indigo-600 hover:bg-indigo-700 cursor-pointer transition-colors shadow-md"
        >
          <svg
            class="w-5 h-5 text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 16 12"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M1 1h14M1 6h14M1 11h7"
            />
          </svg>
        </div>

        <!-- Раскрывающаяся панель -->
        <aside
          class="absolute left-10 top-0 w-56 bg-white dark:bg-gray-800 rounded-r-md shadow-xl transform -translate-x-full opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all duration-200 border border-gray-200 dark:border-gray-700"
          aria-label="Sidebar"
        >
          <div class="px-2 py-2">
            <ul class="space-y-1">
              <li>
                <a
                  href="#"
                  @click.prevent="showStatsModal = true"
                  class="flex items-center p-2 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-100 dark:hover:bg-gray-700 group text-sm"
                >
                  <svg
                    class="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 22 21"
                  >
                    <path
                      d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z"
                    />
                    <path
                      d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z"
                    />
                  </svg>
                  <span class="ml-2">Статистика</span>
                </a>
              </li>
              <li>
                <a
                  href="#"
                  class="flex items-center p-2 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-100 dark:hover:bg-gray-700 group text-sm"
                >
                  <svg
                    class="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 18 18"
                  >
                    <path
                      d="M6.143 0H1.857A1.857 1.857 0 0 0 0 1.857v4.286C0 7.169.831 8 1.857 8h4.286A1.857 1.857 0 0 0 8 6.143V1.857A1.857 1.857 0 0 0 6.143 0Zm10 0h-4.286A1.857 1.857 0 0 0 10 1.857v4.286C10 7.169 10.831 8 11.857 8h4.286A1.857 1.857 0 0 0 18 6.143V1.857A1.857 1.857 0 0 0 16.143 0Zm-10 10H1.857A1.857 1.857 0 0 0 0 11.857v4.286C0 17.169.831 18 1.857 18h4.286A1.857 1.857 0 0 0 8 16.143v-4.286A1.857 1.857 0 0 0 6.143 10Zm10 0h-4.286A1.857 1.857 0 0 0 10 11.857v4.286c0 1.026.831 1.857 1.857 1.857h4.286A1.857 1.857 0 0 0 18 16.143v-4.286A1.857 1.857 0 0 0 16.143 10Z"
                    />
                  </svg>
                  <span class="ml-2">Kanban-доска</span>
                </a>
              </li>
              <li>
                <a
                  href="#"
                  class="flex items-center p-2 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-100 dark:hover:bg-gray-700 group text-sm"
                >
                  <svg
                    class="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      d="m17.418 3.623-.018-.008a6.713 6.713 0 0 0-2.4-.569V2h1a1 1 0 1 0 0-2h-2a1 1 0 0 0-1 1v2H9.89A6.977 6.977 0 0 1 12 8v5h-2V8A5 5 0 1 0 0 8v6a1 1 0 0 0 1 1h8v4a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-4h6a1 1 0 0 0 1-1V8a5 5 0 0 0-2.582-4.377ZM6 12H4a1 1 0 0 1 0-2h2a1 1 0 0 1 0 2Z"
                    />
                  </svg>
                  <span class="ml-2">Информация о проекте</span>
                </a>
              </li>
              <li>
                <a
                  href="#"
                  class="flex items-center p-2 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-100 dark:hover:bg-gray-700 group text-sm"
                >
                  <svg
                    class="w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 20 18"
                  >
                    <path
                      d="M14 2a3.963 3.963 0 0 0-1.4.267 6.439 6.439 0 0 1-1.331 6.638A4 4 0 1 0 14 2Zm1 9h-1.264A6.957 6.957 0 0 1 15 15v2a2.97 2.97 0 0 1-.184 1H19a1 1 0 0 0 1-1v-1a5.006 5.006 0 0 0-5-5ZM6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Z"
                    />
                  </svg>
                  <span class="ml-2">Команда</span>
                </a>
              </li>
            </ul>
          </div>
        </aside>
      </div>

      <div class="h-full overflow-hidden p-3 pt-16 w-4/5 m-auto">
        <h1 class="text-white text-7xl">Kanban-доска</h1>
        <!-- Описание канбан-доски -->
        <div class="">
          <p class="text-white text-2xl mt-4">
            Это канбан-доска для планирования и работы над проектными задачами.
            Вы можете создавать колонки, перемещать карточки и организовывать
            спринты.
          </p>
        </div>

        <!-- Кнопка добавления новой колонки -->
        <div class="mb-4 flex justify-end">
          <button
            v-if="!showAddColumnForm"
            @click="showAddColumnForm = true"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors flex items-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2"
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
            Добавить колонку
          </button>

          <!-- Форма добавления новой колонки -->
          <div
            v-else
            class="p-3 bg-white dark:bg-gray-700 rounded-md shadow mb-4"
          >
            <input
              v-model="newColumnTitle"
              @keyup.enter="addColumn"
              placeholder="Введите название колонки"
              class="w-full px-3 py-2 mb-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-600"
              v-focus
            />
            <div class="flex space-x-2">
              <button
                @click="addColumn"
                class="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
              >
                Добавить
              </button>
              <button
                @click="showAddColumnForm = false"
                class="px-3 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>

        <!-- Горизонтально прокручиваемая область колонок -->
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
            >
              <template #item="{ element }">
                <div
                  class="flex-shrink-0 pb-3 flex flex-col w-80 bg-white dark:bg-gray-700 rounded-md shadow"
                  :style="{ height: 'auto' }"
                >
                  <!-- Заголовок колонки с редактированием -->
                  <div
                    class="flex justify-between items-center p-2 border-b border-gray-200 dark:border-gray-600"
                  >
                    <input
                      v-if="element.editing"
                      v-model="element.title"
                      @blur="saveColumnTitle(element)"
                      @keyup.enter="saveColumnTitle(element)"
                      class="w-full px-2 py-1 text-lg font-semibold bg-white dark:bg-gray-600 rounded border border-gray-300 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      v-focus
                    />
                    <h3
                      v-else
                      class="px-3 py-2 font-semibold text-gray-700 dark:text-gray-200 text-lg cursor-text"
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
                        @click="toggleDropdown(element.id)"
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
                        class="absolute right-0 mt-1 w-32 bg-white dark:bg-gray-600 rounded shadow-md py-1 z-10 border border-gray-200 dark:border-gray-500"
                      >
                        <button
                          @click="editColumnTitle(element)"
                          class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-gray-500"
                        >
                          Редактировать
                        </button>
                        <button
                          @click="toggleLockColumn(element)"
                          class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-gray-500"
                        >
                          {{ element.locked ? "Открепить" : "Закрепить" }}
                        </button>
                        <button
                          @click="archiveList(element.id)"
                          class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-gray-500"
                        >
                          Архивировать
                        </button>
                        <button
                          @click="deleteColumn(element.id)"
                          class="block w-full text-left px-3 py-1 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-500"
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
                    item-key="title"
                    class="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-3 pb-1 space-y-3"
                    animation="200"
                  >
                    <template #item="{ element: task }">
                      <div
                        class="block p-3 rounded-md bg-white dark:bg-gray-600 shadow cursor-pointer hover:shadow-md transition-shadow"
                        @click="openTaskModal(task, element)"
                      >
                        <div class="flex justify-between">
                          <p
                            class="text-sm font-medium text-gray-900 dark:text-gray-100 leading-snug"
                          >
                            {{ task.title }}
                          </p>
                          <img
                            class="h-6 w-6 object-cover rounded-full"
                            :src="task.avatar"
                          />
                        </div>
                        <div class="flex items-baseline justify-between mt-2">
                          <div class="text-sm text-gray-600 dark:text-gray-300">
                            <time :datetime="task.date">{{
                              task.displayDate
                            }}</time>
                          </div>
                          <span
                            class="px-2 py-1 inline-flex items-center bg-indigo-100 dark:bg-indigo-900 rounded text-xs font-medium text-indigo-800 dark:text-indigo-200"
                          >
                            <svg
                              class="h-2 w-2 text-indigo-500 dark:text-indigo-300 mr-2"
                              viewBox="0 0 8 8"
                              fill="currentColor"
                            >
                              <circle cx="4" cy="4" r="3" />
                            </svg>
                            {{ task.label }}
                          </span>
                        </div>
                        <div
                          v-if="task.description"
                          class="mt-2 text-xs text-gray-500 dark:text-gray-400 line-clamp-2"
                        >
                          {{ task.description }}
                        </div>
                      </div>
                    </template>
                  </draggable>

                  <!-- Кнопка добавления задачи -->
                  <div class="px-3 py-2">
                    <button
                      @click="showAddTaskModal(element.id)"
                      class="w-full flex items-center justify-center text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
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

      <!-- Модальное окно для добавления задачи -->
      <div
        v-if="showTaskModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
          <h3 class="text-lg font-semibold mb-4 dark:text-white">
            Добавить задачу
          </h3>

          <div class="space-y-4">
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Название</label
              >
              <input
                v-model="newTask.title"
                class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                placeholder="Введите название задачи"
              />
            </div>

            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Исполнитель</label
              >
              <select
                v-model="newTask.label"
                class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
              >
                <option value="Даша">Даша</option>
                <option value="Саша">Саша</option>
                <option value="Маша">Маша</option>
              </select>
            </div>

            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Дата</label
              >
              <input
                v-model="newTask.date"
                type="date"
                class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
              />
            </div>

            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Описание</label
              >
              <textarea
                v-model="newTask.description"
                class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                placeholder="Детальное описание задачи"
                rows="3"
              ></textarea>
            </div>
          </div>

          <div class="mt-6 flex justify-end space-x-3">
            <button
              @click="showTaskModal = false"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            >
              Отмена
            </button>
            <button
              @click="addTask"
              class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
            >
              Добавить
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно для редактирования задачи (справа) -->
      <div v-if="showEditModal" class="fixed inset-0 z-50 overflow-hidden">
        <div
          class="absolute inset-0 bg-black bg-opacity-50"
          @click="closeEditModal"
        ></div>
        <div class="absolute inset-y-0 right-0 max-w-full flex">
          <div class="relative w-screen max-w-md">
            <div
              class="h-full flex flex-col bg-white dark:bg-gray-800 shadow-xl"
            >
              <div class="flex-1 overflow-y-auto">
                <div class="p-6">
                  <div class="flex items-start justify-between">
                    <h2
                      class="text-lg font-medium text-gray-900 dark:text-white"
                    >
                      Редактирование задачи
                    </h2>
                    <button
                      type="button"
                      class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
                      @click="closeEditModal"
                    >
                      <span class="sr-only">Close</span>
                      <svg
                        class="h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </div>

                  <div class="mt-6 space-y-6">
                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                        >Название</label
                      >
                      <input
                        v-model="editingTask.title"
                        class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                      />
                    </div>

                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                        >Исполнитель</label
                      >
                      <select
                        v-model="editingTask.label"
                        class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                      >
                        <option value="Даша">Даша</option>
                        <option value="Саша">Саша</option>
                        <option value="Маша">Маша</option>
                      </select>
                    </div>

                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                        >Дата</label
                      >
                      <input
                        v-model="editingTask.date"
                        type="date"
                        class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                      />
                    </div>

                    <div>
                      <label
                        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                        >Описание</label
                      >
                      <textarea
                        v-model="editingTask.description"
                        class="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white dark:bg-gray-700"
                        rows="6"
                        placeholder="Детальное описание задачи..."
                      ></textarea>
                    </div>
                  </div>
                </div>
              </div>

              <div
                class="flex-shrink-0 px-4 py-4 flex justify-end border-t border-gray-200 dark:border-gray-700"
              >
                <button
                  type="button"
                  class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                  @click="closeEditModal"
                >
                  Отмена
                </button>
                <button
                  type="submit"
                  class="ml-4 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
                  @click="saveTaskChanges"
                >
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Модальное окно статистики команды -->
      <div
        v-if="showStatsModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold dark:text-white">
              Статистика команды
            </h3>
            <button
              @click="showStatsModal = false"
              class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <!-- Название команды -->
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Название команды</label
              >
              <div class="p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
                <p class="font-medium">Dream Team</p>
              </div>
            </div>

            <!-- Члены команды -->
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Участники команды</label
              >
              <div class="space-y-2">
                <div
                  v-for="(member, index) in teamMembers"
                  :key="index"
                  class="flex items-center p-3 bg-gray-100 dark:bg-gray-700 rounded-md"
                >
                  <img
                    :src="member.avatar"
                    class="w-8 h-8 rounded-full mr-3"
                    :alt="member.name"
                  />
                  <div>
                    <p class="font-medium">{{ member.name }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ member.role }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Тимлид -->
            <div>
              <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Тимлид</label
              >
              <div
                class="flex items-center p-3 bg-indigo-50 dark:bg-indigo-900 rounded-md"
              >
                <img
                  :src="teamLead.avatar"
                  class="w-8 h-8 rounded-full mr-3"
                  :alt="teamLead.name"
                />
                <div>
                  <p class="font-medium">{{ teamLead.name }}</p>
                  <p class="text-xs text-indigo-600 dark:text-indigo-300">
                    Team Lead
                  </p>
                </div>
              </div>
            </div>

            <!-- Оценка команды -->
            <div class="pt-4">
              <button
                @click="showRating = !showRating"
                class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
              >
                Поставить оценку
              </button>

              <div v-if="showRating" class="mt-4">
                <p
                  class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Оцените работу команды:
                </p>
                <div class="flex items-center space-x-1">
                  <button
                    v-for="star in 5"
                    :key="star"
                    @click="setRating(star)"
                    class="focus:outline-none"
                  >
                    <svg
                      :class="[
                        'h-8 w-8',
                        star <= currentRating
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300 dark:text-gray-500 fill-current',
                      ]"
                      viewBox="0 0 20 20"
                    >
                      <path
                        d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                      />
                    </svg>
                  </button>
                </div>
                <p
                  v-if="currentRating > 0"
                  class="mt-2 text-sm text-gray-600 dark:text-gray-400"
                >
                  Вы поставили: {{ currentRating }} звезд{{
                    currentRating > 1 ? "ы" : "а"
                  }}
                </p>
              </div>
            </div>
          </div>

          <div class="mt-6 flex justify-end">
            <button
              @click="showStatsModal = false"
              class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Header from "@/components/header.vue";

export default {
  name: "CompactBacklog",
  components: { draggable, Header },
  directives: {
    focus: {
      inserted(el) {
        el.focus();
      },
    },
  },
  data() {
    return {
      showStatsModal: false,
      showRating: false,
      currentRating: 0,
      teamMembers: [
        {
          name: "Даша",
          role: "Frontend разработчик",
          avatar:
            "https://images.unsplash.com/photo-1506755855567-92ff770e8d00?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
        },
        {
          name: "Саша",
          role: "Backend разработчик",
          avatar:
            "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
        },
        {
          name: "Маша",
          role: "Дизайнер",
          avatar:
            "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
        },
      ],
      teamLead: {
        name: "Алексей",
        role: "Team Lead",
        avatar:
          "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
      },
      dropdownOpen: {},
      showAddColumnForm: false,
      newColumnTitle: "",
      showTaskModal: false,
      showEditModal: false,
      currentColumnId: null,
      editingTask: null,
      newTask: {
        title: "",
        label: "Даша",
        date: new Date().toISOString().split("T")[0],
        description: "",
        avatar:
          "https://images.unsplash.com/photo-1506755855567-92ff770e8d00?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
      },
      columns: [
        {
          id: "backlog",
          title: "Backlog",
          editing: false,
          locked: false,
          tasks: [
            {
              title: "Работать сообща",
              avatar:
                "https://images.unsplash.com/photo-1506755855567-92ff770e8d00?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
              date: "2020-08-10",
              displayDate: "10 авг",
              label: "Даша",
              description: "Совместная работа над проектом с командой",
            },
          ],
        },
        {
          id: "in-progress",
          title: "In Progress",
          editing: false,
          locked: false,
          tasks: [
            {
              title: "Сделать красивый фронт",
              avatar:
                "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
              date: "2020-08-11",
              displayDate: "11 авг",
              label: "Даша",
              description: "Разработка пользовательского интерфейса",
            },
          ],
        },
      ],
    };
  },
  methods: {
    setRating(rating) {
      this.currentRating = rating;
      // Здесь можно добавить сохранение оценки (например, через API)
    },
    toggleDropdown(columnId) {
      this.dropdownOpen[columnId] = !this.dropdownOpen[columnId];
    },
    editColumnTitle(column) {
      column.editing = true;
      this.dropdownOpen[column.id] = false;
    },
    saveColumnTitle(column) {
      column.editing = false;
      if (!column.title.trim()) {
        column.title = "Без названия";
      }
    },
    toggleLockColumn(column) {
      column.locked = !column.locked;
      this.dropdownOpen[column.id] = false;
    },
    archiveList(columnId) {
      console.log(`Archive column ${columnId}`);
      this.dropdownOpen[columnId] = false;
    },
    deleteColumn(columnId) {
      this.columns = this.columns.filter((col) => col.id !== columnId);
      this.dropdownOpen[columnId] = false;
    },
    onMoveColumn(evt) {
      const { from, to } = evt;
      return !to || to.nodeName !== "DIV" || to.contains(from);
    },
    addColumn() {
      if (this.newColumnTitle.trim()) {
        const newId = "col-" + Date.now();
        this.columns.push({
          id: newId,
          title: this.newColumnTitle,
          editing: false,
          locked: false,
          tasks: [],
        });
        this.newColumnTitle = "";
        this.showAddColumnForm = false;
      }
    },
    showAddTaskModal(columnId) {
      this.currentColumnId = columnId;
      this.newTask = {
        title: "",
        label: "Даша",
        date: new Date().toISOString().split("T")[0],
        description: "",
        avatar:
          "https://images.unsplash.com/photo-1506755855567-92ff770e8d00?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80",
      };
      this.showTaskModal = true;
    },
    addTask() {
      if (this.newTask.title.trim()) {
        const column = this.columns.find(
          (col) => col.id === this.currentColumnId
        );
        if (column) {
          column.tasks.push({
            title: this.newTask.title,
            avatar: this.newTask.avatar,
            date: this.newTask.date,
            displayDate: this.formattedTaskDate,
            label: this.newTask.label,
            description: this.newTask.description,
          });
          this.showTaskModal = false;
        }
      }
    },
    openTaskModal(task, column) {
      this.editingTask = {
        ...task,
        originalTask: task,
        columnId: column.id,
      };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editingTask = null;
    },
    saveTaskChanges() {
      if (this.editingTask) {
        const column = this.columns.find(
          (col) => col.id === this.editingTask.columnId
        );
        if (column) {
          const task = column.tasks.find(
            (t) => t.title === this.editingTask.originalTask.title
          );
          if (task) {
            task.title = this.editingTask.title;
            task.label = this.editingTask.label;
            task.date = this.editingTask.date;
            task.description = this.editingTask.description;

            if (task.date) {
              const date = new Date(task.date);
              const options = { day: "numeric", month: "short" };
              task.displayDate = date.toLocaleDateString("ru-RU", options);
            }
          }
        }
        this.closeEditModal();
      }
    },
  },
  computed: {
    formattedTaskDate() {
      if (!this.newTask.date) return "";
      const date = new Date(this.newTask.date);
      const options = { day: "numeric", month: "short" };
      return date.toLocaleDateString("ru-RU", options);
    },
  },
};
</script>

<style scoped>
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
