<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Приветствие -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">
        Панель администратора
      </h1>
      <p class="text-gray-600 mt-2">
        Управление системой, пользователями и мониторинг
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
              <p class="text-sm text-gray-500 mb-1">Пользователей</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalUsers }}</p>
            </div>
            <div class="bg-blue-100 p-3 rounded-full">
              <UsersIcon class="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            <span class="text-green-600">+{{ stats.newUsersToday }}</span> за сегодня
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Книг в каталоге</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalBooks }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-full">
              <BookOpenIcon class="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            <span class="text-green-600">+{{ stats.newBooksToday }}</span> за сегодня
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Активных выдач</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.activeLoans }}</p>
            </div>
            <div class="bg-yellow-100 p-3 rounded-full">
              <ClipboardDocumentListIcon class="h-6 w-6 text-yellow-600" />
            </div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            <span class="text-red-600">{{ stats.overdueLoans }}</span> просрочено
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">Экземпляров</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalCopies }}</p>
            </div>
            <div class="bg-purple-100 p-3 rounded-full">
              <CubeIcon class="h-6 w-6 text-purple-600" />
            </div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            Доступно: {{ stats.availableCopies }}
          </div>
        </div>
      </div>

      <!-- Быстрые действия -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <router-link
          to="/admin/users/create"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-blue-100 p-3 rounded-full group-hover:bg-blue-200 transition">
              <UserPlusIcon class="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Новый пользователь</h3>
              <p class="text-sm text-gray-500">Добавить читателя или библиотекаря</p>
            </div>
          </div>
        </router-link>

        <router-link
          to="/admin/books/create"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-green-100 p-3 rounded-full group-hover:bg-green-200 transition">
              <PlusIcon class="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Новая книга</h3>
              <p class="text-sm text-gray-500">Добавить книгу в каталог</p>
            </div>
          </div>
        </router-link>

        <router-link
          to="/admin/copies"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-yellow-100 p-3 rounded-full group-hover:bg-yellow-200 transition">
              <DocumentDuplicateIcon class="h-6 w-6 text-yellow-600" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Управление копиями</h3>
              <p class="text-sm text-gray-500">Добавить или переместить экземпляры</p>
            </div>
          </div>
        </router-link>

        <button
          @click="runDailyProcess"
          :disabled="isProcessing"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition group text-left disabled:opacity-50"
        >
          <div class="flex items-center gap-4">
            <div class="bg-red-100 p-3 rounded-full group-hover:bg-red-200 transition">
              <ArrowPathIcon class="h-6 w-6 text-red-600" :class="{ 'animate-spin': isProcessing }" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Ежедневная обработка</h3>
              <p class="text-sm text-gray-500">Обновить статусы просрочек</p>
            </div>
          </div>
        </button>
      </div>

      <!-- Графики и аналитика -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Популярные книги -->
        <div class="bg-white rounded-lg shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Популярные книги</h2>
          </div>
          <div class="p-6">
            <div v-if="popularBooks.length > 0" class="space-y-4">
              <div
                v-for="(book, index) in popularBooks"
                :key="book.book_id"
                class="flex items-center gap-4"
              >
                <span class="text-lg font-bold text-gray-400 w-6">#{{ index + 1 }}</span>
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{{ book.book_title }}</h3>
                  <p class="text-sm text-gray-500">Выдач: {{ book.loan_count }}</p>
                </div>
                <div class="w-24 h-2 bg-gray-200 rounded-full">
                  <div
                    class="h-2 bg-blue-600 rounded-full"
                    :style="{ width: (book.loan_count / maxPopularCount * 100) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4 text-gray-500">
              Нет данных
            </div>
          </div>
        </div>

        <!-- Активные пользователи -->
        <div class="bg-white rounded-lg shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Активные читатели</h2>
          </div>
          <div class="p-6">
            <div v-if="activeUsers.length > 0" class="space-y-4">
              <div
                v-for="(user, index) in activeUsers"
                :key="user.user_id"
                class="flex items-center gap-4"
              >
                <span class="text-lg font-bold text-gray-400 w-6">#{{ index + 1 }}</span>
                <div
                  class="h-8 w-8 rounded-full flex items-center justify-center text-white text-sm"
                  :class="getAvatarColor(user.user_name)"
                >
                  {{ getInitials({ first_name: user.user_name.split(' ')[1], last_name: user.user_name.split(' ')[0] }) }}
                </div>
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{{ user.user_name }}</h3>
                  <p class="text-sm text-gray-500">Книг взято: {{ user.loan_count }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4 text-gray-500">
              Нет данных
            </div>
          </div>
        </div>
      </div>

      <!-- Последние действия -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Последние действия</h2>
        </div>
        <div class="p-6">
          <div v-if="recentActivities.length > 0" class="space-y-4">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="flex items-start gap-4 border-b last:border-0 pb-4 last:pb-0"
            >
              <div
                :class="[
                  'p-2 rounded-full',
                  activity.type === 'loan' ? 'bg-green-100' :
                  activity.type === 'return' ? 'bg-blue-100' : 'bg-gray-100'
                ]"
              >
                <component
                  :is="activity.type === 'loan' ? 'ArrowRightIcon' : activity.type === 'return' ? 'ArrowLeftIcon' : 'PlusIcon'"
                  :class="[
                    'h-4 w-4',
                    activity.type === 'loan' ? 'text-green-600' :
                    activity.type === 'return' ? 'text-blue-600' : 'text-gray-600'
                  ]"
                />
              </div>
              <div class="flex-1">
                <p class="text-sm text-gray-900">{{ activity.description }}</p>
                <p class="text-xs text-gray-500">{{ formatRelativeDate(activity.created_at) }}</p>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500">
            Нет действий для отображения
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUIStore } from '@/stores/ui'
import { loansApi } from '@/api/loans'
import { usersApi } from '@/api/users'
import { booksApi } from '@/api/books'
import { copiesApi } from '@/api/copies'
import {
  UsersIcon,
  BookOpenIcon,
  ClipboardDocumentListIcon,
  CubeIcon,
  UserPlusIcon,
  PlusIcon,
  DocumentDuplicateIcon,
  ArrowPathIcon,
  ArrowRightIcon,
  ArrowLeftIcon
} from '@heroicons/vue/24/outline'
import { formatRelativeDate } from '@/utils/formatters'
import { getAvatarColor, getInitials } from '@/utils/helpers'

