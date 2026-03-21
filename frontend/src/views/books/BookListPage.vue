<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Управление книгами</h1>
        <p class="text-gray-600 mt-2">
          Добавление, редактирование и удаление книг в каталоге
        </p>
      </div>
      <router-link
        to="/admin/books/create"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="h-5 w-5" />
        Добавить книгу
      </router-link>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
          <input
            v-model="filters.title"
            type="text"
            placeholder="Поиск по названию"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">ISBN</label>
          <input
            v-model="filters.isbn"
            type="text"
            placeholder="Поиск по ISBN"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Автор</label>
          <input
            v-model="filters.author"
            type="text"
            placeholder="Фамилия автора"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Жанр</label>
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

    <!-- Таблица книг -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Название
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Авторы
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ISBN
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Год
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Экземпляры
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Действия
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex justify-center">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              </td>
            </tr>
            <tr v-else-if="books.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                Книги не найдены
              </td>
            </tr>
            <tr v-for="book in books" :key="book.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ book.title }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  {{ book.authors?.map(a => `${a.last_name} ${a.first_name[0]}.`).join(', ') || '—' }}
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-500">{{ book.isbn || '—' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-500">{{ book.publication_year || '—' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <span class="text-gray-900">{{ book.available_copies || 0 }}</span>
                  <span class="text-gray-500"> / {{ book.total_copies || 0 }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-right space-x-2">
                <router-link
                  :to="`/admin/books/${book.id}`"
                  class="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  title="Просмотр"
                >
                  <EyeIcon class="h-5 w-5" />
                </router-link>
                <router-link
                  :to="`/admin/books/${book.id}/edit`"
                  class="text-yellow-600 hover:text-yellow-800 inline-flex items-center gap-1"
                  title="Редактировать"
                >
                  <PencilIcon class="h-5 w-5" />
                </router-link>
                <button
                  @click="confirmDelete(book)"
                  class="text-red-600 hover:text-red-800 inline-flex items-center gap-1"
                  title="Удалить"
                >
                  <TrashIcon class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-200">
        <div class="flex justify-center">
          <nav class="flex items-center gap-2">
            <button
              @click="prevPage"
              :disabled="!hasPrevPage"
              class="px-3 py-1 rounded border disabled:opacity-50"
            >
              ←
            </button>
            <button
              v-for="page in paginationRange"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'px-3 py-1 rounded',
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
              class="px-3 py-1 rounded border disabled:opacity-50"
            >
              →
            </button>
          </nav>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <AppModal
      v-model="showDeleteModal"
      title="Подтверждение удаления"
      :show-actions="true"
      confirm-variant="danger"
      confirm-text="Удалить"
      @confirm="handleDelete"
    >
      <p class="text-gray-700">
        Вы уверены, что хотите удалить книгу
        <span class="font-semibold">"{{ selectedBook?.title }}"</span>?
      </p>
      <p class="text-sm text-red-600 mt-2">
        Внимание! Это действие нельзя отменить.
      </p>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { useBooksStore } from '@/stores/books'
import { useUIStore } from '@/stores/ui'
import { usePagination } from '@/composables/usePagination'
import { useFilters } from '@/composables/useFilters'
import AppModal from '@/components/ui/AppModal.vue'
import { debounce } from '@/utils/helpers'

const router = useRouter()
const booksStore = useBooksStore()
const uiStore = useUIStore()

const books = ref([])
const genres = ref([])
const isLoading = ref(false)
const totalBooks = ref(0)

const showDeleteModal = ref(false)
const selectedBook = ref(null)

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
} = usePagination({ initialPerPage: 10 })

const {
  filters,
  searchQuery,
  setFilter,
  resetFilters,
  hasActiveFilters
} = useFilters({
  initialFilters: {
    title: '',
    isbn: '',
    author: '',
    genre: ''
  },
  onFilterChange: (params) => {
    setPage(1)
    search(params)
  }
})

const fetchGenres = async () => {
  try {
    const response = await booksStore.fetchGenres({ limit: 100 })
    genres.value = response
  } catch (error) {
    console.error('Error fetching genres:', error)
  }
}

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const params = searchParams || filters.value
    const response = await booksStore.searchBooks({
      ...params,
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    })
    
    books.value = response
    totalBooks.value = response.length // В реальном приложении брать из заголовков
    setTotal(totalBooks.value)
  } catch (error) {
    console.error('Error searching books:', error)
    uiStore.error('Ошибка загрузки книг')
  } finally {
    isLoading.value = false
  }
}

const debouncedSearch = debounce(search, 500)

const goToPage = (page) => {
  if (typeof page === 'number') {
    setPage(page)
    search()
  }
}

const confirmDelete = (book) => {
  selectedBook.value = book
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!selectedBook.value) return
  
  try {
    await booksStore.deleteBook(selectedBook.value.id)
    uiStore.success('Книга успешно удалена')
    showDeleteModal.value = false
    search()
  } catch (error) {
    console.error('Error deleting book:', error)
    uiStore.error('Ошибка при удалении книги')
  }
}

watch(currentPage, () => {
  if (!hasActiveFilters.value) {
    search()
  }
})

onMounted(() => {
  fetchGenres()
  search()
})
</script>