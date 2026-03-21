<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-center py-12">
      <ExclamationCircleIcon class="h-16 w-16 text-red-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Ошибка загрузки</h3>
      <p class="text-gray-600">{{ error }}</p>
      <router-link to="/admin/users" class="mt-4 inline-block text-blue-600 hover:text-blue-800">
        ← Вернуться к списку
      </router-link>
    </div>

    <!-- Детали пользователя -->
    <div v-else-if="user" class="space-y-6">
      <!-- Шапка профиля -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
          <div class="flex justify-between items-start">
            <div class="flex items-center gap-6">
              <div
                :class="[
                  'h-20 w-20 rounded-full flex items-center justify-center text-white text-2xl font-bold',
                  getAvatarColor(getDisplayName(user))
                ]"
              >
                {{ getInitials(user) }}
              </div>
              <div>
                <h1 class="text-2xl font-bold text-white mb-2">
                  {{ getDisplayName(user) }}
                </h1>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="role in user.roles"
                    :key="role.id"
                    class="px-2 py-1 bg-white bg-opacity-20 text-white rounded-full text-xs"
                  >
                    {{ role.name === 'reader' ? 'Читатель' : role.name === 'librarian' ? 'Библиотекарь' : 'Администратор' }}
                  </span>
                </div>
              </div>
            </div>
            <div class="flex gap-2">
              <router-link
                :to="`/admin/users/${user.id}/edit`"
                class="bg-white text-yellow-600 px-4 py-2 rounded-lg hover:bg-gray-100 transition flex items-center gap-2"
              >
                <PencilIcon class="h-5 w-5" />
                Редактировать
              </router-link>
              <button
                @click="toggleUserStatus"
                :class="[
                  'px-4 py-2 rounded-lg transition flex items-center gap-2',
                  user.is_active
                    ? 'bg-orange-500 text-white hover:bg-orange-600'
                    : 'bg-green-500 text-white hover:bg-green-600'
                ]"
              >
                <component
                  :is="user.is_active ? 'LockClosedIcon' : 'LockOpenIcon'"
                  class="h-5 w-5"
                />
                {{ user.is_active ? 'Заблокировать' : 'Разблокировать' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Основная информация -->
        <div class="p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Левая колонка -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Контактная информация</h3>
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm text-gray-500">Email</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ user.email }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Телефон</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ formatPhone(user.phone) || 'Не указан' }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Дата регистрации</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ formatDateTime(user.created_at) }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Последнее обновление</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ formatDateTime(user.updated_at) || '—' }}</dd>
                </div>
              </dl>
            </div>

            <!-- Правая колонка -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Статистика</h3>
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm text-gray-500">Текущие выдачи</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ loanStats.active }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Просрочено</dt>
                  <dd class="text-sm font-medium" :class="{ 'text-red-600': loanStats.overdue > 0 }">
                    {{ loanStats.overdue }}
                  </dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Всего выдач</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ loanStats.total }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Возвращено</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ loanStats.returned }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Вкладки -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'px-6 py-3 text-sm font-medium border-b-2 transition',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- Текущие выдачи -->
          <div v-if="activeTab === 'active'">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Активные выдачи</h3>
              <router-link
                :to="`/librarian/loans/create?user=${user.id}`"
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Оформить выдачу →
              </router-link>
            </div>

            <div v-if="activeLoans.length > 0" class="space-y-4">
              <div
                v-for="loan in activeLoans"
                :key="loan.id"
                class="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-900">{{ loan.book_title }}</h4>
                    <p class="text-sm text-gray-500 mt-1">Выдана: {{ formatDate(loan.loan_date) }}</p>
                    <p class="text-sm text-gray-500">Вернуть до: {{ formatDate(loan.due_date) }}</p>
                  </div>
                  <div class="flex flex-col items-end gap-2">
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
                    <span class="text-sm text-gray-500">
                      Осталось дней: {{ loan.days_remaining }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              У пользователя нет активных выдач
            </div>
          </div>

          <!-- История выдач -->
          <div v-if="activeTab === 'history'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">История выдач</h3>
            
            <div v-if="loanHistory.length > 0" class="space-y-4">
              <div
                v-for="loan in loanHistory"
                :key="loan.id"
                class="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-900">{{ loan.book_title }}</h4>
                    <p class="text-sm text-gray-500">Выдана: {{ formatDate(loan.loan_date) }}</p>
                    <p v-if="loan.return_date" class="text-sm text-gray-500">
                      Возвращена: {{ formatDate(loan.return_date) }}
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
          </div>

          <!-- Управление ролями -->
          <div v-if="activeTab === 'roles'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Управление ролями</h3>
            
            <div class="space-y-4">
              <div
                v-for="role in allRoles"
                :key="role.id"
                class="flex items-center justify-between p-4 border rounded-lg"
              >
                <div>
                  <h4 class="font-medium text-gray-900">
                    {{ role.name === 'reader' ? 'Читатель' : role.name === 'librarian' ? 'Библиотекарь' : 'Администратор' }}
                  </h4>
                  <p class="text-sm text-gray-500">{{ role.description }}</p>
                </div>
                <button
                  @click="toggleRole(role)"
                  :class="[
                    'px-3 py-1 rounded-lg text-sm font-medium transition',
                    hasRole(role.name)
                      ? 'bg-red-100 text-red-700 hover:bg-red-200'
                      : 'bg-green-100 text-green-700 hover:bg-green-200'
                  ]"
                >
                  {{ hasRole(role.name) ? 'Удалить' : 'Добавить' }}
                </button>
              </div>

              <div class="mt-4 p-4 bg-yellow-50 rounded-lg">
                <div class="flex items-start gap-3">
                  <ExclamationCircleIcon class="h-5 w-5 text-yellow-600 flex-shrink-0" />
                  <p class="text-sm text-yellow-700">
                    Изменение ролей влияет на права доступа пользователя. Будьте внимательны.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  PencilIcon,
  LockClosedIcon,
  LockOpenIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/24/outline'
