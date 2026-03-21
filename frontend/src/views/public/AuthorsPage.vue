<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Авторы</h1>
      <p class="text-gray-600 mt-2">
        Полный список авторов, чьи книги представлены в библиотеке
      </p>
    </div>

    <!-- Поиск -->
    <div class="mb-8">
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск авторов по имени или фамилии..."
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

    <!-- Список авторов -->
    <div v-else-if="authors.length > 0" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div
        v-for="author in authors"
        :key="author.id"
        class="bg-white rounded-lg shadow-sm hover:shadow-md transition p-6"
      >
        <div class="flex items-start gap-4">
          <!-- Аватар -->
          <div class="flex-shrink-0">
            <div
              :class="[
                'h-12 w-12 rounded-full flex items-center justify-center text-white text-lg font-semibold',
                getAvatarColor(formatFullName(author))
              ]"
            >
              {{ getInitials(author) }}
            </div>
          </div>

          <!-- Информация -->
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-gray-900 truncate">
              {{ formatFullName(author) }}
            </h3>
            <p class="text-sm text-gray-500">
              Книг в каталоге: {{ author.books_count || 0 }}
            </p>
          </div>
        </div>

        <!-- Ссылка на книги автора -->
        <div class="mt-4">
          <router-link
            :to="{ path: '/books', query: { author: `${author.last_name} ${author.first_name}` } }"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Показать книги →
          </router-link>
        </div>
      </div>
    </div>

    <!-- Пустой результат -->
    <div v-else class="text-center py-12">
      <UserGroupIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Авторы не найдены</h3>
      <p class="text-gray-600">
        {{ searchQuery ? 'Попробуйте изменить поисковый запрос' : 'В каталоге пока нет авторов' }}
      </p>
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
import { ref, onMounted, watch } from 'vue'
import { MagnifyingGlassIcon, UserGroupIcon } from '@heroicons/vue/24/outline'
import { booksApi } from '@/api/books'
import { usePagination } from '@/composables/usePagination'
import { debounce, getAvatarColor, getInitials } from '@/utils/helpers'
import { formatFullName } from '@/utils/formatters'

const authors = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const totalAuthors = ref(0)

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

const fetchAuthors = async () => {
  isLoading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    }
    
    const response = await booksApi.getAuthors(params)
    authors.value = response.data
    
    // Если есть поисковый запрос, используем поиск
    if (searchQuery.value) {
      const searchResponse = await booksApi.searchAuthors(searchQuery.value)
      authors.value = searchResponse.data
    }
    
    totalAuthors.value = authors.value.length
    setTotal(totalAuthors.value)
  } catch (error) {
    console.error('Error fetching authors:', error)
  } finally {
    isLoading.value = false
  }
}

const search = async () => {
  if (searchQuery.value) {
    isLoading.value = true
    try {
      const response = await booksApi.searchAuthors(searchQuery.value)
      authors.value = response.data
      totalAuthors.value = authors.value.length
      setTotal(totalAuthors.value)
    } catch (error) {
      console.error('Error searching authors:', error)
    } finally {
      isLoading.value = false
    }
  } else {
    fetchAuthors()
  }
}

const debouncedSearch = debounce(search, 500)

const goToPage = (page) => {
  if (typeof page === 'number') {
    setPage(page)
    fetchAuthors()
  }
}

watch(currentPage, () => {
  if (!searchQuery.value) {
    fetchAuthors()
  }
})

watch(searchQuery, (newVal) => {
  setPage(1)
  if (!newVal) {
    fetchAuthors()
  }
})

onMounted(() => {
  fetchAuthors()
})
</script>