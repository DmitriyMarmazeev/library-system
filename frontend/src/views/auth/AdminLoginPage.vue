<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Вход для администратора</h2>
    <p class="text-gray-600 mb-6">Только для администраторов системы</p>

    <LoginForm :role="'admin'" />

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        <router-link to="/login" class="text-blue-600 hover:text-blue-800">
          ← На страницу выбора роли
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/auth/LoginForm.vue'
</script>