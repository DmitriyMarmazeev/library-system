<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Жанры</h1>
      <p class="text-gray-600 mt-2">
        Каталог жанров для удобного поиска книг
      </p>
    </div>

    <!-- Поиск -->
    <div class="mb-8">
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск жанров..."
          class="input-field pl-10"
          @input="debouncedSearch"
        />
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Облако тегов -->
    <div v-else-if="genres.length > 0" class="bg-white rounded-lg shadow-sm p-8">
      <div class="flex flex-wrap gap-3 justify-center">
        <router-link
          v-for="genre in genres"
          :key="genre.id"
          :to="{ path: '/books', query: { genre: genre.name } }"
          class="group relative"
        >
          <span
            :class="[
              'inline-block px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 hover:scale-105',
              getGenreColor(genre.name)
            ]"
            :style="{
              fontSize: getFontSize(genre.books_count) + 'px'
            }"
          >
            {{ genre.name }}
            <span class="ml-1 text-xs opacity-75">
              ({{ genre.books_count }})
            </span>
          </span>
        </router-link>
      </div>
    </div>

    <!-- Пустой результат -->
    <div v-else class="text-center py-12">
      <TagIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Жанры не найдены</h3>
      <p class="text-gray-600">
        {{ searchQuery ? 'Попробуйте изменить поисковый запрос' : 'В каталоге пока нет жанров' }}
      </p>
    </div>

    <!-- Пагинация -->
    <div v-if="totalPages > 1 && !searchQuery" class="mt-8 flex justify-center">
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
import { ref, onMounted, watch } from 'vue'
import { MagnifyingGlassIcon, TagIcon } from '@heroicons/vue/24/outline'
import { booksApi } from '@/api/books'
import { usePagination } from '@/composables/usePagination'
import { debounce } from '@/utils/helpers'

const genres = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const totalGenres = ref(0)

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
} = usePagination({ initialPerPage: 30 })

// Цвета для жанров
const genreColors = [
  'bg-red-100 text-red-800 hover:bg-red-200',
  'bg-blue-100 text-blue-800 hover:bg-blue-200',
  'bg-green-100 text-green-800 hover:bg-green-200',
  'bg-yellow-100 text-yellow-800 hover:bg-yellow-200',
  'bg-purple-100 text-purple-800 hover:bg-purple-200',
  'bg-pink-100 text-pink-800 hover:bg-pink-200',
  'bg-indigo-100 text-indigo-800 hover:bg-indigo-200',
  'bg-orange-100 text-orange-800 hover:bg-orange-200',
  'bg-teal-100 text-teal-800 hover:bg-teal-200',
  'bg-cyan-100 text-cyan-800 hover:bg-cyan-200'
]

const getGenreColor = (genreName) => {
  const index = genreName.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return genreColors[index % genreColors.length]
}

const getFontSize = (booksCount) => {
  const minSize = 14
  const maxSize = 24
  const maxCount = 100
  
  if (!booksCount) return minSize
  const size = minSize + (Math.min(booksCount, maxCount) / maxCount) * (maxSize - minSize)
  return Math.round(size)
}

const fetchGenres = async () => {
  isLoading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    }
    
    const response = await booksApi.getGenres(params)
    genres.value = response.data
    totalGenres.value = response.headers?.['x-total-count'] || genres.value.length
    setTotal(totalGenres.value)
  } catch (error) {
    console.error('Error fetching genres:', error)
  } finally {
    isLoading.value = false
  }
}

const search = async () => {
  if (searchQuery.value) {
    isLoading.value = true
    try {
      const response = await booksApi.searchGenres(searchQuery.value)
      genres.value = response.data
      totalGenres.value = genres.value.length
      setTotal(totalGenres.value)
    } catch (error) {
      console.error('Error searching genres:', error)
    } finally {
      isLoading.value = false
    }
  } else {
    fetchGenres()
  }
}

const debouncedSearch = debounce(search, 500)

const goToPage = (page) => {
  if (typeof page === 'number') {
    setPage(page)
    fetchGenres()
  }
}

watch(currentPage, () => {
  if (!searchQuery.value) {
    fetchGenres()
  }
})

watch(searchQuery, (newVal) => {
  setPage(1)
  if (!newVal) {
    fetchGenres()
  }
})

onMounted(() => {
  fetchGenres()
})
</script>