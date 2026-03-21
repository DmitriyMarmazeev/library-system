<template>
  <div class="text-center">
    <h2 class="text-3xl font-bold text-gray-900 mb-4">Вход в систему</h2>
    <p class="text-gray-600 mb-8">Выберите роль для входа</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Читатель -->
      <router-link
        to="/login/reader"
        class="group p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition border-2 border-transparent hover:border-blue-500"
      >
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-500 transition">
            <UserIcon class="h-8 w-8 text-blue-600 group-hover:text-white transition" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Читатель</h3>
          <p class="text-sm text-gray-600">
            Поиск книг, бронирование, личный кабинет
          </p>
        </div>
      </router-link>

      <!-- Библиотекарь -->
      <router-link
        to="/login/librarian"
        class="group p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition border-2 border-transparent hover:border-green-500"
      >
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-green-500 transition">
            <BookOpenIcon class="h-8 w-8 text-green-600 group-hover:text-white transition" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Библиотекарь</h3>
          <p class="text-sm text-gray-600">
            Управление выдачами, каталогом и читателями
          </p>
        </div>
      </router-link>

      <!-- Администратор (скрытая, но доступная) -->
      <router-link
        to="/login/admin"
        class="group p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition border-2 border-transparent hover:border-purple-500"
      >
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4 group-hover:bg-purple-500 transition">
            <ShieldCheckIcon class="h-8 w-8 text-purple-600 group-hover:text-white transition" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Администратор</h3>
          <p class="text-sm text-gray-600">
            Полный доступ ко всем функциям системы
          </p>
        </div>
      </router-link>
    </div>

    <div class="mt-8 text-center">
      <p class="text-gray-600">
        Нет аккаунта?
        <router-link to="/register" class="text-blue-600 hover:text-blue-800 font-medium">
          Зарегистрироваться
        </router-link>
      </p>
      <p class="text-sm text-gray-500 mt-4">
        * Для входа как администратор используйте специальный URL
      </p>
    </div>
  </div>
</template>

<script setup>
import { UserIcon, BookOpenIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline'
</script>