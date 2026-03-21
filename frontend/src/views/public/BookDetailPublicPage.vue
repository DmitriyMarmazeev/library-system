<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-center py-12">
      <ExclamationCircleIcon class="h-16 w-16 text-red-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Ошибка загрузки</h3>
      <p class="text-gray-600">{{ error }}</p>
      <router-link to="/books" class="mt-4 inline-block text-blue-600 hover:text-blue-800">
        ← Вернуться к каталогу
      </router-link>
    </div>

    <!-- Детали книги -->
    <div v-else-if="book" class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Заголовок -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
        <h1 class="text-3xl font-bold text-white mb-2">{{ book.title }}</h1>
        <p class="text-blue-100 text-lg">
          {{ authorNames }}
        </p>
      </div>

      <!-- Основная информация -->
      <div class="p-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Левая колонка: детали -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Аннотация -->
            <div v-if="book.description">
              <h2 class="text-xl font-semibold text-gray-900 mb-3">Аннотация</h2>
              <p class="text-gray-700 leading-relaxed">{{ book.description }}</p>
            </div>

            <!-- Детали -->
            <div>
              <h2 class="text-xl font-semibold text-gray-900 mb-3">Детали</h2>
              <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="book.isbn">
                  <dt class="text-sm text-gray-500">ISBN</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ book.isbn }}</dd>
                </div>
                <div v-if="book.publication_year">
                  <dt class="text-sm text-gray-500">Год издания</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ book.publication_year }}</dd>
                </div>
                <div v-if="book.publisher">
                  <dt class="text-sm text-gray-500">Издательство</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ book.publisher }}</dd>
                </div>
                <div v-if="book.pages">
                  <dt class="text-sm text-gray-500">Количество страниц</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ book.pages }}</dd>
                </div>
              </dl>
            </div>

            <!-- Жанры -->
            <div v-if="book.genres && book.genres.length > 0">
              <h2 class="text-xl font-semibold text-gray-900 mb-3">Жанры</h2>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="genre in book.genres"
                  :key="genre.id"
                  class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                >
                  {{ genre.name }}
                </span>
              </div>
            </div>
          </div>

          <!-- Правая колонка: статус и действия -->
          <div class="lg:col-span-1">
            <div class="bg-gray-50 rounded-lg p-6 sticky top-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Доступность</h2>
              
              <!-- Статус -->
              <div class="space-y-3 mb-6">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Всего экземпляров:</span>
                  <span class="font-semibold">{{ book.total_copies || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Доступно:</span>
                  <span :class="[
                    'font-semibold',
                    book.available_copies > 0 ? 'text-green-600' : 'text-red-600'
                  ]">
                    {{ book.available_copies || 0 }}
                  </span>
                </div>
              </div>

              <!-- Кнопки действий -->
              <div class="space-y-3">
                <router-link
                  v-if="auth.isAuthenticated && auth.isReader && book.available_copies > 0"
                  to="/reader/dashboard"
                  class="w-full block text-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
                >
                  Забронировать
                </router-link>

                <router-link
                  v-if="!auth.isAuthenticated"
                  to="/register"
                  class="w-full block text-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Зарегистрироваться, чтобы взять книгу
                </router-link>

                <router-link
                  to="/books"
                  class="w-full block text-center border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition"
                >
                  ← Назад к каталогу
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ExclamationCircleIcon } from '@heroicons/vue/24/outline'
import { booksApi } from '@/api/books'
import { useAuthStore } from '@/stores/auth'
import { formatFullName } from '@/utils/formatters'

const route = useRoute()
const auth = useAuthStore()

const book = ref(null)
const isLoading = ref(true)
const error = ref('')

const authorNames = computed(() => {
  if (!book.value?.authors || book.value.authors.length === 0) {
    return 'Автор не указан'
  }
  return book.value.authors.map(a => formatFullName(a)).join(', ')
})

const fetchBook = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await booksApi.getById(route.params.id)
    book.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки книги'
    console.error('Error fetching book:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchBook()
})
</script>