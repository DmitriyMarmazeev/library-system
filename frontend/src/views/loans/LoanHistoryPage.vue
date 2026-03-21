<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">История выдач</h1>
      <p class="text-gray-600 mt-2">
        Полная история всех выдач книг в библиотеке
      </p>
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
            <option
              v-for="(label, value) in LOAN_STATUS_LABELS"
              :key="value"
              :value="value"
            >
              {{ label }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Период</label>
          <select
            v-model="filters.period"
            class="input-field"
            @change="search"
          >
            <option value="">За все время</option>
            <option value="today">Сегодня</option>
            <option value="week">Последняя неделя</option>
            <option value="month">Последний месяц</option>
            <option value="year">Последний год</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Дата с</label>
          <input
            v-model="filters.dateFrom"
            type="date"
            class="input-field"
            @change="search"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Дата по</label>
          <input
            v-model="filters.dateTo"
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
        <button
          @click="exportToCSV"
          class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition flex items-center gap-2"
        >
          <ArrowDownTrayIcon class="h-5 w-5" />
          Экспорт в CSV
        </button>
      </div>
    </div>

    <!-- Статистика по периодам -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Сегодня</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.today }}</p>
          </div>
          <div class="bg-blue-100 p-3 rounded-full">
            <CalendarIcon class="h-6 w-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">За неделю</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.week }}</p>
          </div>
          <div class="bg-green-100 p-3 rounded-full">
            <CalendarDaysIcon class="h-6 w-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">За месяц</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.month }}</p>
          </div>
          <div class="bg-yellow-100 p-3 rounded-full">
            <CalendarIcon class="h-6 w-6 text-yellow-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Средняя длительность</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.avgDuration }} дн.</p>
          </div>
          <div class="bg-purple-100 p-3 rounded-full">
            <ClockIcon class="h-6 w-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица истории -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Дата выдачи
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Читатель
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Книга
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Экземпляр
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Дата возврата
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Статус
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Длительность
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Действия
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading">
              <td colspan="8" class="px-6 py-12 text-center">
                <div class="flex justify-center">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              </td>
            </tr>
            <tr v-else-if="loans.length === 0">
              <td colspan="8" class="px-6 py-12 text-center text-gray-500">
                История выдач пуста
              </td>
            </tr>
            <tr
              v-for="loan in loans"
              :key="loan.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(loan.loan_date) }}
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
                  <div v-if="loan.book_isbn" class="text-gray-500">ISBN: {{ loan.book_isbn }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                #{{ loan.copy_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(loan.return_date) || '—' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    LOAN_STATUS_COLORS[loan.status]
                  ]"
                >
                  {{ LOAN_STATUS_LABELS[loan.status] }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ loan.duration || '—' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <button
                  @click="viewDetails(loan)"
                  class="text-blue-600 hover:text-blue-800"
                  title="Детали"
                >
                  <EyeIcon class="h-5 w-5" />
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  EyeIcon,
  ArrowDownTrayIcon,
  CalendarIcon,
  CalendarDaysIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import { useLoansStore } from '@/stores/loans'
import { useUIStore } from '@/stores/ui'
import { usePagination } from '@/composables/usePagination'
import { useFilters } from '@/composables/useFilters'
import {
  LOAN_STATUS,
  LOAN_STATUS_COLORS,
  LOAN_STATUS_LABELS
} from '@/utils/constants'
import { formatDate } from '@/utils/formatters'
import { debounce } from '@/utils/helpers'
import { differenceInDays, subDays, subWeeks, subMonths, subYears, isWithinInterval } from 'date-fns'

const router = useRouter()
const loansStore = useLoansStore()
const uiStore = useUIStore()

const loans = ref([])
const isLoading = ref(false)
const totalLoans = ref(0)

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
  resetFilters,
  hasActiveFilters
} = useFilters({
  initialFilters: {
    reader: '',
    book: '',
    status: '',
    period: '',
    dateFrom: '',
    dateTo: ''
  },
  onFilterChange: (params) => {
    setPage(1)
    search(params)
  }
})

