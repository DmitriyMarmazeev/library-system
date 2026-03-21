<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Шапка для публичных страниц -->
    <header class="bg-white shadow-sm">
      <div class="mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between items-center">
          <!-- Логотип -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center gap-2 text-xl font-bold text-gray-900">
              <BookOpenIcon class="h-6 w-6 text-blue-600" />
              <span>LibraryMS</span>
            </router-link>
          </div>

          <!-- Навигация -->
          <nav class="hidden md:flex items-center space-x-8">
            <router-link
              to="/books"
              class="text-gray-700 hover:text-gray-900"
              :class="{ 'text-blue-600 font-medium': $route.path === '/books' }"
            >
              Книги
            </router-link>
            <router-link
              to="/authors"
              class="text-gray-700 hover:text-gray-900"
              :class="{ 'text-blue-600 font-medium': $route.path === '/authors' }"
            >
              Авторы
            </router-link>
            <router-link
              to="/genres"
              class="text-gray-700 hover:text-gray-900"
              :class="{ 'text-blue-600 font-medium': $route.path === '/genres' }"
            >
              Жанры
            </router-link>
            <router-link
              to="/about"
              class="text-gray-700 hover:text-gray-900"
              :class="{ 'text-blue-600 font-medium': $route.path === '/about' }"
            >
              О проекте
            </router-link>
          </nav>

          <!-- Кнопки авторизации -->
          <div class="flex items-center gap-4">
            <template v-if="!auth.isAuthenticated">
              <router-link
                to="/login"
                class="text-gray-700 hover:text-gray-900"
              >
                Войти
              </router-link>
              <router-link
                to="/register"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                Регистрация
              </router-link>
            </template>
            <template v-else>
              <router-link
                :to="dashboardRoute"
                class="flex items-center gap-2 text-gray-700 hover:text-gray-900"
              >
                <UserIcon class="h-5 w-5" />
                <span>Личный кабинет</span>
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Основной контент -->
    <main>
      <router-view />
    </main>

    <!-- Футер -->
    <footer class="bg-white mt-12 border-t">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              LibraryMS
            </h3>
            <p class="mt-4 text-sm text-gray-500">
              Современная система управления библиотекой с открытым доступом к каталогу.
            </p>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Каталог
            </h3>
            <ul class="mt-4 space-y-2">
              <li>
                <router-link to="/books" class="text-sm text-gray-500 hover:text-gray-900">
                  Все книги
                </router-link>
              </li>
              <li>
                <router-link to="/authors" class="text-sm text-gray-500 hover:text-gray-900">
                  Авторы
                </router-link>
              </li>
              <li>
                <router-link to="/genres" class="text-sm text-gray-500 hover:text-gray-900">
                  Жанры
                </router-link>
              </li>
            </ul>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Информация
            </h3>
            <ul class="mt-4 space-y-2">
              <li>
                <router-link to="/about" class="text-sm text-gray-500 hover:text-gray-900">
                  О проекте
                </router-link>
              </li>
              <li>
                <a href="#" class="text-sm text-gray-500 hover:text-gray-900">
                  Правила пользования
                </a>
              </li>
              <li>
                <a href="#" class="text-sm text-gray-500 hover:text-gray-900">
                  Контакты
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Контакты
            </h3>
            <ul class="mt-4 space-y-2">
              <li class="flex items-center gap-2 text-sm text-gray-500">
                <EnvelopeIcon class="h-4 w-4" />
                <a href="mailto:info@libraryms.ru" class="hover:text-gray-900">
                  info@libraryms.ru
                </a>
              </li>
              <li class="flex items-center gap-2 text-sm text-gray-500">
                <PhoneIcon class="h-4 w-4" />
                <a href="tel:+78001234567" class="hover:text-gray-900">
                  8 (800) 123-45-67
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="mt-8 border-t pt-8 text-center text-sm text-gray-500">
          <p>&copy; {{ new Date().getFullYear() }} Library Management System. Все права защищены.</p>
        </div>
      </div>
    </footer>

    <!-- Глобальные уведомления -->
    <div class="fixed bottom-4 right-4 z-50 space-y-2">
      <TransitionGroup
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform translate-x-full opacity-0"
        enter-to-class="transform translate-x-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform translate-x-0 opacity-100"
        leave-to-class="transform translate-x-full opacity-0"
      >
        <div
          v-for="notification in uiStore.notifications"
          :key="notification.id"
          :class="[
            'w-80 rounded-lg shadow-lg p-4',
            notificationClasses[notification.type]
          ]"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-start gap-3">
              <component
                :is="notificationIcons[notification.type]"
                class="h-5 w-5 flex-shrink-0"
              />
              <div>
                <p class="text-sm font-medium">{{ notification.message }}</p>
                <p v-if="notification.description" class="text-xs mt-1 opacity-75">
                  {{ notification.description }}
                </p>
              </div>
            </div>
            <button
              @click="uiStore.removeNotification(notification.id)"
              class="ml-4 flex-shrink-0"
            >
              <XMarkIcon class="h-4 w-4" />
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import {
  BookOpenIcon,
  UserIcon,
  EnvelopeIcon,
  PhoneIcon,
  XMarkIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const uiStore = useUIStore()

const dashboardRoute = computed(() => {
  if (auth.isAdmin) return '/admin/dashboard'
  if (auth.isLibrarian) return '/librarian/dashboard'
  if (auth.isReader) return '/reader/dashboard'
  return '/'
})

const notificationIcons = {
  success: CheckCircleIcon,
  error: XCircleIcon,
  warning: ExclamationCircleIcon,
  info: InformationCircleIcon
}

const notificationClasses = {
  success: 'bg-green-50 text-green-800 border border-green-200',
  error: 'bg-red-50 text-red-800 border border-red-200',
  warning: 'bg-yellow-50 text-yellow-800 border border-yellow-200',
  info: 'bg-blue-50 text-blue-800 border border-blue-200'
}
</script>