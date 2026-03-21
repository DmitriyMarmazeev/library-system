<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Просроченные выдачи</h1>
      <p class="text-gray-600 mt-2">
        Книги, которые не были возвращены в срок
      </p>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Всего просрочек</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
          </div>
          <div class="bg-red-100 p-3 rounded-full">
            <ExclamationCircleIcon class="h-6 w-6 text-red-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Средняя просрочка</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.avgDays }} дн.</p>
          </div>
          <div class="bg-yellow-100 p-3 rounded-full">
            <ClockIcon class="h-6 w-6 text-yellow-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Макс. просрочка</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.maxDays }} дн.</p>
          </div>
          <div class="bg-orange-100 p-3 rounded-full">
            <ArrowTrendingUpIcon class="h-6 w-6 text-orange-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Читателей с долгами</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.debtors }}</p>
          </div>
          <div class="bg-purple-100 p-3 rounded-full">
            <UsersIcon class="h-6 w-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
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
          <label class="block text-sm font-medium text-gray-700 mb-1">Дней просрочки</label>
          <select
            v-model="filters.overdueDays"
            class="input-field"
            @change="search"
          >
            <option value="">Все</option>
            <option value="1-7">1-7 дней</option>
            <option value="8-14">8-14 дней</option>
            <option value="15-30">15-30 дней</option>
            <option value="30+">Более 30 дней</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end mt-4">
        <button
          @click="resetFilters"
          class="text-gray-600 hover:text-gray-900 text-sm"
        >
          Сбросить фильтры
        </button>
      </div>
    </div>

    <!-- Таблица просрочек -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Читатель
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Контакты
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
                Просрочка
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
            <tr v-else-if="overdueLoans.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                Просроченных выдач нет
              </td>
            </tr>
            <tr
              v-for="loan in overdueLoans"
              :key="loan.id"
              class="hover:bg-gray-50"
              :class="{
                'bg-red-50': loan.days_overdue > 30,
                'bg-yellow-50': loan.days_overdue > 14 && loan.days_overdue <= 30
              }"
            >
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ loan.user_name }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <div class="text-gray-900">{{ loan.user_email }}</div>
                  <div class="text-gray-500">{{ formatPhone(loan.user_phone) || '—' }}</div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ loan.book_title }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(loan.loan_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(loan.due_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm">
                  <span
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      loan.days_overdue > 30 ? 'bg-red-100 text-red-800' :
                      loan.days_overdue > 14 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-orange-100 text-orange-800'
                    ]"
                  >
                    {{ loan.days_overdue }} дн.
                  </span>
                </div>
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
                  @click="sendReminder(loan)"
                  class="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  title="Отправить напоминание"
                >
                  <EnvelopeIcon class="h-5 w-5" />
                </button>
                <button
                  @click="viewDetails(loan)"
                  class="text-yellow-600 hover:text-yellow-800 inline-flex items-center gap-1"
                  title="Детали"
                >
                  <EyeIcon class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
          <span class="font-medium">Просрочка:</span> {{ selectedLoan.days_overdue }} дней
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

        <div class="bg-yellow-50 p-4 rounded-lg">
          <div class="flex items-start gap-3">
            <ExclamationCircleIcon class="h-5 w-5 text-yellow-600 flex-shrink-0" />
            <p class="text-sm text-yellow-700">
              При возврате просроченной книги статус читателя будет автоматически обновлен.
            </p>
          </div>
        </div>
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ExclamationCircleIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  UsersIcon,
  ArrowLeftIcon,
  EnvelopeIcon,
  EyeIcon
} from '@heroicons/vue/24/outline'
import { useLoansStore } from '@/stores/loans'
import { useUIStore } from '@/stores/ui'
import { useFilters } from '@/composables/useFilters'
import AppModal from '@/components/ui/AppModal.vue'
import { formatDate, formatPhone } from '@/utils/formatters'
import { debounce } from '@/utils/helpers'

const router = useRouter()
const loansStore = useLoansStore()
const uiStore = useUIStore()

const overdueLoans = ref([])
const isLoading = ref(false)

const showReturnModal = ref(false)
const selectedLoan = ref(null)
const returnDate = ref(new Date().toISOString().split('T')[0])

const {
  filters,
  resetFilters,
  hasActiveFilters
} = useFilters({
  initialFilters: {
    reader: '',
    book: '',
    overdueDays: ''
  },
  onFilterChange: (params) => {
    search(params)
  }
})

const stats = computed(() => {
  const loans = overdueLoans.value
  const total = loans.length
  const totalDays = loans.reduce((sum, loan) => sum + loan.days_overdue, 0)
  const maxDays = loans.length > 0 ? Math.max(...loans.map(l => l.days_overdue)) : 0
  const uniqueDebtors = new Set(loans.map(l => l.user_id)).size

  return {
    total,
    avgDays: total > 0 ? Math.round(totalDays / total) : 0,
    maxDays,
    debtors: uniqueDebtors
  }
})

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const response = await loansStore.fetchOverdueLoans()
    let filtered = response

    // Применяем фильтры на клиенте
    const params = searchParams || filters.value
    if (params.reader) {
      const searchTerm = params.reader.toLowerCase()
      filtered = filtered.filter(loan =>
        loan.user_name.toLowerCase().includes(searchTerm)
      )
    }
    if (params.book) {
      const searchTerm = params.book.toLowerCase()
      filtered = filtered.filter(loan =>
        loan.book_title.toLowerCase().includes(searchTerm)
      )
    }
    if (params.overdueDays) {
      const [min, max] = params.overdueDays.split('-').map(Number)
      filtered = filtered.filter(loan => {
        if (max) {
          return loan.days_overdue >= min && loan.days_overdue <= max
        } else {
          return loan.days_overdue >= min
        }
      })
    }

    overdueLoans.value = filtered
  } catch (error) {
    console.error('Error fetching overdue loans:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

const debouncedSearch = debounce(search, 500)

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

const sendReminder = (loan) => {
  // В реальном приложении здесь будет отправка email
  uiStore.success(`Напоминание отправлено читателю ${loan.user_name}`)
}

const viewDetails = (loan) => {
  router.push(`/librarian/loans/${loan.id}`)
}

onMounted(() => {
  search()
})
</script>