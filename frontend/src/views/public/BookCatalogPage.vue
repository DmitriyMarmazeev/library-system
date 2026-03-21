<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Каталог книг</h1>
      <p class="text-gray-600 mt-2">
        Найдите интересующие вас книги в нашей библиотеке
      </p>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Название
          </label>
          <input
            v-model="filters.title"
            type="text"
            placeholder="Введите название"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Автор
          </label>
          <input
            v-model="filters.author"
            type="text"
            placeholder="Фамилия автора"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Жанр
          </label>
          <select
            v-model="filters.genre"
            class="input-field"
            @change="search"
          >
            <option value="">Все жанры</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.name">
              {{ genre.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Год издания
          </label>
          <div class="flex gap-2">
            <div class="relative flex-1">
              <input
                v-model.number="filters.year_from"
                type="number"
                placeholder="От"
                class="input-field"
                :class="{ 'border-red-500': yearErrors.from }"
                @input="validateAndSearch"
                @blur="validateYear('from')"
              />
              <p v-if="yearErrors.from" class="absolute text-xs text-red-600 mt-1">
                {{ yearErrors.from }}
              </p>
            </div>
            <div class="relative flex-1">
              <input
                v-model.number="filters.year_to"
                type="number"
                placeholder="До"
                class="input-field"
                :class="{ 'border-red-500': yearErrors.to }"
                @input="validateAndSearch"
                @blur="validateYear('to')"
              />
              <p v-if="yearErrors.to" class="absolute text-xs text-red-600 mt-1">
                {{ yearErrors.to }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Ошибки валидации -->
      <div v-if="hasYearErrors" class="mt-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
        <p v-if="yearErrors.from">{{ yearErrors.from }}</p>
        <p v-if="yearErrors.to">{{ yearErrors.to }}</p>
        <p v-if="yearErrors.range">{{ yearErrors.range }}</p>
      </div>

      <div class="flex justify-between items-center mt-4">
        <button
          @click="resetFilters"
          class="text-gray-600 hover:text-gray-900 text-sm"
        >
          Сбросить фильтры
        </button>
        <span class="text-sm text-gray-600">
          Найдено книг: {{ totalBooks }}
        </span>
      </div>
    </div>

    <!-- Результаты -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else-if="books.length === 0" class="text-center py-12">
      <BookOpenIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Книги не найдены</h3>
      <p class="text-gray-600">
        Попробуйте изменить параметры поиска
      </p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
      />
    </div>

    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav class="flex items-center gap-2">
        <button
          @click="prevPage"
          :disabled="!hasPrevPage"
          class="px-3 py-2 rounded-lg border disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ←
        </button>
        
        <button
          v-for="page in paginationRange"
          :key="page"
          @click="goToPage(page)"
          :class="[
            'px-3 py-2 rounded-lg',
            page === currentPage
              ? 'bg-blue-600 text-white'
              : 'hover:bg-gray-100'
          ]"
          :disabled="page === '...'"
        >
          {{ page }}
        </button>

        <button
          @click="nextPage"
          :disabled="!hasNextPage"
          class="px-3 py-2 rounded-lg border disabled:opacity-50 disabled:cursor-not-allowed"
        >
          →
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { BookOpenIcon } from '@heroicons/vue/24/outline'
import BookCard from '@/components/books/BookCard.vue'
import { booksApi } from '@/api/books'
import { usePagination } from '@/composables/usePagination'
import { debounce } from '@/utils/helpers'

const books = ref([])
const genres = ref([])
const isLoading = ref(false)
const totalBooks = ref(0)

// Состояние для ошибок валидации
const yearErrors = reactive({
  from: '',
  to: '',
  range: ''
})

const filters = reactive({
  title: '',
  author: '',
  genre: '',
  year_from: null,
  year_to: null
})

const {
  currentPage,
  perPage,
  totalPages,
  hasNextPage,
  hasPrevPage,
  paginationRange,
  setPage,
  nextPage,
  prevPage,
  setTotal
} = usePagination({ initialPerPage: 12 })

const hasYearErrors = computed(() => {
  return yearErrors.from || yearErrors.to || yearErrors.range
})

// Функция валидации года
const validateYear = (field) => {
  const currentYear = new Date().getFullYear()
  
  if (field === 'from' && filters.year_from !== null && filters.year_from !== '') {
    if (filters.year_from < 1400) {
      yearErrors.from = 'Год должен быть не ранее 1400'
    } else if (filters.year_from > currentYear) {
      yearErrors.from = 'Год не может быть в будущем'
    } else {
      yearErrors.from = ''
    }
  } else if (field === 'from') {
    yearErrors.from = ''
  }

  if (field === 'to' && filters.year_to !== null && filters.year_to !== '') {
    if (filters.year_to < 1400) {
      yearErrors.to = 'Год должен быть не ранее 1400'
    } else if (filters.year_to > currentYear) {
      yearErrors.to = 'Год не может быть в будущем'
    } else {
      yearErrors.to = ''
    }
  } else if (field === 'to') {
    yearErrors.to = ''
  }

  // Проверка соотношения годов
  if (filters.year_from && filters.year_to) {
    if (filters.year_to < filters.year_from) {
      yearErrors.range = 'Год "До" должен быть больше или равен году "От"'
    } else {
      yearErrors.range = ''
    }
  } else {
    yearErrors.range = ''
  }
}

// Валидация всех полей перед отправкой
const validateFilters = () => {
  validateYear('from')
  validateYear('to')
  return !hasYearErrors.value
}

// Функция поиска с валидацией
const validateAndSearch = () => {
  validateYear('from')
  validateYear('to')
  debouncedSearch()
}

const fetchGenres = async () => {
  try {
    const response = await booksApi.getGenres({ limit: 100 })
    genres.value = response.data
  } catch (error) {
    console.error('Error fetching genres:', error)
  }
}

const search = async () => {
  // Не отправляем запрос, если есть ошибки валидации
  if (!validateFilters()) {
    return
  }

  isLoading.value = true
  try {
    const params = {
      ...filters,
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    }
    
    // Удаляем пустые значения
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

    const response = await booksApi.search(params)
    books.value = response.data
    
    // Предполагаем общее количество из заголовка или вычисляем
    totalBooks.value = response.headers?.['x-total-count'] || books.value.length
    setTotal(totalBooks.value)
  } catch (error) {
    console.error('Error searching books:', error)
  } finally {
    isLoading.value = false
  }
}

const debouncedSearch = debounce(search, 500)

const resetFilters = () => {
  filters.title = ''
  filters.author = ''
  filters.genre = ''
  filters.year_from = null
  filters.year_to = null
  yearErrors.from = ''
  yearErrors.to = ''
  yearErrors.range = ''
  setPage(1)
  search()
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    setPage(page)
    search()
  }
}

watch(currentPage, () => {
  search()
})

onMounted(() => {
  fetchGenres()
  search()
})
</script>