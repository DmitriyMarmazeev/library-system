<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Регистрация</h2>
    <p class="text-gray-600 mb-6">Создайте аккаунт для доступа к библиотеке</p>

    <form @submit.prevent="handleSubmit" class="space-y-4">
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
          placeholder="your@email.com"
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
          />
          <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name }}</p>
        </div>
      </div>

      <!-- Отчество (опционально) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Отчество
        </label>
        <input
          v-model="form.middle_name"
          type="text"
          class="input-field"
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

      <!-- Пароль -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Пароль <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.password"
          type="password"
          class="input-field"
          :class="{ 'border-red-500': errors.password }"
        />
        <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
      </div>

      <!-- Подтверждение пароля -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Подтверждение пароля <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.password_confirm"
          type="password"
          class="input-field"
          :class="{ 'border-red-500': errors.password_confirm }"
        />
        <p v-if="errors.password_confirm" class="mt-1 text-sm text-red-600">{{ errors.password_confirm }}</p>
      </div>

      <!-- Кнопка регистрации -->
      <button
        type="submit"
        :disabled="isLoading"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        <span v-if="isLoading">Регистрация...</span>
        <span v-else>Зарегистрироваться</span>
      </button>

      <!-- Ошибка -->
      <div v-if="error" class="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
        {{ error }}
      </div>
    </form>

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        Уже есть аккаунт?
        <router-link to="/login/reader" class="text-blue-600 hover:text-blue-800 font-medium">
          Войти
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { registerSchema } from '@/utils/validators'
import * as yup from 'yup'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const isLoading = ref(false)
const error = ref('')
const errors = ref({})

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  phone: '',
  password: '',
  password_confirm: ''
})

const handleSubmit = async () => {
  try {
    errors.value = {}
    error.value = ''

    // Валидация
    await registerSchema.validate(form, { abortEarly: false })
    
    isLoading.value = true
    
    await authStore.register(form)
    uiStore.success('Регистрация прошла успешно!')
    router.push('/reader/dashboard')
  } catch (err) {
    if (err instanceof yup.ValidationError) {
      const validationErrors = {}
      err.inner.forEach((error) => {
        validationErrors[error.path] = error.message
      })
      errors.value = validationErrors
    } else {
      error.value = err.response?.data?.detail || 'Ошибка регистрации'
    }
  } finally {
    isLoading.value = false
  }
}
</script>