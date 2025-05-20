<template>
    <!-- Компактная кнопка для раскрытия панели -->
    <div class="fixed left-0 top-30 transform -translate-y-1/2 z-50 group">
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
                @click="goTo('statistic')"
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
                    @click="goTo('kanban')"
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
                    @click="goTo('info')"
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
            
            </ul>
        </div>
        </aside>
    </div>
</template>

<script>

export default {
  inject: ["globalState"],
  name: "navbar",
props: {
    ideaId: {
    type: [String, Number],
    required: true
  }
  },
computed: {
    selectedInstitute() {
      return this.globalState.institute;
    },
},
methods: {
    goTo(tab) {
  const institute = this.selectedInstitute;
  if (institute) {
    this.$router.push({ path: `/${institute}/project/${this.ideaId}/${tab}` });
  } else {
    console.error("Институт не выбран");
  }
    }
},
};

</script>
