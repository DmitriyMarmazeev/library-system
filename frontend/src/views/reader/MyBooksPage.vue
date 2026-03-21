<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Мои книги</h1>
      <p class="text-gray-600 mt-2">
        Активные выдачи и история чтения
      </p>
    </div>

    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else>
      <!-- Активные выдачи -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <BookOpenIcon class="h-5 w-5 text-blue-600" />
            Книги на руках
          </h2>
        </div>

        <div class="p-6">
          <div v-if="activeLoans.length > 0" class="space-y-4">
            <div
              v-for="loan in activeLoans"
              :key="loan.id"
              class="border rounded-lg p-4 hover:shadow-md transition"
            >
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 text-lg">{{ loan.book_title }}</h3>
                  <p class="text-sm text-gray-500 mt-1">
                    Взята: {{ formatDate(loan.loan_date) }}
                  </p>
                  <div class="mt-2 flex flex-wrap gap-4">
                    <div class="flex items-center gap-1 text-sm">
                      <CalendarIcon class="h-4 w-4 text-gray-400" />
                      <span class="text-gray-600">Вернуть до:</span>
                      <span class="font-medium" :class="loan.is_overdue ? 'text-red-600' : 'text-gray-900'">
                        {{ formatDate(loan.due_date) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-1 text-sm">
                      <ClockIcon class="h-4 w-4 text-gray-400" />
                      <span class="text-gray-600">Осталось дней:</span>
                      <span :class="loan.is_overdue ? 'text-red-600 font-bold' : 'text-gray-900'">
                        {{ loan.days_remaining > 0 ? loan.days_remaining : Math.abs(loan.days_remaining) }}
                        {{ loan.days_remaining > 0 ? 'дн.' : 'дн. просрочки' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-2">
                  <span
                    :class="[
                      'px-3 py-1 text-sm font-medium rounded-full',
                      loan.is_overdue
                        ? 'bg-red-100 text-red-800'
                        : 'bg-green-100 text-green-800'
                    ]"
                  >
                    {{ loan.is_overdue ? 'Просрочена' : 'В срок' }}
                  </span>
                  <div class="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      :class="[
                        'h-2 rounded-full transition-all',
                        loan.is_overdue ? 'bg-red-500' : 'bg-green-500'
                      ]"
                      :style="{ width: loanProgress(loan) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-12">
            <BookOpenIcon class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <p class="text-gray-500">У вас нет книг на руках</p>
            <router-link
              to="/books"
              class="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Перейти к каталогу
            </router-link>
          </div>
        </div>
      </div>

      <!-- История чтения -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <ClockIcon class="h-5 w-5 text-gray-600" />
            История чтения
          </h2>
        </div>

        <div class="p-6">
          <div v-if="loanHistory.length > 0" class="space-y-3">
            <div
              v-for="loan in loanHistory"
              :key="loan.id"
              class="border rounded-lg p-4 hover:bg-gray-50 transition"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{{ loan.book_title }}</h3>
                  <div class="flex flex-wrap gap-4 mt-2 text-sm text-gray-500">
                    <span>Взята: {{ formatDate(loan.loan_date) }}</span>
                    <span v-if="loan.return_date">Возвращена: {{ formatDate(loan.return_date) }}</span>
                  </div>
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

          <div v-else class="text-center py-12">
            <ClockIcon class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <p class="text-gray-500">История чтения пуста</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { loansApi } from '@/api/loans'
import {
  BookOpenIcon,
  CalendarIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import { formatDate } from '@/utils/formatters'
import { LOAN_STATUS_COLORS, LOAN_STATUS_LABELS } from '@/utils/constants'
import { differenceInDays } from 'date-fns'

const router = useRouter()
const auth = useAuthStore()
const uiStore = useUIStore()

const isLoading = ref(false)
const activeLoans = ref([])
const loanHistory = ref([])

const loanProgress = (loan) => {
  if (!loan.loan_date || !loan.due_date) return 0
  const total = differenceInDays(new Date(loan.due_date), new Date(loan.loan_date))
  const remaining = loan.days_remaining
  if (remaining <= 0) return 100
  if (total <= 0) return 0
  return ((total - remaining) / total) * 100
}

const fetchData = async () => {
  isLoading.value = true
  try {
    const [activeRes, historyRes] = await Promise.all([
      loansApi.getMyActiveLoans(),
      loansApi.getMyLoans({ limit: 50 })
    ])
    
    activeLoans.value = activeRes.data
    loanHistory.value = historyRes.data
  } catch (error) {
    console.error('Error fetching loan data:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>