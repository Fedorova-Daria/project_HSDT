<template>
  <div v-if="show" >
        <!-- 1. Приглашение в команду -->
<div v-if="notification.type === 'invitation_team'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Поздравляем! Вас пригласили в команду!</h2>
    <p class="text-gray-600 mb-4">Вас пригласили в команду:</p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <img src="https://via.placeholder.com/80" class="w-20 h-20 rounded-full mx-auto mb-3">
      <h3 class="text-xl font-semibold mb-1">Команда разработчиков</h3>
      <p class="text-sm text-gray-500 mb-3">Участников: 5</p>
      <div class="flex flex-wrap justify-center gap-2 mb-3">
        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Vue.js</span>
        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Tailwind</span>
      </div>
      <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">Подробнее</button>
    </div>
    
    <div class="flex flex-col gap-3">
      <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Принять приглашение</button>
      <button class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg">Отклонить</button>
    </div>
  </div>
</div>

<!-- 2. Вам кинули заявку в команду -->
<div v-else-if="notification.type === 'team_request'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в команду</h2>
    <p class="text-gray-600 mb-4">В вашу команду хочет вступить:</p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <img src="https://via.placeholder.com/80" class="w-20 h-20 rounded-full mx-auto mb-3">
      <h3 class="text-xl font-semibold mb-3">Алексей Иванов</h3>
      <div class="flex flex-wrap justify-center gap-2 mb-3">
        <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">React</span>
        <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">TypeScript</span>
      </div>
      <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">Подробнее</button>
    </div>
    
    <div class="flex flex-col gap-3">
      <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Принять</button>
      <button class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg">Отклонить</button>
      <button class="text-blue-600 hover:text-blue-800 text-sm font-medium mt-1">Рассмотреть все заявки</button>
    </div>
  </div>
</div>

<!-- 3. Заявка в проект (для заказчика) -->
<div v-else-if="notification.type === 'project_request'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в проект</h2>
    <p class="text-gray-600 mb-4">Над вашим проектом хочет работать:</p>
    
    <div class="space-y-4 mb-4">
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="font-semibold text-lg mb-2">Интернет-магазин</h4>
        <p class="text-gray-600 text-sm mb-3 line-clamp-2">Разработка современного интернет-магазина с использованием Vue.js и Node.js...</p>
        <div class="flex flex-wrap gap-2">
          <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">Vue.js</span>
          <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">Node.js</span>
        </div>
      </div>
      
      <div class="bg-gray-50 p-4 rounded-lg text-center">
        <h4 class="font-semibold mb-2">Команда: DevTeam</h4>
        <img src="https://via.placeholder.com/80" class="w-20 h-20 rounded-full mx-auto mb-3">
        <div class="flex flex-wrap justify-center gap-2">
          <span class="px-3 py-1 bg-orange-100 text-orange-800 text-sm rounded-full">PHP</span>
          <span class="px-3 py-1 bg-orange-100 text-orange-800 text-sm rounded-full">Laravel</span>
        </div>
      </div>
    </div>
    
    <div class="flex flex-col gap-3">
      <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Принять</button>
      <button class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg">Отклонить</button>
      <button class="text-blue-600 hover:text-blue-800 text-sm font-medium mt-1">Рассмотреть все заявки</button>
    </div>
  </div>
</div>

<!-- 4. Принятие заявки в проект (для студента) -->
<div v-if="notification.type === 'apply_team'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в проект</h2>
    <p class="text-gray-600 mb-4">Поздравляем! Вашу заявку принял проект <span class="font-semibold">Интернет-магазин</span></p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4">
      <h4 class="font-semibold text-lg mb-2">Интернет-магазин</h4>
      <p class="text-gray-600 text-sm mb-3 line-clamp-2">Разработка современного интернет-магазина с использованием Vue.js и Node.js...</p>
      <div class="flex flex-wrap gap-2">
        <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">Vue.js</span>
        <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">Node.js</span>
      </div>
    </div>
    
    <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Перейти к проекту</button>
  </div>
</div>

<!-- 5. Принятие в команду -->
<div v-if="notification.type === 'apply_project'" class="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50">
  <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">Заявка в команду</h2>
    <p class="text-gray-600 mb-4">Поздравляем! Вас приняли в команду <span class="font-semibold">Web разработчики</span></p>
    
    <div class="bg-gray-50 p-4 rounded-lg mb-4 text-center">
      <img src="https://via.placeholder.com/80" class="w-20 h-20 rounded-full mx-auto mb-3">
      <h3 class="text-xl font-semibold mb-1">Web разработчики</h3>
      <p class="text-sm text-gray-500 mb-3">Участников: 5</p>
      <div class="flex flex-wrap justify-center gap-2">
        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Vue.js</span>
        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Tailwind</span>
      </div>
    </div>
    
    <button class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">Перейти к команде</button>
  </div>
</div>
  </div>
</template>

<script>
export default {
  props: {
    show: Boolean,
    notification: Object
  }
};
</script>