import { useUsersStore } from '@/stores/users'
import { useLoansStore } from '@/stores/loans'
import { useUIStore } from '@/stores/ui'
import { formatDate, formatDateTime, formatPhone } from '@/utils/formatters'
import { getAvatarColor, getInitials, getDisplayName } from '@/utils/helpers'
import { LOAN_STATUS_COLORS, LOAN_STATUS_LABELS } from '@/utils/constants'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const loansStore = useLoansStore()
const uiStore = useUIStore()

const userId = parseInt(route.params.id)
const user = ref(null)
const allRoles = ref([])
const activeLoans = ref([])
const loanHistory = ref([])
const loanStats = ref({ active: 0, overdue: 0, total: 0, returned: 0 })
const isLoading = ref(false)
const error = ref('')

const activeTab = ref('active')

const tabs = [
  { id: 'active', name: 'Текущие выдачи' },
  { id: 'history', name: 'История' },
  { id: 'roles', name: 'Роли' }
]

const hasRole = (roleName) => {
  return user.value?.roles?.some(r => r.name === roleName) || false
}

const fetchUserData = async () => {
  isLoading.value = true
  error.value = ''

  try {
    // Загружаем пользователя и роли
    const [userData, rolesData, activeLoansData, historyData] = await Promise.all([
      usersStore.fetchUserById(userId),
      usersStore.fetchRoles(),
      loansStore.fetchUserLoans(userId, { status: 'active' }),
      loansStore.fetchUserLoans(userId, { limit: 50 })
    ])

    user.value = userData
    allRoles.value = rolesData
    activeLoans.value = activeLoansData

    // Фильтруем историю
    loanHistory.value = historyData.filter(l => l.status !== 'active')
    
    // Считаем статистику
    loanStats.value = {
      active: activeLoansData.length,
      overdue: activeLoansData.filter(l => l.is_overdue).length,
      total: historyData.length,
      returned: historyData.filter(l => l.status === 'returned').length
    }
  } catch (err) {
    console.error('Error fetching user data:', err)
    error.value = 'Ошибка загрузки данных пользователя'
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

const toggleUserStatus = async () => {
  try {
    await usersStore.toggleUserActive(userId)
    user.value.is_active = !user.value.is_active
    uiStore.success(`Пользователь ${user.value.is_active ? 'разблокирован' : 'заблокирован'}`)
  } catch (err) {
    console.error('Error toggling user status:', err)
    uiStore.error('Ошибка при изменении статуса')
  }
}

const toggleRole = async (role) => {
  const hasRole = user.value.roles.some(r => r.id === role.id)

  try {
    if (hasRole) {
      await usersStore.removeRole(userId, role.name)
      user.value.roles = user.value.roles.filter(r => r.id !== role.id)
      uiStore.success(`Роль "${role.name}" удалена`)
    } else {
      await usersStore.addRole(userId, role.name)
      user.value.roles.push(role)
      uiStore.success(`Роль "${role.name}" добавлена`)
    }
  } catch (err) {
    console.error('Error toggling role:', err)
    uiStore.error('Ошибка при изменении роли')
  }
}

onMounted(() => {
  fetchUserData()
})
</script>