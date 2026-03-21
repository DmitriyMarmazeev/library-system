<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Вход для читателя</h2>
    <p class="text-gray-600 mb-6">Войдите, чтобы получить доступ к личному кабинету</p>

    <LoginForm :role="'reader'" />

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600">
        Впервые в системе?
        <router-link to="/register" class="text-blue-600 hover:text-blue-800 font-medium">
          Зарегистрироваться
        </router-link>
      </p>
      <p class="text-xs text-gray-500 mt-4">
        * После регистрации вы получите роль читателя
      </p>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/auth/LoginForm.vue'
</script>