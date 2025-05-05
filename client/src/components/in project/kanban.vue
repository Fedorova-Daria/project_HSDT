<template>
    <div>
        <Header/>

    <div class="flex-1 overflow-auto custom-scrollbar-horizontal">

      <aside id="separator-sidebar" class="fixed bottom-0 left-0 z-40 w-64 h-auto transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
   <div class="px-3 py-4 overflow-y-auto h-211 bg-gray-50 dark:bg-gray-800">
      <ul class="space-y-2 font-medium">
         <li>
            <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
               <svg class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 21">
                  <path d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z"/>
                  <path d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z"/>
               </svg>
               <span class="ms-3">Статистика</span>
            </a>
         </li>
         <li>
            <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
               <svg class="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M6.143 0H1.857A1.857 1.857 0 0 0 0 1.857v4.286C0 7.169.831 8 1.857 8h4.286A1.857 1.857 0 0 0 8 6.143V1.857A1.857 1.857 0 0 0 6.143 0Zm10 0h-4.286A1.857 1.857 0 0 0 10 1.857v4.286C10 7.169 10.831 8 11.857 8h4.286A1.857 1.857 0 0 0 18 6.143V1.857A1.857 1.857 0 0 0 16.143 0Zm-10 10H1.857A1.857 1.857 0 0 0 0 11.857v4.286C0 17.169.831 18 1.857 18h4.286A1.857 1.857 0 0 0 8 16.143v-4.286A1.857 1.857 0 0 0 6.143 10Zm10 0h-4.286A1.857 1.857 0 0 0 10 11.857v4.286c0 1.026.831 1.857 1.857 1.857h4.286A1.857 1.857 0 0 0 18 16.143v-4.286A1.857 1.857 0 0 0 16.143 10Z"/>
               </svg>
               <span class="flex-1 ms-3 whitespace-nowrap">Kanban-доска</span>
            </a>
         </li>
         <li>
            <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
              <svg class="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path d="m17.418 3.623-.018-.008a6.713 6.713 0 0 0-2.4-.569V2h1a1 1 0 1 0 0-2h-2a1 1 0 0 0-1 1v2H9.89A6.977 6.977 0 0 1 12 8v5h-2V8A5 5 0 1 0 0 8v6a1 1 0 0 0 1 1h8v4a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-4h6a1 1 0 0 0 1-1V8a5 5 0 0 0-2.582-4.377ZM6 12H4a1 1 0 0 1 0-2h2a1 1 0 0 1 0 2Z"/>
              </svg>
              <span class="flex-1 ms-3 whitespace-nowrap">Информация о проекте</span>
            </a>
        </li>
        <li>
            <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
              <svg class="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                  <path d="M14 2a3.963 3.963 0 0 0-1.4.267 6.439 6.439 0 0 1-1.331 6.638A4 4 0 1 0 14 2Zm1 9h-1.264A6.957 6.957 0 0 1 15 15v2a2.97 2.97 0 0 1-.184 1H19a1 1 0 0 0 1-1v-1a5.006 5.006 0 0 0-5-5ZM6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Z"/>
              </svg>
              <span class="flex-1 ms-3 whitespace-nowrap">Команда</span>
            </a>
        </li>
      </ul>
   </div>
</aside>


      <div class=" ml-80 h-full overflow-hidden p-3">
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
            <div class="flex-shrink-0 pb-3 flex flex-col w-80 bg-gray-100 rounded-md" :style="{ height: 'auto' }">
              <!-- Заголовок колонки с кнопкой для меню -->
              <div class="flex justify-between">
                <h3 class="pt-3 pb-3 px-3 font-semibold text-gray-700 text-lg">{{ element.title }}</h3>
                <div class="relative mt-3 mr-3">
                  <button @click="toggleDropdown(element.id)" class="text-gray-500 hover:text-gray-700 focus:outline-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
  
                  <!-- Выпадающее меню -->
                  <div v-if="dropdownOpen[element.id]" class="absolute right-0 mt-1 w-32 bg-white rounded shadow-md py-1 z-10 border border-gray-200">
                    <button @click="editItem(element.id)" class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100">
                      Edit
                    </button>
                    <button @click="archiveList(element.id)" class="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100">
                      Archive List
                    </button>
                  </div>
                </div>
              </div>
  
              <!-- Задачи внутри колонки -->
              <draggable
                v-model="element.tasks"
                :group="{ name: 'tasks', pull: true, put: true }"
                item-key="title"
                class="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-3 pb-1 space-y-3"
                animation="200"
              >
                <template #item="{ element: task }">
                  <a href="#" class="block p-5 rounded-md bg-white shadow">
                    <div class="flex justify-between">
                      <p class="text-sm font-medium text-gray-900 leading-snug">{{ task.title }}</p>
                      <img class="h-6 w-6 object-cover rounded-full" :src="task.avatar" />
                    </div>
                    <div class="flex items-baseline justify-between mt-2">
                      <div class="text-sm text-gray-600">
                        <time :datetime="task.date">{{ task.displayDate }}</time>
                      </div>
                      <span class="px-2 py-1 inline-flex items-center bg-indigo-100 rounded text-xs font-medium text-indigo-800">
                        <svg class="h-2 w-2 text-indigo-500 mr-2" viewBox="0 0 8 8" fill="currentColor">
                          <circle cx="4" cy="4" r="3" />
                        </svg>
                        {{ task.label }}
                      </span>
                    </div>
                  </a>
                </template>
              </draggable>
            </div>
          </template>
        </draggable>
      </div>
    </div>
</div>
  </template>
  
  <script>
  import draggable from 'vuedraggable';
  import Header from "@/components/header.vue";

  export default {
    name: 'CompactBacklog',
    components: { draggable, Header },
    data() {
      return {
        dropdownOpen: {},
        columns: [
          {
            id: 'backlog',
            title: 'Backlog',
            tasks: [
              {
                title: 'Работать сообща',
                avatar: 'https://images.unsplash.com/photo-1506755855567-92ff770e8d00?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80',
                date: '2020-08-10',
                label: 'Даша'
              }
            ]
          },
          {
            id: 'in-progress',
            title: 'In Progress',
            tasks: [
              {
                title: 'Сделать красивый фронт',
                avatar: 'https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&facepad=2.5&h=144&w=144&q=80',
                date: '2020-08-11',
                label: 'Даша'
              }
            ]
          }
        ]
      };
    },
    methods: {
      // Тогглить выпадающее меню для колонок
      toggleDropdown(columnId) {
        this.dropdownOpen[columnId] = !this.dropdownOpen[columnId];
      },
      editItem(columnId) {
        console.log(`Edit clicked on column ${columnId}`);
        this.dropdownOpen[columnId] = false;
      },
      archiveList(columnId) {
        console.log(`Archive List clicked on column ${columnId}`);
        this.dropdownOpen[columnId] = false;
      },
      // Проверка, чтобы колонка не вставлялась внутрь другой колонки
      onMoveColumn(evt) {
        // Проверяем, что перемещаемая колонка не вставляется в другую колонку
        const { from, to } = evt;
        return !to || to.nodeName !== 'DIV' || to.contains(from);
      }
    },
  };
  </script>
  
  <style scoped>
  /* Ваши стили */
  </style>
  