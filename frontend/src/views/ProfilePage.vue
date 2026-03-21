<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Профиль -->
    <div v-else-if="user" class="space-y-6">
      <!-- Шапка профиля -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
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
        </div>

        <!-- Информация -->
        <div class="p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                  <dd class="text-sm font-medium text-gray-900">{{ formatDate(user.created_at) }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Статус</dt>
                  <dd>
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
                  </dd>
                </div>
              </dl>
            </div>

            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Статистика</h3>
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm text-gray-500">Книг на руках</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ activeLoans.length }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Просрочено</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ overdueLoans.length }}</dd>
                </div>
                <div>
                  <dt class="text-sm text-gray-500">Всего прочитано</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ loanHistory.length }}</dd>
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
          <!-- Активные выдачи -->
          <div v-if="activeTab === 'active'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Книги на руках</h3>
            <div v-if="activeLoans.length > 0" class="space-y-4">
              <div
                v-for="loan in activeLoans"
                :key="loan.id"
                class="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-900">{{ loan.book_title }}</h4>
                    <p class="text-sm text-gray-500">Взята: {{ formatDate(loan.loan_date) }}</p>
                    <p class="text-sm text-gray-500">Вернуть до: {{ formatDate(loan.due_date) }}</p>
                  </div>
                  <div class="text-right">
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
                    <p class="text-sm mt-2">
                      Осталось дней: {{ loan.days_remaining }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8">
              <BookOpenIcon class="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <p class="text-gray-600">У вас нет книг на руках</p>
              <router-link to="/books" class="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block">
                Перейти к каталогу
              </router-link>
            </div>
          </div>

          <!-- История -->
          <div v-if="activeTab === 'history'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">История чтения</h3>
            <div v-if="loanHistory.length > 0" class="space-y-4">
              <div
                v-for="loan in loanHistory"
                :key="loan.id"
                class="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-900">{{ loan.book_title }}</h4>
                    <p class="text-sm text-gray-500">Взята: {{ formatDate(loan.loan_date) }}</p>
                    <p class="text-sm text-gray-500">Возвращена: {{ formatDate(loan.return_date) }}</p>
                  </div>
                  <span
                    class="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs"
                  >
                    {{ loan.status }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8">
              <ClockIcon class="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <p class="text-gray-600">История чтения пуста</p>
            </div>
          </div>

          <!-- Настройки -->
          <div v-if="activeTab === 'settings'">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Настройки профиля</h3>
            
            <form @submit.prevent="updateProfile" class="max-w-lg space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="input-field"
                  :disabled="!isEditing"
                />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
                  <input
                    v-model="profileForm.first_name"
                    type="text"
                    class="input-field"
                    :disabled="!isEditing"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
                  <input
                    v-model="profileForm.last_name"
                    type="text"
                    class="input-field"
                    :disabled="!isEditing"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Отчество</label>
                <input
                  v-model="profileForm.middle_name"
                  type="text"
                  class="input-field"
                  :disabled="!isEditing"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
                <input
                  v-model="profileForm.phone"
                  type="tel"
                  class="input-field"
                  :disabled="!isEditing"
                  placeholder="+7 (999) 999-99-99"
                />
              </div>

              <div class="flex gap-3">
                <button
                  v-if="!isEditing"
                  type="button"
                  @click="startEditing"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Редактировать
                </button>
                <template v-else>
                  <button
                    type="submit"
                    :disabled="isLoading"
                    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50"
                  >
                    Сохранить
                  </button>
                  <button
                    type="button"
                    @click="cancelEditing"
                    class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
                  >
                    Отмена
                  </button>
                </template>
              </div>
            </form>

            <div class="mt-8 pt-8 border-t">
              <h4 class="text-md font-medium text-gray-900 mb-4">Смена пароля</h4>
              <form @submit.prevent="changePassword" class="max-w-lg space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Текущий пароль</label>
                  <input
                    v-model="passwordForm.current_password"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Новый пароль</label>
                  <input
                    v-model="passwordForm.new_password"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Подтверждение пароля</label>
                  <input
                    v-model="passwordForm.new_password_confirm"
                    type="password"
                    class="input-field"
                    required
                  />
                </div>

                <button
                  type="submit"
                  :disabled="isPasswordLoading"
                  class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition disabled:opacity-50"
                >
                  Сменить пароль
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { usersApi } from '@/api/users'
import { loansApi } from '@/api/loans'
import { formatDate, formatPhone } from '@/utils/formatters'
import { getAvatarColor, getInitials, getDisplayName } from '@/utils/helpers'
import { BookOpenIcon, ClockIcon } from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const uiStore = useUIStore()

const user = ref(null)
const activeLoans = ref([])
const loanHistory = ref([])
const isLoading = ref(false)
const isPasswordLoading = ref(false)
const isEditing = ref(false)

const activeTab = ref('active')

const tabs = [
  { id: 'active', name: 'Книги на руках' },
  { id: 'history', name: 'История' },
  { id: 'settings', name: 'Настройки' }
]

const profileForm = reactive({
  email: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  phone: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  new_password_confirm: ''
})

const fetchUserData = async () => {
  isLoading.value = true
  try {
    const [userRes, activeRes, historyRes] = await Promise.all([
      usersApi.getMe(),
      loansApi.getMyActiveLoans(),
      loansApi.getMyLoans({ limit: 50 })
    ])
    
    user.value = userRes.data
    activeLoans.value = activeRes.data
    loanHistory.value = historyRes.data
    
    // Заполняем форму профиля
    profileForm.email = user.value.email
    profileForm.first_name = user.value.first_name
    profileForm.last_name = user.value.last_name
    profileForm.middle_name = user.value.middle_name || ''
    profileForm.phone = user.value.phone || ''
  } catch (error) {
    console.error('Error fetching user data:', error)
    uiStore.error('Ошибка загрузки данных')
  } finally {
    isLoading.value = false
  }
}

const startEditing = () => {
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
  // Восстанавливаем исходные значения
  profileForm.email = user.value.email
  profileForm.first_name = user.value.first_name
  profileForm.last_name = user.value.last_name
  profileForm.middle_name = user.value.middle_name || ''
  profileForm.phone = user.value.phone || ''
}

const updateProfile = async () => {
  isLoading.value = true
  try {
    const response = await usersApi.update(user.value.id, profileForm)
    user.value = response.data
    uiStore.success('Профиль успешно обновлен')
    isEditing.value = false
  } catch (error) {
    console.error('Error updating profile:', error)
    uiStore.error('Ошибка обновления профиля')
  } finally {
    isLoading.value = false
  }
}

const changePassword = async () => {
  if (passwordForm.new_password !== passwordForm.new_password_confirm) {
    uiStore.error('Пароли не совпадают')
    return
  }

  isPasswordLoading.value = true
  try {
    await usersApi.changePassword(user.value.id, passwordForm)
    uiStore.success('Пароль успешно изменен')
    
    // Очищаем форму
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password_confirm = ''
  } catch (error) {
    console.error('Error changing password:', error)
    uiStore.error(error.response?.data?.detail || 'Ошибка смены пароля')
  } finally {
    isPasswordLoading.value = false
  }
}

onMounted(() => {
  fetchUserData()
})
</script>