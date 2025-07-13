<template>
    <div>
<h1>
    модель сайта
(че какая страничка там)
действия каждой кнопки или прочего
листинг обязательно
обосновать перспективу
</h1>

  
    <Transition name="fade">
    <div  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
        <div class="text-center">
          <div class="h-12 w-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Вы уверены, что хотите удалить команду?</h3>
          <p class="text-gray-600 mb-6">
            При удалении команда не будет отображаться в вашем портфолио. Вы можете расформировать команду, чтобы она осталась в истории.
          </p>
        </div>
        <div class="flex flex-col space-y-3 sm:flex-row sm:space-y-0 sm:space-x-3 justify-center">
          <button
            @click="$emit('delete')"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none transition"
          >
            Удалить
          </button>
          <button
            @click="$emit('disband')"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none transition"
          >
            Расформировать
          </button>
          <button
            @click="$emit('cancel')"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none transition"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </Transition>

</div>
  </template>