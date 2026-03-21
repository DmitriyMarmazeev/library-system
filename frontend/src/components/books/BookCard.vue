<template>
  <div class="bg-white rounded-lg shadow-sm hover:shadow-md transition overflow-hidden">
    <div class="p-6">
      <!-- Заголовок и статус -->
      <div class="flex justify-between items-start mb-3">
        <h3 class="text-lg font-semibold text-gray-900 line-clamp-2">
          {{ book.title }}
        </h3>
        <span
          v-if="!compact"
          :class="[
            'px-2 py-1 text-xs font-medium rounded-full',
            book.available_copies > 0
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          ]"
        >
          {{ book.available_copies > 0 ? 'Доступна' : 'Нет в наличии' }}
        </span>
      </div>

      <!-- Авторы -->
      <p class="text-sm text-gray-600 mb-2 line-clamp-1">
        {{ authorNames }}
      </p>

      <!-- Дополнительная информация -->
      <div v-if="!compact" class="space-y-2 text-sm text-gray-500">
        <div class="flex items-center gap-2">
          <CalendarIcon class="h-4 w-4" />
          <span>{{ book.publication_year || 'Год не указан' }}</span>
        </div>
        <div class="flex items-center gap-2">
          <BuildingLibraryIcon class="h-4 w-4" />
          <span>{{ book.publisher || 'Издательство не указано' }}</span>
        </div>
        <div class="flex items-center gap-2">
          <DocumentTextIcon class="h-4 w-4" />
          <span>{{ book.pages || '?' }} стр.</span>
        </div>
        <div class="flex items-center gap-2">
          <CubeIcon class="h-4 w-4" />
          <span>
            Доступно: {{ book.available_copies || 0 }} из {{ book.total_copies || 0 }}
          </span>
        </div>
      </div>

      <!-- Кнопки -->
      <div class="mt-4 flex gap-2">
        <router-link
          :to="`/books/${book.id}`"
          class="flex-1 text-center text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          Подробнее
        </router-link>
        
        <button
          v-if="auth.isAuthenticated && auth.isReader && book.available_copies > 0"
          @click="handleBorrow"
          class="flex-1 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition text-sm"
        >
          Забронировать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { CalendarIcon, BuildingLibraryIcon, DocumentTextIcon, CubeIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { formatFullName } from '@/utils/formatters'

const props = defineProps({
  book: {
    type: Object,
    required: true
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const auth = useAuthStore()
const uiStore = useUIStore()

const authorNames = computed(() => {
  if (!props.book.authors || props.book.authors.length === 0) {
    return 'Автор не указан'
  }
  return props.book.authors.map(a => formatFullName(a)).join(', ')
})

const handleBorrow = () => {
  uiStore.info('Функция бронирования будет доступна в личном кабинете')
}
</script>