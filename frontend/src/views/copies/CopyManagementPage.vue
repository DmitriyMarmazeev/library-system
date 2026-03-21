<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Управление экземплярами книг</h1>
        <p class="text-gray-600 mt-2">
          Добавление, перемещение и списание экземпляров
        </p>
      </div>
      <button
        @click="showAddModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="h-5 w-5" />
        Добавить экземпляры
      </button>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Книга</label>
          <input
            v-model="filters.bookTitle"
            type="text"
            placeholder="Название книги"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
          <select
            v-model="filters.status"
            class="input-field"
            @change="search"
          >
            <option value="">Все статусы</option>
            <option
              v-for="(label, value) in COPY_STATUS_LABELS"
              :key="value"
              :value="value"
            >
              {{ label }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Местоположение</label>
          <input
            v-model="filters.location"
            type="text"
            placeholder="Поиск по местоположению"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">ID экземпляра</label>
          <input
            v-model="filters.copyId"
            type="text"
            placeholder="Поиск по ID"
            class="input-field"
            @input="debouncedSearch"
          />
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
          Найдено экземпляров: {{ totalCopies }}
        </span>
      </div>
    </div>

    <!-- Статистика по статусам -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div
        v-for="status in statusStats"
        :key="status.value"
        class="bg-white rounded-lg shadow-sm p-4 cursor-pointer hover:shadow-md transition"
        :class="{ 'ring-2 ring-blue-500': filters.status === status.value }"
        @click="filterByStatus(status.value)"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">{{ status.label }}</p>
            <p class="text-2xl font-bold" :class="status.color">{{ status.count }}</p>
          </div>
          <div class="p-3 rounded-full" :class="status.bgColor">
            <component :is="status.icon" class="h-6 w-6" :class="status.iconColor" />
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица экземпляров -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Книга
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Статус
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Местоположение
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Текущая выдача
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
            <tr v-else-if="copies.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                Экземпляры не найдены
              </td>
            </tr>
            <tr v-for="copy in copies" :key="copy.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                #{{ copy.id }}
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <router-link
                    :to="`/admin/books/${copy.book_id}`"
                    class="font-medium text-gray-900 hover:text-blue-600"
                  >
                    {{ copy.book_title }}
                  </router-link>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    COPY_STATUS_COLORS[copy.status]
                  ]"
                >
                  {{ COPY_STATUS_LABELS[copy.status] }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ copy.location || '—' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span v-if="copy.current_loan_id">
                  <router-link
                    :to="`/admin/loans/${copy.current_loan_id}`"
                    class="text-blue-600 hover:text-blue-800"
                  >
                    Выдача #{{ copy.current_loan_id }}
                  </router-link>
                </span>
                <span v-else>—</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right space-x-2">
                <button
                  @click="editCopy(copy)"
                  class="text-yellow-600 hover:text-yellow-800 inline-flex items-center gap-1"
                  title="Редактировать"
                >
                  <PencilIcon class="h-5 w-5" />
                </button>
                <button
                  @click="viewHistory(copy)"
                  class="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  title="История выдач"
                >
                  <ClockIcon class="h-5 w-5" />
                </button>
                <button
                  @click="deleteCopy(copy)"
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

    <!-- Модальное окно добавления экземпляров -->
    <AppModal
      v-model="showAddModal"
      title="Добавление экземпляров"
      :show-actions="true"
      @confirm="handleAddCopies"
    >
      <form class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Книга <span class="text-red-500">*</span>
          </label>
          <select
            v-model="bulkForm.book_id"
            class="input-field"
            required
          >
            <option value="">Выберите книгу</option>
            <option
              v-for="book in books"
              :key="book.id"
              :value="book.id"
            >
              {{ book.title }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Количество <span class="text-red-500">*</span>
          </label>
          <input
            v-model.number="bulkForm.count"
            type="number"
            min="1"
            max="100"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Местоположение
          </label>
          <input
            v-model="bulkForm.location"
            type="text"
            class="input-field"
            placeholder="Например: Абонемент, ряд 3, полка 5"
          />
        </div>
      </form>
    </AppModal>

    <!-- Модальное окно редактирования -->
    <AppModal
      v-model="showEditModal"
      title="Редактирование экземпляра"
      :show-actions="true"
      @confirm="handleEditCopy"
    >
      <form class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Статус
          </label>
          <select
            v-model="editForm.status"
            class="input-field"
          >
            <option
              v-for="(label, value) in COPY_STATUS_LABELS"
              :key="value"
              :value="value"
            >
              {{ label }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Местоположение
          </label>
          <input
            v-model="editForm.location"
            type="text"
            class="input-field"
          />
        </div>

        <div v-if="editForm.status === 'damaged' || editForm.status === 'lost'">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Причина
          </label>
          <textarea
            v-model="editForm.reason"
            rows="3"
            class="input-field"
            placeholder="Укажите причину изменения статуса"
          ></textarea>
        </div>
      </form>
    </AppModal>

    <!-- Модальное окно истории -->
    <AppModal
      v-model="showHistoryModal"
      :title="`История выдач экземпляра #${selectedCopy?.id}`"
      size="lg"
    >
      <div v-if="loanHistory.length > 0" class="space-y-4">
        <div
          v-for="loan in loanHistory"
          :key="loan.loan_id"
          class="border rounded-lg p-4"
        >
          <div class="flex justify-between items-start">
            <div>
              <p class="text-sm font-medium text-gray-900">
                Читатель: {{ loan.reader_name }}
              </p>
              <p class="text-sm text-gray-500">
                Выдана: {{ formatDate(loan.loan_date) }}
              </p>
              <p class="text-sm text-gray-500">
                Возвращена: {{ formatDate(loan.return_date) || 'Не возвращена' }}
              </p>
            </div>
            <span
              :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                LOAN_STATUS_COLORS[loan.status]
              ]"
            >
              {{ LOAN_STATUS_LABELS[loan.status] }}
            </span>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        История выдач пуста
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  ClockIcon,
  BookOpenIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'
import { useCopiesStore } from '@/stores/copies'
import { useBooksStore } from '@/stores/books'
import { useUIStore } from '@/stores/ui'
import { usePagination } from '@/composables/usePagination'
import { useFilters } from '@/composables/useFilters'
import AppModal from '@/components/ui/AppModal.vue'
import {
  COPY_STATUS,
  COPY_STATUS_COLORS,
  COPY_STATUS_LABELS,
  LOAN_STATUS_COLORS,
  LOAN_STATUS_LABELS
} from '@/utils/constants'
import { formatDate } from '@/utils/formatters'
import { debounce } from '@/utils/helpers'

const copiesStore = useCopiesStore()
const booksStore = useBooksStore()
const uiStore = useUIStore()

const copies = ref([])
const books = ref([])
const isLoading = ref(false)
const totalCopies = ref(0)

const showAddModal = ref(false)
const showEditModal = ref(false)
const showHistoryModal = ref(false)
const selectedCopy = ref(null)
const loanHistory = ref([])

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
  setFilter,
  resetFilters,
  hasActiveFilters
} = useFilters({
  initialFilters: {
    bookTitle: '',
    status: '',
    location: '',
    copyId: ''
  },
  onFilterChange: (params) => {
    setPage(1)
    search(params)
  }
})

const bulkForm = reactive({
  book_id: '',
  count: 1,
  location: ''
})

const editForm = reactive({
  status: '',
  location: '',
  reason: ''
})

// Статистика по статусам
const statusStats = computed(() => {
  const stats = {}
  Object.values(COPY_STATUS).forEach(status => {
    stats[status] = copies.value.filter(c => c.status === status).length
  })
  
  return [
    {
      value: COPY_STATUS.AVAILABLE,
      label: COPY_STATUS_LABELS[COPY_STATUS.AVAILABLE],
      count: stats[COPY_STATUS.AVAILABLE] || 0,
      icon: CheckCircleIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      iconColor: 'text-green-600'
    },
    {
      value: COPY_STATUS.BORROWED,
      label: COPY_STATUS_LABELS[COPY_STATUS.BORROWED],
      count: stats[COPY_STATUS.BORROWED] || 0,
      icon: BookOpenIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      iconColor: 'text-blue-600'
    },
    {
      value: COPY_STATUS.DAMAGED,
      label: COPY_STATUS_LABELS[COPY_STATUS.DAMAGED],
      count: stats[COPY_STATUS.DAMAGED] || 0,
      icon: ExclamationCircleIcon,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
      iconColor: 'text-yellow-600'
    },
    {
      value: COPY_STATUS.LOST,
      label: COPY_STATUS_LABELS[COPY_STATUS.LOST],
      count: stats[COPY_STATUS.LOST] || 0,
      icon: XCircleIcon,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
      iconColor: 'text-red-600'
    }
  ]
})

const filterByStatus = (status) => {
  setFilter('status', status === filters.status ? '' : status)
}

const fetchBooks = async () => {
  try {
    books.value = await booksStore.fetchBooks({ limit: 1000 })
  } catch (error) {
    console.error('Error fetching books:', error)
  }
}

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const params = searchParams || filters.value
    const response = await copiesStore.fetchCopies({
      ...params,
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    })
    
    copies.value = response
    totalCopies.value = response.length
    setTotal(totalCopies.value)
  } catch (error) {
    console.error('Error searching copies:', error)
    uiStore.error('Ошибка загрузки экземпляров')
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

const handleAddCopies = async () => {
  if (!bulkForm.book_id || !bulkForm.count) {
    uiStore.error('Заполните обязательные поля')
    return
  }

  try {
    const response = await copiesStore.createCopiesBulk({
      book_id: parseInt(bulkForm.book_id),
      count: bulkForm.count,
      location: bulkForm.location || null
    })
    
    uiStore.success(`Добавлено ${response.created_count} экземпляров`)
    showAddModal.value = false
    
    // Сброс формы
    bulkForm.book_id = ''
    bulkForm.count = 1
    bulkForm.location = ''
    
    await search()
  } catch (error) {
    console.error('Error adding copies:', error)
    uiStore.error('Ошибка при добавлении экземпляров')
  }
}

const editCopy = (copy) => {
  selectedCopy.value = copy
  editForm.status = copy.status
  editForm.location = copy.location || ''
  editForm.reason = ''
  showEditModal.value = true
}

const handleEditCopy = async () => {
  if (!selectedCopy.value) return

  try {
    await copiesStore.updateCopy(selectedCopy.value.id, {
      status: editForm.status,
      location: editForm.location
    })
    
    uiStore.success('Экземпляр обновлен')
    showEditModal.value = false
    await search()
  } catch (error) {
    console.error('Error updating copy:', error)
    uiStore.error('Ошибка при обновлении экземпляра')
  }
}

const deleteCopy = async (copy) => {
  if (!confirm(`Удалить экземпляр #${copy.id}?`)) return

  try {
    await copiesStore.deleteCopy(copy.id)
    uiStore.success('Экземпляр удален')
    await search()
  } catch (error) {
    console.error('Error deleting copy:', error)
    uiStore.error('Ошибка при удалении экземпляра')
  }
}

const viewHistory = async (copy) => {
  selectedCopy.value = copy
  try {
    const response = await copiesStore.fetchCopyLoanHistory(copy.id)
    loanHistory.value = response
    showHistoryModal.value = true
  } catch (error) {
    console.error('Error fetching loan history:', error)
    uiStore.error('Ошибка загрузки истории')
  }
}

watch(currentPage, () => {
  if (!hasActiveFilters.value) {
    search()
  }
})

onMounted(() => {
  fetchBooks()
  search()
})
</script>