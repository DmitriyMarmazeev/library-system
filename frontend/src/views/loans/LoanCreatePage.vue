<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Оформление выдачи</h1>
      <p class="text-gray-600 mt-2">
        Выберите читателя и книгу для оформления выдачи
      </p>
    </div>

    <!-- Форма -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Поиск читателя -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Читатель <span class="text-red-500">*</span>
          </label>
          
          <!-- Поиск -->
          <div class="relative mb-2">
            <input
              v-model="readerSearch"
              type="text"
              placeholder="Поиск читателя по имени или email..."
              class="input-field pl-10"
              @input="searchReaders"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          <!-- Результаты поиска -->
          <div v-if="readerSearchResults.length > 0" class="border rounded-lg divide-y max-h-60 overflow-y-auto mb-2">
            <div
              v-for="reader in readerSearchResults"
              :key="reader.id"
              @click="selectReader(reader)"
              class="p-3 hover:bg-gray-50 cursor-pointer"
              :class="{ 'bg-blue-50': selectedReader?.id === reader.id }"
            >
              <div class="flex items-center gap-3">
                <div
                  :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-white text-sm',
                    getAvatarColor(getDisplayName(reader))
                  ]"
                >
                  {{ getInitials(reader) }}
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ getDisplayName(reader) }}</p>
                  <p class="text-sm text-gray-500">{{ reader.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Выбранный читатель -->
          <div v-if="selectedReader" class="bg-green-50 rounded-lg p-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div
                :class="[
                  'h-10 w-10 rounded-full flex items-center justify-center text-white',
                  getAvatarColor(getDisplayName(selectedReader))
                ]"
              >
                {{ getInitials(selectedReader) }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ getDisplayName(selectedReader) }}</p>
                <p class="text-sm text-gray-600">{{ selectedReader.email }}</p>
              </div>
            </div>
            <button
              type="button"
              @click="selectedReader = null"
              class="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>

          <!-- Информация о читателе -->
          <div v-if="selectedReader" class="mt-3 grid grid-cols-2 gap-3 text-sm">
            <div class="bg-gray-50 rounded p-2">
              <span class="text-gray-500">Активных выдач:</span>
              <span class="ml-2 font-medium">{{ readerStats.activeLoans }}</span>
            </div>
            <div class="bg-gray-50 rounded p-2">
              <span class="text-gray-500">Просрочено:</span>
              <span class="ml-2 font-medium" :class="{ 'text-red-600': readerStats.overdueLoans > 0 }">
                {{ readerStats.overdueLoans }}
              </span>
            </div>
          </div>
        </div>

        <!-- Поиск книги -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Книга <span class="text-red-500">*</span>
          </label>

          <!-- Поиск -->
          <div class="relative mb-2">
            <input
              v-model="bookSearch"
              type="text"
              placeholder="Поиск книги по названию, автору или ISBN..."
              class="input-field pl-10"
              @input="searchBooks"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          <!-- Результаты поиска -->
          <div v-if="bookSearchResults.length > 0" class="border rounded-lg divide-y max-h-60 overflow-y-auto mb-2">
            <div
              v-for="book in bookSearchResults"
              :key="book.id"
              @click="selectBook(book)"
              class="p-3 hover:bg-gray-50 cursor-pointer"
              :class="{ 'bg-blue-50': selectedBook?.id === book.id }"
            >
              <div>
                <p class="font-medium text-gray-900">{{ book.title }}</p>
                <p class="text-sm text-gray-500">
                  {{ book.authors?.map(a => getDisplayName(a)).join(', ') || 'Автор не указан' }}
                </p>
                <div class="flex items-center gap-4 mt-1 text-xs">
                  <span>ISBN: {{ book.isbn || '—' }}</span>
                  <span :class="book.available_copies > 0 ? 'text-green-600' : 'text-red-600'">
                    Доступно: {{ book.available_copies || 0 }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Выбранная книга -->
          <div v-if="selectedBook" class="bg-green-50 rounded-lg p-3">
            <div class="flex items-start justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ selectedBook.title }}</p>
                <p class="text-sm text-gray-600">
                  {{ selectedBook.authors?.map(a => getDisplayName(a)).join(', ') || 'Автор не указан' }}
                </p>
                <p class="text-xs text-gray-500 mt-1">ISBN: {{ selectedBook.isbn || '—' }}</p>
              </div>
              <button
                type="button"
                @click="selectedBook = null"
                class="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon class="h-5 w-5" />
              </button>
            </div>

            <!-- Выбор экземпляра -->
            <div v-if="selectedBook.available_copies > 0" class="mt-3 pt-3 border-t">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Выберите экземпляр
              </label>
              <select
                v-model="selectedCopyId"
                class="input-field"
                required
              >
                <option value="">Выберите экземпляр</option>
                <option
                  v-for="copy in availableCopies"
                  :key="copy.id"
                  :value="copy.id"
                >
                  #{{ copy.id }} - {{ copy.location || 'Местоположение не указано' }}
                </option>
              </select>
            </div>
            <div v-else class="mt-3 pt-3 border-t text-red-600 text-sm">
              Нет доступных экземпляров для выдачи
            </div>
          </div>
        </div>

        <!-- Дата возврата -->
        <div v-if="selectedBook && selectedCopyId">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Дата возврата <span class="text-red-500">*</span>
          </label>
          <input
            v-model="dueDate"
            type="date"
            class="input-field max-w-xs"
            :min="minDueDate"
            :max="maxDueDate"
            required
          />
          <p class="text-sm text-gray-500 mt-1">
            Стандартный срок выдачи - 14 дней
          </p>
        </div>

        <!-- Кнопки -->
        <div class="flex justify-end gap-4 pt-4">
          <router-link
            to="/librarian/loans/active"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
          >
            Отмена
          </router-link>
          <button
            type="submit"
            :disabled="!canSubmit || isSubmitting"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ isSubmitting ? 'Оформление...' : 'Оформить выдачу' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  MagnifyingGlassIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useUsersStore } from '@/stores/users'
