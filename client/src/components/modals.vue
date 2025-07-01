<template>
    <div>
  <!-- Фон модального окна -->
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- Контейнер модального окна -->
    <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
      <!-- Иконка и заголовок -->
      <div class="text-center mb-6">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
          <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900">Вы точно готовы начать работу?</h3>
      </div>

      <!-- Текст сообщения -->
      <div class="mb-6 text-center">
        <p class="text-gray-600">
          После создания идеи ваша команда автоматически начнёт работу над проектом и не сможет отправлять приглашения на проекты в бирже проектов.
        </p>
      </div>

      <!-- Кнопки действий -->
      <div class="flex justify-center space-x-4">
        <button class="px-5 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
          Назад
        </button>
        <button class="px-5 py-2.5 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200">
          Создать
        </button>
      </div>
    </div>
  </div>


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