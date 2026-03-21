<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Вход для библиотекаря</h2>
    <p class="text-gray-600 mb-6">Войдите, чтобы получить доступ к рабочему месту</p>

    <LoginForm :role="'librarian'" />

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        <router-link to="/login" class="text-blue-600 hover:text-blue-800">
          ← Выбрать другую роль
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/auth/LoginForm.vue'
</script>