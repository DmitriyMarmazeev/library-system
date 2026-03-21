<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Приветствие -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">
        Здравствуйте, {{ getDisplayName(user) }}!
      </h1>
      <p class="text-gray-600 mt-2">
        Добро пожаловать в ваш личный кабинет читателя
      </p>
    </div>

    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else>
      <!-- Статистика -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Книг на руках</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.activeLoans }}</p>
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
              <p class="text-2xl font-bold text-gray-900">{{ stats.overdueLoans }}</p>
            </div>
            <div class="bg-red-100 p-3 rounded-full">
              <ExclamationCircleIcon class="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Всего прочитано</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalLoans }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-full">
              <CheckCircleIcon class="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Можно взять</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.canBorrow }}</p>
            </div>
            <div class="bg-purple-100 p-3 rounded-full">
              <PlusIcon class="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Активные выдачи -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Активные выдачи</h2>
        </div>

        <div class="p-6">
          <div v-if="activeLoans.length > 0" class="space-y-4">
            <div
              v-for="loan in activeLoans"
              :key="loan.id"
              class="border rounded-lg p-4 hover:shadow-sm transition"
            >
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{{ loan.book_title }}</h3>
                  <p class="text-sm text-gray-500 mt-1">
                    Взята: {{ formatDate(loan.loan_date) }}
                  </p>
                </div>

                <div class="flex flex-col md:items-end">
                  <div class="flex items-center gap-3 mb-2">
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
                    <span class="text-sm text-gray-600">
                      Вернуть до: {{ formatDate(loan.due_date) }}
                    </span>
                  </div>
                  
                  <div class="flex items-center gap-2">
                    <div class="w-32 bg-gray-200 rounded-full h-2">
                      <div
                        :class="[
                          'h-2 rounded-full',
                          loan.is_overdue ? 'bg-red-500' : 'bg-green-500'
                        ]"
                        :style="{ width: loanProgress(loan) + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm text-gray-600">
                      {{ loan.days_remaining > 0 ? loan.days_remaining : Math.abs(loan.days_remaining) }}
                      {{ loan.days_remaining > 0 ? 'дн.' : 'дн. просрочки' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <BookOpenIcon class="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p class="text-gray-600">У вас нет книг на руках</p>
            <router-link
              to="/books"
              class="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Перейти к каталогу
            </router-link>
          </div>
        </div>
      </div>

      <!-- Рекомендации -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Рекомендуемые книги</h2>
        </div>

        <div class="p-6">
          <div v-if="recommendations.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              v-for="book in recommendations"
              :key="book.id"
              class="border rounded-lg p-4 hover:shadow-md transition"
            >
              <h3 class="font-medium text-gray-900 mb-2 line-clamp-2">{{ book.title }}</h3>
              <p class="text-sm text-gray-600 mb-3">
                {{ book.authors?.map(a => getDisplayName(a)).join(', ') || 'Автор не указан' }}
              </p>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">
                  Доступно: {{ book.available_copies || 0 }}
                </span>
                <router-link
                  :to="`/books/${book.id}`"
                  class="text-sm text-blue-600 hover:text-blue-800"
                >
                  Подробнее
                </router-link>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <p class="text-gray-600">Пока нет рекомендаций</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' // ЕДИНСТВЕННЫЙ импорт из vue
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { loansApi } from '@/api/loans'
import { booksApi } from '@/api/books'
import {
  BookOpenIcon,
  ExclamationCircleIcon,
  CheckCircleIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'
import { formatDate } from '@/utils/formatters'
import { getDisplayName } from '@/utils/helpers' // getDisplayName из helpers
import { differenceInDays } from 'date-fns'

const auth = useAuthStore()
const uiStore = useUIStore()

const isLoading = ref(false)
const activeLoans = ref([])
const loanHistory = ref([])
const recommendations = ref([])
const borrowStatus = ref(null)

const user = computed(() => auth.user)

const stats = computed(() => ({
  activeLoans: activeLoans.value.length,
  overdueLoans: activeLoans.value.filter(l => l.is_overdue).length,
  totalLoans: loanHistory.value.length,
  canBorrow: borrowStatus.value?.can_borrow ? 'Да' : 'Нет'
}))

const loanProgress = (loan) => {
  const total = differenceInDays(new Date(loan.due_date), new Date(loan.loan_date))
  const remaining = loan.days_remaining
  if (remaining <= 0) return 100
  return ((total - remaining) / total) * 100
}

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    const [activeRes, historyRes, statusRes, booksRes] = await Promise.all([
      loansApi.getMyActiveLoans(),
      loansApi.getMyLoans({ limit: 10 }),
      loansApi.getMyBorrowStatus(),
      booksApi.getAll({ limit: 3 })
    ])
    
    activeLoans.value = activeRes.data
    loanHistory.value = historyRes.data
    borrowStatus.value = statusRes.data
    recommendations.value = booksRes.data
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>