const uiStore = useUIStore()

const isLoading = ref(false)
const isProcessing = ref(false)
const stats = ref({
  totalUsers: 0,
  newUsersToday: 0,
  totalBooks: 0,
  newBooksToday: 0,
  activeLoans: 0,
  overdueLoans: 0,
  totalCopies: 0,
  availableCopies: 0
})
const popularBooks = ref([])
const activeUsers = ref([])
const recentActivities = ref([])

const maxPopularCount = ref(1)

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    // Получаем статистику из разных источников
    const [usersRes, booksRes, loansStats, copiesRes] = await Promise.all([
      usersApi.getAll({ limit: 1 }),
      booksApi.getAll({ limit: 1 }),
      loansApi.getStats(),
      copiesApi.getAll({ limit: 1 })
    ])

    // Получаем популярные книги из статистики
    const statsRes = loansStats.data
    popularBooks.value = statsRes.most_borrowed_books || []
    activeUsers.value = statsRes.most_active_users || []
    
    if (popularBooks.value.length > 0) {
      maxPopularCount.value = Math.max(...popularBooks.value.map(b => b.loan_count))
    }

    // Базовая статистика
    stats.value = {
      totalUsers: usersRes.headers?.['x-total-count'] || 0,
      newUsersToday: Math.floor(Math.random() * 10), // В реальном приложении брать из API
      totalBooks: booksRes.headers?.['x-total-count'] || 0,
      newBooksToday: Math.floor(Math.random() * 5),
      activeLoans: statsRes.total_active || 0,
      overdueLoans: statsRes.total_overdue || 0,
      totalCopies: copiesRes.headers?.['x-total-count'] || 0,
      availableCopies: Math.floor(Math.random() * 100) // В реальном приложении вычислять
    }

    // Последние действия (в реальном приложении брать из API логов)
    recentActivities.value = [
      {
        id: 1,
        type: 'loan',
        description: 'Иванов Иван взял книгу "Война и мир"',
        created_at: new Date(Date.now() - 1000 * 60 * 30)
      },
      {
        id: 2,
        type: 'return',
        description: 'Петров Петр вернул книгу "Преступление и наказание"',
        created_at: new Date(Date.now() - 1000 * 60 * 120)
      },
      {
        id: 3,
        type: 'user',
        description: 'Зарегистрирован новый пользователь: Сидоров Сидор',
        created_at: new Date(Date.now() - 1000 * 60 * 180)
      }
    ]
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

const runDailyProcess = async () => {
  if (isProcessing.value) return
  
  isProcessing.value = true
  try {
    const response = await loansApi.runDailyProcess()
    uiStore.success(`Обработано ${response.data.processed_count} просроченных выдач`)
    await fetchDashboardData()
  } catch (error) {
    console.error('Error running daily process:', error)
    uiStore.error('Ошибка при выполнении ежедневной обработки')
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>