import { useBooksStore } from '@/stores/books'
import { useCopiesStore } from '@/stores/copies'
import { useLoansStore } from '@/stores/loans'
import { useUIStore } from '@/stores/ui'
import { getAvatarColor, getInitials, getDisplayName, debounce } from '@/utils/helpers'
import { addDays, format } from 'date-fns'

const router = useRouter()
const usersStore = useUsersStore()
const booksStore = useBooksStore()
const copiesStore = useCopiesStore()
const loansStore = useLoansStore()
const uiStore = useUIStore()

const readerSearch = ref('')
const readerSearchResults = ref([])
const selectedReader = ref(null)
const readerStats = ref({ activeLoans: 0, overdueLoans: 0 })

const bookSearch = ref('')
const bookSearchResults = ref([])
const selectedBook = ref(null)
const selectedCopyId = ref('')
const availableCopies = ref([])

const dueDate = ref('')
const isSubmitting = ref(false)

const minDueDate = computed(() => format(new Date(), 'yyyy-MM-dd'))
const maxDueDate = computed(() => format(addDays(new Date(), 30), 'yyyy-MM-dd'))

const canSubmit = computed(() => {
  return selectedReader.value && 
         selectedCopyId.value && 
         dueDate.value &&
         selectedBook.value?.available_copies > 0
})

// Поиск читателей
const searchReaders = debounce(async () => {
  if (!readerSearch.value.trim()) {
    readerSearchResults.value = []
    return
  }

  try {
    const response = await usersStore.searchUsers(readerSearch.value)
    readerSearchResults.value = response
  } catch (error) {
    console.error('Error searching readers:', error)
  }
}, 300)

// Выбор читателя
const selectReader = async (reader) => {
  selectedReader.value = reader
  readerSearchResults.value = []
  readerSearch.value = ''

  try {
    // Получаем статистику читателя
    const [activeLoans, borrowStatus] = await Promise.all([
      loansStore.fetchUserLoans(reader.id, { status: 'active' }),
      loansStore.fetchMyBorrowStatus() // Этот эндпоинт для текущего пользователя
    ])
    
    readerStats.value = {
      activeLoans: activeLoans.length,
      overdueLoans: borrowStatus?.overdue_loans || 0
    }

    // Проверяем, может ли читатель брать книги
    if (!borrowStatus?.can_borrow) {
      uiStore.warning('У читателя есть просроченные выдачи или достигнут лимит')
    }
  } catch (error) {
    console.error('Error fetching reader stats:', error)
  }
}

// Поиск книг
const searchBooks = debounce(async () => {
  if (!bookSearch.value.trim()) {
    bookSearchResults.value = []
    return
  }

  try {
    const response = await booksStore.searchBooks({
      title: bookSearch.value,
      author: bookSearch.value
    })
    bookSearchResults.value = response
  } catch (error) {
    console.error('Error searching books:', error)
  }
}, 300)

// Выбор книги
const selectBook = async (book) => {
  selectedBook.value = book
  bookSearchResults.value = []
  bookSearch.value = ''

  if (book.available_copies > 0) {
    await fetchAvailableCopies(book.id)
  }
  
  // Устанавливаем стандартную дату возврата через 14 дней
  dueDate.value = format(addDays(new Date(), 14), 'yyyy-MM-dd')
}

// Получение доступных экземпляров
const fetchAvailableCopies = async (bookId) => {
  try {
    const response = await copiesStore.fetchCopiesByBook(bookId)
    availableCopies.value = response.filter(c => c.status === 'available')
  } catch (error) {
    console.error('Error fetching available copies:', error)
  }
}

// Оформление выдачи
const handleSubmit = async () => {
  if (!canSubmit.value) return

  isSubmitting.value = true
  try {
    await loansStore.createLoan({
      copy_id: parseInt(selectedCopyId.value),
      user_id: selectedReader.value.id,
      due_date: dueDate.value
    })

    uiStore.success('Выдача успешно оформлена')
    router.push('/librarian/loans/active')
  } catch (error) {
    console.error('Error creating loan:', error)
    uiStore.error(error.response?.data?.detail || 'Ошибка при оформлении выдачи')
  } finally {
    isSubmitting.value = false
  }
}

watch(selectedCopyId, (newVal) => {
  if (newVal) {
    const copy = availableCopies.value.find(c => c.id === parseInt(newVal))
    if (copy && copy.location) {
      // Можно добавить дополнительную логику
    }
  }
})
</script>