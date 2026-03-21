<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Редактирование пользователя</h1>
      <p class="text-gray-600 mt-2">
        Изменение информации о пользователе
      </p>
    </div>

    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Форма -->
    <div v-else-if="user" class="bg-white rounded-lg shadow-sm p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Email <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.email"
            type="email"
            class="input-field"
            :class="{ 'border-red-500': errors.email }"
            placeholder="user@example.com"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
        </div>

        <!-- Имя и фамилия -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Имя <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.first_name"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.first_name }"
              placeholder="Иван"
            />
            <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Фамилия <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.last_name"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.last_name }"
              placeholder="Иванов"
            />
            <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name }}</p>
          </div>
        </div>

        <!-- Отчество -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Отчество
          </label>
          <input
            v-model="form.middle_name"
            type="text"
            class="input-field"
            placeholder="Иванович"
          />
        </div>

        <!-- Телефон -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Телефон
          </label>
          <input
            v-model="form.phone"
            type="tel"
            class="input-field"
            :class="{ 'border-red-500': errors.phone }"
            placeholder="+7 (999) 999-99-99"
          />
          <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone }}</p>
        </div>

        <!-- Роли -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Роли <span class="text-red-500">*</span>
          </label>
          <div class="space-y-2">
            <div
              v-for="role in availableRoles"
              :key="role.id"
              class="flex items-center gap-2"
            >
              <input
                :id="`role-${role.id}`"
                type="checkbox"
                :value="role.id"
                v-model="form.role_ids"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label :for="`role-${role.id}`" class="text-sm text-gray-700">
                {{ role.name === 'reader' ? 'Читатель' : role.name === 'librarian' ? 'Библиотекарь' : 'Администратор' }}
                <span class="text-gray-500 text-xs ml-2">{{ role.description }}</span>
              </label>
            </div>
          </div>
          <p v-if="errors.role_ids" class="mt-1 text-sm text-red-600">{{ errors.role_ids }}</p>
        </div>

        <!-- Статус -->
        <div>
          <label class="flex items-center gap-2">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Активен (может входить в систему)</span>
          </label>
        </div>

        <!-- Кнопки -->
        <div class="flex justify-end gap-4 pt-4">
          <router-link
            :to="`/admin/users/${userId}`"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
          >
            Отмена
          </router-link>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsersStore } from '@/stores/users'
import { useUIStore } from '@/stores/ui'
import { userSchema } from '@/utils/validators'
import * as yup from 'yup'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const uiStore = useUIStore()

const userId = parseInt(route.params.id)
const user = ref(null)
const availableRoles = ref([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const errors = ref({})

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  phone: '',
  role_ids: [],
  is_active: true
})

const fetchUser = async () => {
  isLoading.value = true
  try {
    user.value = await usersStore.fetchUserById(userId)
    
    // Заполняем форму
    form.email = user.value.email
    form.first_name = user.value.first_name
    form.last_name = user.value.last_name
    form.middle_name = user.value.middle_name || ''
    form.phone = user.value.phone || ''
    form.role_ids = user.value.roles.map(r => r.id)
    form.is_active = user.value.is_active
  } catch (error) {
    console.error('Error fetching user:', error)
    uiStore.error('Ошибка загрузки данных пользователя')
    router.push('/admin/users')
  } finally {
    isLoading.value = false
  }
}

const fetchRoles = async () => {
  try {
    availableRoles.value = await usersStore.fetchRoles()
  } catch (error) {
    console.error('Error fetching roles:', error)
    uiStore.error('Ошибка загрузки списка ролей')
  }
}

const handleSubmit = async () => {
  try {
    errors.value = {}

    // Валидация
    await userSchema.validate(form, { abortEarly: false })
    
    if (form.role_ids.length === 0) {
      errors.value.role_ids = 'Выберите хотя бы одну роль'
      return
    }

    isSubmitting.value = true

    // Подготавливаем данные для отправки
    const userData = {
      ...form,
      role_ids: form.role_ids
    }

    await usersStore.updateUser(userId, userData)
    uiStore.success('Пользователь успешно обновлен')
    router.push(`/admin/users/${userId}`)
  } catch (err) {
    if (err instanceof yup.ValidationError) {
      const validationErrors = {}
      err.inner.forEach((error) => {
        validationErrors[error.path] = error.message
      })
      errors.value = validationErrors
    } else {
      console.error('Error updating user:', err)
      uiStore.error(err.response?.data?.detail || 'Ошибка при обновлении пользователя')
    }
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchRoles()
  fetchUser()
})
</script>