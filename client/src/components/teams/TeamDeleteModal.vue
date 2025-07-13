<template>
  <Transition name="fade">
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-card rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
        <div class="text-center">
          <div class="h-12 w-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">
            Вы уверены, что хотите удалить команду?
          </h3>
          <p class="opacity-60 mb-6">
            При удалении команда не будет отображаться в вашем портфолио. 
            Вы можете расформировать команду, чтобы она осталась в истории.
          </p>
        </div>
        
        <div class="flex flex-col space-y-3 sm:flex-row sm:space-y-0 sm:space-x-3 justify-center">
          <button
            @click="handleDelete"
            :disabled="isLoading"
            class="px-4 py-2 bg-red-600 text-always-white rounded-md hover:bg-red-700 focus:outline-none transition disabled:opacity-50"
          >
            {{ isLoading && actionType === 'delete' ? 'Удаление...' : 'Удалить' }}
          </button>
          
          <button
            @click="handleDisband"
            :disabled="isLoading"
            class="px-4 py-2 bg-indigo-600 text-always-white rounded-md hover:bg-indigo-700 focus:outline-none transition disabled:opacity-50"
          >
            {{ isLoading && actionType === 'disband' ? 'Расформирование...' : 'Расформировать' }}
          </button>
          
          <button
            @click="handleCancel"
            :disabled="isLoading"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none transition disabled:opacity-50"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'TeamDeleteModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    teamId: {
      type: String,
      required: true
    }
  },
  emits: ['close', 'deleted', 'disbanded'],
  
  data() {
    return {
      isLoading: false,
      actionType: null // 'delete' или 'disband'
    }
  },
  
  methods: {
    handleDelete() {
      this.actionType = 'delete';
      this.$emit('delete');
    },
    
    handleDisband() {
      this.actionType = 'disband';
      this.$emit('disband');
    },
    
    handleCancel() {
      this.$emit('close');
    },
    
    setLoading(loading) {
      this.isLoading = loading;
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
