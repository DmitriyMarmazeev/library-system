<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <!-- Email -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Email
      </label>
      <input
        v-model="form.email"
        type="email"
        class="input-field"
        :class="{ 'border-red-500': errors.email }"
        placeholder="your@email.com"
        required
      />
      <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
    </div>

    <!-- Пароль -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Пароль
      </label>
      <input
        v-model="form.password"
        type="password"
        class="input-field"
        :class="{ 'border-red-500': errors.password }"
        placeholder="••••••••"
        required
      />
      <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
    </div>

    <!-- Кнопка входа -->
    <button
      type="submit"
      :disabled="isLoading"
      class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
    >
      <span v-if="isLoading">Вход...</span>
      <span v-else>Войти</span>
    </button>

    <!-- Ошибка -->
    <div v-if="error" class="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { loginSchema } from '@/utils/validators'
import * as yup from 'yup'

const props = defineProps({
  role: {
    type: String,
    required: true,
    validator: (value) => ['reader', 'librarian', 'admin'].includes(value)
  }
})

const authStore = useAuthStore()
const uiStore = useUIStore()

const isLoading = ref(false)
const error = ref('')
const errors = ref({})

const form = reactive({
  email: '',
  password: ''
})

const handleSubmit = async () => {
  try {
    errors.value = {}
    error.value = ''

    // Валидация
    await loginSchema.validate(form, { abortEarly: false })
    
    isLoading.value = true
    
    await authStore.login(form, props.role)
    uiStore.success('Вход выполнен успешно!')
  } catch (err) {
    if (err instanceof yup.ValidationError) {
      const validationErrors = {}
      err.inner.forEach((error) => {
        validationErrors[error.path] = error.message
      })
      errors.value = validationErrors
    } else {
      error.value = err.response?.data?.detail || 'Ошибка входа'
    }
  } finally {
    isLoading.value = false
  }
}
</script>