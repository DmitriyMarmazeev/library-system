<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Активные выдачи</h1>
        <p class="text-gray-600 mt-2">
          Список книг, находящихся на руках у читателей
        </p>
      </div>
      <router-link
        to="/librarian/loans/create"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="h-5 w-5" />
        Оформить выдачу
      </router-link>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Читатель</label>
          <input
            v-model="filters.reader"
            type="text"
            placeholder="ФИО читателя"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Книга</label>
          <input
            v-model="filters.book"
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
            <option value="">Все</option>
            <option value="active">В срок</option>
            <option value="overdue">Просрочено</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Дата возврата</label>
          <input
            v-model="filters.dueDate"
            type="date"
            class="input-field"
            @change="search"
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
          Найдено выдач: {{ totalLoans }}
        </span>
      </div>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Всего активных</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
          </div>
          <div class="bg-blue-100 p-3 rounded-full">
            <BookOpenIcon class="h-6 w-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Просрочено</p>
            <p class="text-2xl font-bold text-red-600">{{ stats.overdue }}</p>
          </div>
          <div class="bg-red-100 p-3 rounded-full">
            <ExclamationCircleIcon class="h-6 w-6 text-red-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">В срок</p>
            <p class="text-2xl font-bold text-green-600">{{ stats.onTime }}</p>
          </div>
          <div class="bg-green-100 p-3 rounded-full">
            <CheckCircleIcon class="h-6 w-6 text-green-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица выдач -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Читатель
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Книга
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Дата выдачи
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Срок возврата
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Статус
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Действия
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading">
              <td colspan="7" class="px-6 py-12 text-center">
                <div class="flex justify-center">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              </td>
            </tr>
            <tr v-else-if="loans.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                Активные выдачи не найдены
              </td>
            </tr>
            <tr
              v-for="loan in loans"
              :key="loan.id"
              class="hover:bg-gray-50"
              :class="{ 'bg-red-50': loan.is_overdue }"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                #{{ loan.id }}
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <div class="font-medium text-gray-900">{{ loan.user_name }}</div>
                  <div class="text-gray-500">{{ loan.user_email }}</div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <div class="font-medium text-gray-900">{{ loan.book_title }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(loan.loan_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm">
                  <div :class="['font-medium', loan.is_overdue ? 'text-red-600' : 'text-gray-900']">
                    {{ formatDate(loan.due_date) }}
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ loan.days_remaining > 0 ? `Осталось ${loan.days_remaining} дн.` : `Просрочено ${Math.abs(loan.days_remaining)} дн.` }}
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    loan.is_overdue
                      ? 'bg-red-100 text-red-800'
                      : 'bg-green-100 text-green-800'
                  ]"
                >
                  {{ loan.is_overdue ? 'Просрочена' : 'В срок' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right space-x-2">
                <button
                  @click="openReturnModal(loan)"
                  class="text-green-600 hover:text-green-800 inline-flex items-center gap-1"
                  title="Принять возврат"
                >
                  <ArrowLeftIcon class="h-5 w-5" />
                </button>
                <button
                  @click="openExtendModal(loan)"
                  class="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  title="Продлить"
                >
                  <ClockIcon class="h-5 w-5" />
                </button>
                <router-link
                  :to="`/librarian/loans/${loan.id}`"
                  class="text-yellow-600 hover:text-yellow-800 inline-flex items-center gap-1"
                  title="Детали"
                >
                  <EyeIcon class="h-5 w-5" />
                </router-link>
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

    <!-- Модальное окно возврата -->
    <AppModal
      v-model="showReturnModal"
      title="Оформление возврата"
      :show-actions="true"
      confirm-text="Подтвердить возврат"
      @confirm="handleReturn"
    >
      <div v-if="selectedLoan" class="space-y-4">
        <p class="text-gray-700">
          <span class="font-medium">Книга:</span> {{ selectedLoan.book_title }}
        </p>
        <p class="text-gray-700">
          <span class="font-medium">Читатель:</span> {{ selectedLoan.user_name }}
        </p>
        <p class="text-gray-700">
          <span class="font-medium">Должен был вернуть:</span> {{ formatDate(selectedLoan.due_date) }}
        </p>
        <p v-if="selectedLoan.is_overdue" class="text-red-600">
          Просрочка {{ Math.abs(selectedLoan.days_remaining) }} дней
        </p>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Дата возврата
          </label>
          <input
            v-model="returnDate"
            type="date"
            class="input-field"
            :max="new Date().toISOString().split('T')[0]"
          />
        </div>
      </div>
    </AppModal>

    <!-- Модальное окно продления -->
    <AppModal
      v-model="showExtendModal"
      title="Продление срока"
      :show-actions="true"
      confirm-text="Продлить"
      @confirm="handleExtend"
    >
      <div v-if="selectedLoan" class="space-y-4">
        <p class="text-gray-700">
          <span class="font-medium">Книга:</span> {{ selectedLoan.book_title }}
        </p>
        <p class="text-gray-700">
          <span class="font-medium">Читатель:</span> {{ selectedLoan.user_name }}
        </p>
        <p class="text-gray-700">
          <span class="font-medium">Текущий срок:</span> {{ formatDate(selectedLoan.due_date) }}
        </p>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Новый срок возврата
          </label>
          <input
            v-model="newDueDate"
            type="date"
            class="input-field"
            :min="new Date().toISOString().split('T')[0]"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Причина продления
          </label>
          <textarea
            v-model="extendReason"
            rows="3"
            class="input-field"
            placeholder="Укажите причину продления..."
          ></textarea>
        </div>
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import {
  PlusIcon,
  EyeIcon,
  ArrowLeftIcon,
  ClockIcon,
  BookOpenIcon,
  ExclamationCircleIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { useLoansStore } from '@/stores/loans'
import { useUIStore } from '@/stores/ui'
import { usePagination } from '@/composables/usePagination'
import { useFilters } from '@/composables/useFilters'
import AppModal from '@/components/ui/AppModal.vue'
import { formatDate } from '@/utils/formatters'
import { debounce } from '@/utils/helpers'

const loansStore = useLoansStore()
const uiStore = useUIStore()

const loans = ref([])
const isLoading = ref(false)
const totalLoans = ref(0)

const showReturnModal = ref(false)
const showExtendModal = ref(false)
const selectedLoan = ref(null)
const returnDate = ref(new Date().toISOString().split('T')[0])
const newDueDate = ref('')
const extendReason = ref('')

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
    reader: '',
    book: '',
    status: '',
    dueDate: ''
  },
  onFilterChange: (params) => {
    setPage(1)
    search(params)
  }
})

