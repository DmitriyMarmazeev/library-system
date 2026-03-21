<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Приветствие -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">
        Рабочее место библиотекаря
      </h1>
      <p class="text-gray-600 mt-2">
        Управление выдачами, каталогом и читателями
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
              <p class="text-sm text-gray-500 mb-1">Активные выдачи</p>
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
              <p class="text-sm text-gray-500 mb-1">Читателей</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalReaders }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-full">
              <UsersIcon class="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Книг в каталоге</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalBooks }}</p>
            </div>
            <div class="bg-purple-100 p-3 rounded-full">
              <CubeIcon class="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Быстрые действия -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <router-link
          to="/librarian/loans/create"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-green-100 p-3 rounded-full group-hover:bg-green-200 transition">
              <PlusIcon class="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Оформить выдачу</h3>
              <p class="text-sm text-gray-500">Выдать книгу читателю</p>
            </div>
          </div>
        </router-link>

        <router-link
          to="/librarian/loans/active"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-blue-100 p-3 rounded-full group-hover:bg-blue-200 transition">
              <ArrowPathIcon class="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Принять книгу</h3>
              <p class="text-sm text-gray-500">Оформить возврат</p>
            </div>
          </div>
        </router-link>

        <router-link
          to="/librarian/copies"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-yellow-100 p-3 rounded-full group-hover:bg-yellow-200 transition">
              <DocumentDuplicateIcon class="h-6 w-6 text-yellow-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Добавить экземпляры</h3>
              <p class="text-sm text-gray-500">Пополнить фонд</p>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Просроченные выдачи -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900">Просроченные выдачи</h2>
          <router-link
            to="/librarian/loans/overdue"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Все просроченные →
          </router-link>
        </div>

        <div class="p-6">
          <div v-if="overdueLoans.length > 0" class="space-y-4">
            <div
              v-for="loan in overdueLoans.slice(0, 5)"
              :key="loan.id"
              class="border rounded-lg p-4 hover:shadow-sm transition"
            >
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <h3 class="font-medium text-gray-900">{{ loan.book_title }}</h3>
                  <p class="text-sm text-gray-600">Читатель: {{ loan.user_name }}</p>
                  <p class="text-sm text-gray-500">
                    Должен был вернуть: {{ formatDate(loan.due_date) }}
                  </p>
                </div>
                <div class="flex items-center gap-3">
                  <span class="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs">
                    Просрочка {{ loan.days_overdue }} дн.
                  </span>
                  <button
                    @click="openReturnModal(loan)"
                    class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition text-sm"
                  >
                Принять
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <CheckCircleIcon class="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p class="text-gray-600">Просроченных выдач нет</p>
          </div>
        </div>
      </div>

      <!-- Последние выдачи -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900">Последние выдачи</h2>
          <router-link
            to="/librarian/loans/active"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Все выдачи →
          </router-link>
        </div>

        <div class="p-6">
          <div v-if="recentLoans.length > 0" class="space-y-4">
            <div
              v-for="loan in recentLoans"
              :key="loan.id"
              class="border rounded-lg p-4 hover:shadow-sm transition"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-medium text-gray-900">{{ loan.book_title }}</h3>
                  <p class="text-sm text-gray-600">Читатель: {{ loan.user_name }}</p>
                  <p class="text-sm text-gray-500">
                    Выдана: {{ formatDate(loan.loan_date) }}
                  </p>
                </div>
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
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <p class="text-gray-600">Нет активных выдач</p>
          </div>
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
        <p class="text-gray-700">
          <span class="font-medium">Просрочка:</span> {{ selectedLoan.days_overdue }} дней
        </p>

        <div class="mt-4">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { loansApi } from '@/api/loans'
import { booksApi } from '@/api/books'
import { usersApi } from '@/api/users'
import {
  BookOpenIcon,
  ExclamationCircleIcon,
  UsersIcon,
  CubeIcon,
  PlusIcon,
  ArrowPathIcon,
  DocumentDuplicateIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import AppModal from '@/components/ui/AppModal.vue'
import { formatDate } from '@/utils/formatters'

const router = useRouter()
const uiStore = useUIStore()

const isLoading = ref(false)
const stats = ref({
  activeLoans: 0,
  overdueLoans: 0,
  totalReaders: 0,
  totalBooks: 0
})
const overdueLoans = ref([])
const recentLoans = ref([])

const showReturnModal = ref(false)
const selectedLoan = ref(null)
const returnDate = ref(new Date().toISOString().split('T')[0])

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    const [activeRes, overdueRes, readersRes, booksRes] = await Promise.all([
      loansApi.getActive({ limit: 5 }),
      loansApi.getOverdue(),
      usersApi.getAll({ limit: 1 }),
      booksApi.getAll({ limit: 1 })
    ])
    
    recentLoans.value = activeRes.data
    overdueLoans.value = overdueRes.data
    
    // Получаем статистику
    const [statsRes] = await Promise.all([
      loansApi.getStats()
    ])
    
    stats.value = {
      activeLoans: statsRes.data.total_active,
      overdueLoans: statsRes.data.total_overdue,
      totalReaders: readersRes.headers?.['x-total-count'] || 0,
      totalBooks: booksRes.headers?.['x-total-count'] || 0
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
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
    await loansApi.return(selectedLoan.value.id, {
      return_date: returnDate.value
    })
    
    uiStore.success('Книга успешно возвращена')
    showReturnModal.value = false
    await fetchDashboardData()
  } catch (error) {
    console.error('Error returning book:', error)
    uiStore.error('Ошибка при возврате книги')
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>