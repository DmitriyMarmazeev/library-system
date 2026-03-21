<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between items-center">
          <!-- Левая часть: логотип и бургер-меню -->
          <div class="flex items-center">
            <button
              @click="uiStore.toggleSidebar"
              class="text-gray-500 hover:text-gray-700 lg:hidden"
            >
              <Bars3Icon class="h-6 w-6" />
            </button>
            <div class="ml-4 lg:ml-0">
              <router-link to="/" class="text-xl font-bold text-gray-900">
                LibraryMS
              </router-link>
            </div>
          </div>

          <!-- Правая часть: уведомления и профиль -->
          <div class="flex items-center gap-4">
            <!-- Уведомления -->
            <button
              @click="showNotifications = !showNotifications"
              class="relative text-gray-500 hover:text-gray-700"
            >
              <BellIcon class="h-6 w-6" />
              <span
                v-if="uiStore.notifications.length"
                class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center"
              >
                {{ uiStore.notifications.length }}
              </span>
            </button>

            <!-- Профиль -->
            <Menu as="div" class="relative">
              <MenuButton class="flex items-center gap-2 hover:opacity-80">
                <div
                  v-if="auth.user"
                  :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-white',
                    getAvatarColor(getDisplayName(auth.user))
                  ]"
                >
                  {{ getInitials(auth.user) }}
                </div>
                <div v-else class="h-8 w-8 rounded-full bg-gray-300 animate-pulse"></div>
                <span class="hidden md:block text-sm font-medium text-gray-700">
                  {{ auth.user ? getDisplayName(auth.user) : 'Загрузка...' }}
                </span>
                <ChevronDownIcon class="h-4 w-4 text-gray-500" />
              </MenuButton>

              <transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0"
              >
                <MenuItems
                  class="absolute right-0 mt-2 w-48 origin-top-right bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <MenuItem v-slot="{ active }">
                    <router-link
                      to="/profile"
                      :class="[
                        active ? 'bg-gray-100' : '',
                        'block px-4 py-2 text-sm text-gray-700'
                      ]"
                    >
                      <UserIcon class="h-4 w-4 inline mr-2" />
                      Профиль
                    </router-link>
                  </MenuItem>
                  <MenuItem v-slot="{ active }">
                    <button
                      @click="auth.logout"
                      :class="[
                        active ? 'bg-gray-100' : '',
                        'block w-full text-left px-4 py-2 text-sm text-gray-700'
                      ]"
                    >
                      <ArrowRightOnRectangleIcon class="h-4 w-4 inline mr-2" />
                      Выйти
                    </button>
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>
    </header>

    <!-- Основной контент с сайдбаром -->
    <div class="flex">
      <!-- Sidebar -->
      <aside
        :class="[
          'fixed inset-y-0 left-0 z-40 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:static lg:translate-x-0',
          uiStore.sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <div class="h-16 flex items-center justify-between px-4 border-b lg:hidden">
          <span class="font-semibold">Меню</span>
          <button @click="uiStore.toggleSidebar" class="text-gray-500 hover:text-gray-700">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>

        <nav class="p-4">
          <ul class="space-y-2">
            <!-- Публичные разделы -->
            <li>
              <router-link
                to="/books"
                class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                :class="{ 'bg-gray-100': $route.path.startsWith('/books') }"
              >
                <BookOpenIcon class="h-5 w-5" />
                <span>Книги</span>
              </router-link>
            </li>

            <!-- Разделы для авторизованных пользователей -->
            <template v-if="auth.isAuthenticated">
              <!-- Читатель -->
              <template v-if="auth.isReader">
                <li>
                  <router-link
                    to="/reader/dashboard"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                    :class="{ 'bg-gray-100': $route.path.startsWith('/reader/dashboard') }"
                  >
                    <HomeIcon class="h-5 w-5" />
                    <span>Мой профиль</span>
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/reader/books"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                    :class="{ 'bg-gray-100': $route.path === '/reader/books' }"
                  >
                    <BookOpenIcon class="h-5 w-5" />
                    <span>Мои книги</span>
                  </router-link>
                </li>
              </template>

              <!-- Библиотекарь -->
              <template v-if="auth.isLibrarian">
                <li class="pt-4">
                  <div class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Библиотекарь
                  </div>
                </li>
                <li>
                  <router-link
                    to="/librarian/dashboard"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <ChartBarIcon class="h-5 w-5" />
                    <span>Дашборд</span>
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/librarian/loans/active"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <ClipboardDocumentListIcon class="h-5 w-5" />
                    <span>Выдачи</span>
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/librarian/copies"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <CubeIcon class="h-5 w-5" />
                    <span>Экземпляры</span>
                  </router-link>
                </li>
              </template>

              <!-- Администратор -->
              <template v-if="auth.isAdmin">
                <li class="pt-4">
                  <div class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Администрирование
                  </div>
                </li>
                <li>
                  <router-link
                    to="/admin/users"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <UsersIcon class="h-5 w-5" />
                    <span>Пользователи</span>
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/admin/roles"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <ShieldCheckIcon class="h-5 w-5" />
                    <span>Роли</span>
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/admin/stats"
                    class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    <ChartPieIcon class="h-5 w-5" />
                    <span>Статистика</span>
                  </router-link>
                </li>
              </template>
            </template>

            <!-- Неавторизованные пользователи -->
            <template v-else>
              <li class="pt-4">
                <router-link
                  to="/login"
                  class="flex items-center gap-3 px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <ArrowRightOnRectangleIcon class="h-5 w-5" />
                  <span>Войти</span>
                </router-link>
              </li>
            </template>
          </ul>
        </nav>
      </aside>

      <!-- Оверлей для мобильного меню -->
      <div
        v-if="uiStore.sidebarOpen"
        @click="uiStore.toggleSidebar"
        class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
      ></div>

      <!-- Основной контент -->
      <main class="flex-1 p-6">
        <router-view />
      </main>
    </div>

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
import { ref, computed } from 'vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  Bars3Icon,
  XMarkIcon,
  BellIcon,
  ChevronDownIcon,
  BookOpenIcon,
  HomeIcon,
  ClockIcon,
  ChartBarIcon,
  ClipboardDocumentListIcon,
  CubeIcon,
  UsersIcon,
  ShieldCheckIcon,
  ChartPieIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'

import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { getAvatarColor, getInitials, getDisplayName } from '@/utils/helpers'

const auth = useAuthStore()
const uiStore = useUIStore()
const showNotifications = ref(false)

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