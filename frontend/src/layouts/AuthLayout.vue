<template>
  <div class="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <!-- Логотип -->
      <div class="text-center">
        <router-link to="/" class="inline-flex items-center gap-2 text-2xl font-bold text-gray-900">
          <BookOpenIcon class="h-8 w-8 text-blue-600" />
          <span>LibraryMS</span>
        </router-link>
      </div>

      <!-- Контент страницы (форма логина/регистрации) -->
      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-4 shadow-xl rounded-lg sm:px-10">
          <router-view />
        </div>

        <!-- Ссылка на главную -->
        <div class="mt-4 text-center">
          <router-link to="/" class="text-sm text-gray-600 hover:text-gray-900">
            ← Вернуться на главную
          </router-link>
        </div>
      </div>
    </div>

    <!-- Футер -->
    <footer class="mt-8 text-center text-sm text-gray-500">
      <p>&copy; {{ new Date().getFullYear() }} Library Management System</p>
    </footer>
  </div>
</template>

<script setup>
import { BookOpenIcon } from '@heroicons/vue/24/outline'
</script>