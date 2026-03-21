<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <!-- Иконка -->
      <div class="flex justify-center mb-6">
        <div class="relative">
          <ShieldExclamationIcon class="h-32 w-32 text-red-500" />
        </div>
      </div>

      <!-- Заголовок -->
      <h1 class="text-3xl font-bold text-gray-900 mb-4">
        Доступ запрещен
      </h1>

      <!-- Описание -->
      <p class="text-lg text-gray-600 mb-8">
        У вас недостаточно прав для доступа к этой странице.
        Пожалуйста, войдите с соответствующей ролью.
      </p>

      <!-- Текущий пользователь -->
      <div v-if="auth.isAuthenticated" class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-center gap-3 mb-4">
          <div
            :class="[
              'h-12 w-12 rounded-full flex items-center justify-center text-white',
              getAvatarColor(getDisplayName(auth.user))
            ]"
          >
            {{ getInitials(auth.user) }}
          </div>
          <div class="text-left">
            <p class="font-medium text-gray-900">{{ getDisplayName(auth.user) }}</p>
            <p class="text-sm text-gray-500">{{ auth.user?.email }}</p>
          </div>
        </div>

        <div class="space-y-2">
          <p class="text-sm text-gray-600">Ваши роли:</p>
          <div class="flex flex-wrap gap-2 justify-center">
            <span
              v-for="role in auth.userRoles"
              :key="role.id"
              class="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs"
            >
              {{ role.name === 'reader' ? 'Читатель' : role.name === 'librarian' ? 'Библиотекарь' : 'Администратор' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Варианты действий -->
      <div class="space-y-4">
        <template v-if="!auth.isAuthenticated">
          <router-link
            to="/login"
            class="inline-flex items-center justify-center w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5 mr-2" />
            Войти в систему
          </router-link>
        </template>

        <template v-else>
          <router-link
            :to="dashboardRoute"
            class="inline-flex items-center justify-center w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <HomeIcon class="h-5 w-5 mr-2" />
            Перейти в личный кабинет
          </router-link>
        </template>

        <router-link
          to="/"
          class="inline-flex items-center justify-center w-full px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
        >
          <HomeIcon class="h-5 w-5 mr-2" />
          На главную
        </router-link>

        <button
          @click="goBack"
          class="inline-flex items-center justify-center w-full px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
        >
          <ArrowLeftIcon class="h-5 w-5 mr-2" />
          Вернуться назад
        </button>
      </div>

      <!-- Подсказка -->
      <div class="mt-8 p-4 bg-yellow-50 rounded-lg">
        <div class="flex items-start gap-3">
          <LightBulbIcon class="h-5 w-5 text-yellow-600 flex-shrink-0" />
          <p class="text-sm text-yellow-800 text-left">
            Если вы считаете, что это ошибка, обратитесь к администратору системы для получения соответствующих прав доступа.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  ShieldExclamationIcon,
  ArrowRightOnRectangleIcon,
  HomeIcon,
  ArrowLeftIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'
import { getAvatarColor, getInitials, getDisplayName } from '@/utils/helpers'

const router = useRouter()
const auth = useAuthStore()

const dashboardRoute = computed(() => {
  if (auth.isAdmin) return '/admin/dashboard'
  if (auth.isLibrarian) return '/librarian/dashboard'
  if (auth.isReader) return '/reader/dashboard'
  return '/'
})

const goBack = () => {
  router.go(-1)
}
</script>