const stats = computed(() => {
  const total = loans.value.length
  const overdue = loans.value.filter(l => l.is_overdue).length
  return {
    total,
    overdue,
    onTime: total - overdue
  }
})

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const params = searchParams || filters.value
    const response = await loansStore.fetchActiveLoans({
      ...params,
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    })
    
    loans.value = response
    totalLoans.value = response.length
    setTotal(totalLoans.value)
  } catch (error) {
    console.error('Error searching loans:', error)
    uiStore.error('Ошибка загрузки выдач')
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

const openReturnModal = (loan) => {
  selectedLoan.value = loan
  returnDate.value = new Date().toISOString().split('T')[0]
  showReturnModal.value = true
}

const handleReturn = async () => {
  if (!selectedLoan.value) return

  try {
    await loansStore.returnLoan(selectedLoan.value.id, {
      return_date: returnDate.value
    })
    
    uiStore.success('Книга успешно возвращена')
    showReturnModal.value = false
    await search()
  } catch (error) {
    console.error('Error returning book:', error)
    uiStore.error('Ошибка при возврате книги')
  }
}

const openExtendModal = (loan) => {
  selectedLoan.value = loan
  // Предлагаем новую дату через 14 дней
  const newDate = new Date(loan.due_date)
  newDate.setDate(newDate.getDate() + 14)
  newDueDate.value = newDate.toISOString().split('T')[0]
  extendReason.value = ''
  showExtendModal.value = true
}

const handleExtend = async () => {
  if (!selectedLoan.value || !newDueDate.value) {
    uiStore.error('Укажите новую дату возврата')
    return
  }

  try {
    await loansStore.extendLoan(selectedLoan.value.id, {
      new_due_date: newDueDate.value,
      reason: extendReason.value || null
    })
    
    uiStore.success('Срок успешно продлен')
    showExtendModal.value = false
    await search()
  } catch (error) {
    console.error('Error extending loan:', error)
    uiStore.error('Ошибка при продлении срока')
  }
}

watch(currentPage, () => {
  if (!hasActiveFilters.value) {
    search()
  }
})

onMounted(() => {
  search()
})
</script>