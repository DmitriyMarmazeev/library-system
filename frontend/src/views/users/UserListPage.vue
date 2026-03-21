<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Управление пользователями</h1>
        <p class="text-gray-600 mt-2">
          Список всех зарегистрированных пользователей системы
        </p>
      </div>
      <router-link
        to="/admin/users/create"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
      >
        <PlusIcon class="h-5 w-5" />
        Добавить пользователя
      </router-link>
    </div>

    <!-- Фильтры -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Поиск</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Имя, фамилия или email"
            class="input-field"
            @input="debouncedSearch"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Роль</label>
          <select
            v-model="filters.role"
            class="input-field"
            @change="search"
          >
            <option value="">Все роли</option>
            <option value="reader">Читатель</option>
            <option value="librarian">Библиотекарь</option>
            <option value="admin">Администратор</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
          <select
            v-model="filters.status"
            class="input-field"
            @change="search"
          >
            <option value="">Все</option>
            <option value="active">Активные</option>
            <option value="inactive">Заблокированные</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Дата регистрации</label>
          <input
            v-model="filters.registeredAfter"
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
          Найдено пользователей: {{ totalUsers }}
        </span>
      </div>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Всего пользователей</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
          </div>
          <div class="bg-blue-100 p-3 rounded-full">
            <UsersIcon class="h-6 w-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Читателей</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.readers }}</p>
          </div>
          <div class="bg-green-100 p-3 rounded-full">
            <UserIcon class="h-6 w-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Библиотекарей</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.librarians }}</p>
          </div>
          <div class="bg-yellow-100 p-3 rounded-full">
            <BookOpenIcon class="h-6 w-6 text-yellow-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 mb-1">Администраторов</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.admins }}</p>
          </div>
          <div class="bg-purple-100 p-3 rounded-full">
            <ShieldCheckIcon class="h-6 w-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица пользователей -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Пользователь
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Контакты
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Роли
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Статус
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Дата регистрации
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Активных выдач
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
            <tr v-else-if="users.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                Пользователи не найдены
              </td>
            </tr>
            <tr
              v-for="user in users"
              :key="user.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-3">
                  <div
                    :class="[
                      'h-10 w-10 rounded-full flex items-center justify-center text-white',
                      getAvatarColor(getDisplayName(user))
                    ]"
                  >
                    {{ getInitials(user) }}
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ getDisplayName(user) }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <div class="text-gray-900">{{ user.email }}</div>
                  <div class="text-gray-500">{{ formatPhone(user.phone) || '—' }}</div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="role in user.roles"
                    :key="role.id"
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="roleClasses[role.name]"
                  >
                    {{ role.name === 'reader' ? 'Читатель' : role.name === 'librarian' ? 'Библиотекарь' : 'Админ' }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    user.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ user.is_active ? 'Активен' : 'Заблокирован' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.active_loans || 0 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right space-x-2">
                <router-link
                  :to="`/admin/users/${user.id}`"
                  class="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  title="Просмотр"
                >
                  <EyeIcon class="h-5 w-5" />
                </router-link>
                <router-link
                  :to="`/admin/users/${user.id}/edit`"
                  class="text-yellow-600 hover:text-yellow-800 inline-flex items-center gap-1"
                  title="Редактировать"
                >
                  <PencilIcon class="h-5 w-5" />
                </router-link>
                <button
                  @click="toggleUserStatus(user)"
                  class="text-orange-600 hover:text-orange-800 inline-flex items-center gap-1"
                  :title="user.is_active ? 'Заблокировать' : 'Разблокировать'"
                >
                  <component
                    :is="user.is_active ? 'LockClosedIcon' : 'LockOpenIcon'"
                    class="h-5 w-5"
                  />
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
import {
  PlusIcon,
  EyeIcon,
  PencilIcon,
  LockClosedIcon,
  LockOpenIcon,
  UsersIcon,
  UserIcon,
  BookOpenIcon,
  ShieldCheckIcon
} from '@heroicons/vue/24/outline'
import { useUsersStore } from '@/stores/users'
import { useUIStore } from '@/stores/ui'
import { usePagination } from '@/composables/usePagination'
import { useFilters } from '@/composables/useFilters'
import { formatDate, formatPhone } from '@/utils/formatters'
import { getAvatarColor, getInitials, getDisplayName, debounce } from '@/utils/helpers'

const usersStore = useUsersStore()
const uiStore = useUIStore()

const users = ref([])
const isLoading = ref(false)
const totalUsers = ref(0)

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
    search: '',
    role: '',
    status: '',
    registeredAfter: ''
  },
  onFilterChange: (params) => {
    setPage(1)
    search(params)
  }
})

const roleClasses = {
  reader: 'bg-blue-100 text-blue-800',
  librarian: 'bg-green-100 text-green-800',
  admin: 'bg-purple-100 text-purple-800'
}

const stats = computed(() => {
  const stats = {
    total: users.value.length,
    readers: 0,
    librarians: 0,
    admins: 0
  }

  users.value.forEach(user => {
    user.roles.forEach(role => {
      if (role.name === 'reader') stats.readers++
      else if (role.name === 'librarian') stats.librarians++
      else if (role.name === 'admin') stats.admins++
    })
  })

  return stats
})

const search = async (searchParams = null) => {
  isLoading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * perPage.value,
      limit: perPage.value
    }
    
    const response = await usersStore.fetchUsers(params)
    let filtered = response

    // Применяем фильтры
    const filtersData = searchParams || filters.value
    
    if (filtersData.search) {
      const searchTerm = filtersData.search.toLowerCase()
      filtered = filtered.filter(user =>
        user.email.toLowerCase().includes(searchTerm) ||
        `${user.last_name} ${user.first_name}`.toLowerCase().includes(searchTerm)
      )
    }
    
    if (filtersData.role) {
      filtered = filtered.filter(user =>
        user.roles.some(r => r.name === filtersData.role)
      )
    }
    
    if (filtersData.status === 'active') {
      filtered = filtered.filter(user => user.is_active)
    } else if (filtersData.status === 'inactive') {
      filtered = filtered.filter(user => !user.is_active)
    }
    
    if (filtersData.registeredAfter) {
      const afterDate = new Date(filtersData.registeredAfter)
      filtered = filtered.filter(user =>
        new Date(user.created_at) >= afterDate
      )
    }

    users.value = filtered
    totalUsers.value = filtered.length
    setTotal(totalUsers.value)
  } catch (error) {
    console.error('Error fetching users:', error)
    uiStore.error('Ошибка загрузки пользователей')
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

const toggleUserStatus = async (user) => {
  try {
    await usersStore.toggleUserActive(user.id)
    uiStore.success(`Пользователь ${user.is_active ? 'заблокирован' : 'разблокирован'}`)
    await search()
  } catch (error) {
    console.error('Error toggling user status:', error)
    uiStore.error('Ошибка при изменении статуса')
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