const stats = computed(() => {
  const today = new Date()
  const todayLoans = loans.value.filter(loan =>
    formatDate(loan.loan_date) === formatDate(today)
  ).length
  
  const weekLoans = loans.value.filter(loan => {
    const loanDate = new Date(loan.loan_date)
    return loanDate >= subWeeks(today, 1)
  }).length
  
  const monthLoans = loans.value.filter(loan => {
    const loanDate = new Date(loan.loan_date)
    return loanDate >= subMonths(today, 1)
  }).length
  
  // Средняя длительность для возвращенных книг
  const returnedLoans = loans.value.filter(loan => loan.return_date)
  const totalDuration = returnedLoans.reduce((sum, loan) => {
    const start = new Date(loan.loan_date)
    const end = new Date(loan.return_date)
    return sum + differenceInDays(end, start)
  }, 0)
  const avgDuration = returnedLoans.length > 0
    ? Math.round(totalDuration / returnedLoans.length)
    : 0

  return {
    today: todayLoans,
    week: weekLoans,
    month: monthLoans,
    avgDuration
  }
})

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    }
    
    const response = await loansStore.fetchAllLoans(params)
    let filtered = response

    // Применяем фильтры
    const filtersData = searchParams || filters.value
    
    if (filtersData.reader) {
      const searchTerm = filtersData.reader.toLowerCase()
      filtered = filtered.filter(loan =>
        loan.user_name.toLowerCase().includes(searchTerm)
      )
    }
    
    if (filtersData.book) {
      const searchTerm = filtersData.book.toLowerCase()
      filtered = filtered.filter(loan =>
        loan.book_title.toLowerCase().includes(searchTerm)
      )
    }
    
    if (filtersData.status) {
      filtered = filtered.filter(loan => loan.status === filtersData.status)
    }
    
    if (filtersData.dateFrom || filtersData.dateTo) {
      filtered = filtered.filter(loan => {
        const loanDate = new Date(loan.loan_date)
        if (filtersData.dateFrom && filtersData.dateTo) {
          return isWithinInterval(loanDate, {
            start: new Date(filtersData.dateFrom),
            end: new Date(filtersData.dateTo)
          })
        } else if (filtersData.dateFrom) {
          return loanDate >= new Date(filtersData.dateFrom)
        } else if (filtersData.dateTo) {
          return loanDate <= new Date(filtersData.dateTo)
        }
        return true
      })
    } else if (filtersData.period) {
      const now = new Date()
      filtered = filtered.filter(loan => {
        const loanDate = new Date(loan.loan_date)
        switch (filtersData.period) {
          case 'today':
            return formatDate(loanDate) === formatDate(now)
          case 'week':
            return loanDate >= subWeeks(now, 1)
          case 'month':
            return loanDate >= subMonths(now, 1)
          case 'year':
            return loanDate >= subYears(now, 1)
          default:
            return true
        }
      })
    }

    loans.value = filtered
    totalLoans.value = filtered.length
    setTotal(totalLoans.value)
  } catch (error) {
    console.error('Error fetching loan history:', error)
    uiStore.error('Ошибка загрузки истории')
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

const viewDetails = (loan) => {
  router.push(`/librarian/loans/${loan.id}`)
}

const exportToCSV = () => {
  try {
    const headers = [
      'Дата выдачи',
      'Читатель',
      'Email читателя',
      'Книга',
      'ISBN',
      'Экземпляр',
      'Дата возврата',
      'Статус'
    ]

    const rows = loans.value.map(loan => [
      formatDate(loan.loan_date),
      loan.user_name,
      loan.user_email,
      loan.book_title,
      loan.book_isbn || '',
      `#${loan.copy_id}`,
      formatDate(loan.return_date) || '',
      LOAN_STATUS_LABELS[loan.status]
    ])

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `loan_history_${formatDate(new Date())}.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    uiStore.success('Данные экспортированы в CSV')
  } catch (error) {
    console.error('Error exporting to CSV:', error)
    uiStore.error('Ошибка при экспорте данных')
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