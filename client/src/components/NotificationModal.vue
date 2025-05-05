<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg max-w-md w-full">
      <h2 class="text-xl font-bold mb-2">{{ notification.title }}</h2>
      <p class="text-gray-700 mb-4">{{ notification.message }}</p>

      <div v-if="notification.notification_type === 'Apply_team'" class="text-sm text-gray-600">
        Заявка в команду подтверждена. Добро пожаловать!
      </div>

      <div v-else-if="notification.notification_type === 'Cancel_team'" class="text-sm text-red-600">
        Команда была отменена. Возможно, стоит создать новую?
      </div>

      <div v-else-if="notification.notification_type === 'team_request'" class="text-sm text-blue-600">
        Вам поступил новый запрос на вступление в команду.
      </div>

      <div v-else class="text-sm text-gray-400">
        Тип уведомления: {{ notification.type }}
      </div>

      <div class="mt-6 text-right">
        <button @click="$emit('close')" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Закрыть
        </button>
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
