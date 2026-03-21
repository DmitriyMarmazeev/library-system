<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <!-- Иконка -->
      <div class="flex justify-center mb-6">
        <div class="relative">
          <div class="text-9xl font-bold text-gray-300 opacity-50">404</div>
          <div class="absolute inset-0 flex items-center justify-center">
            <DocumentMagnifyingGlassIcon class="h-24 w-24 text-blue-500 opacity-75" />
          </div>
        </div>
      </div>

      <!-- Заголовок -->
      <h1 class="text-3xl font-bold text-gray-900 mb-4">
        Страница не найдена
      </h1>

      <!-- Описание -->
      <p class="text-lg text-gray-600 mb-8">
        К сожалению, запрашиваемая страница не существует или была перемещена.
      </p>

      <!-- Варианты действий -->
      <div class="space-y-4">
        <router-link
          to="/"
          class="inline-flex items-center justify-center w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <HomeIcon class="h-5 w-5 mr-2" />
          Вернуться на главную
        </router-link>

        <button
          @click="goBack"
          class="inline-flex items-center justify-center w-full px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
        >
          <ArrowLeftIcon class="h-5 w-5 mr-2" />
          Вернуться назад
        </button>

        <div class="pt-4">
          <p class="text-sm text-gray-500 mb-3">Возможно, вас заинтересует:</p>
          <div class="flex justify-center gap-4">
            <router-link to="/books" class="text-sm text-blue-600 hover:text-blue-800">
              Каталог книг
            </router-link>
            <span class="text-gray-300">|</span>
            <router-link to="/authors" class="text-sm text-blue-600 hover:text-blue-800">
              Авторы
            </router-link>
            <span class="text-gray-300">|</span>
            <router-link to="/genres" class="text-sm text-blue-600 hover:text-blue-800">
              Жанры
            </router-link>
          </div>
        </div>
      </div>

      <!-- Поиск -->
      <div class="mt-8 pt-8 border-t">
        <p class="text-sm text-gray-600 mb-3">
          Попробуйте найти нужную информацию через поиск:
        </p>
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск книг..."
            class="input-field pl-10"
            @keyup.enter="searchBooks"
          />
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  DocumentMagnifyingGlassIcon,
  HomeIcon,
  ArrowLeftIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const searchQuery = ref('')

const goBack = () => {
  router.go(-1)
}

const searchBooks = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/books',
      query: { title: searchQuery.value.trim() }
    })
  }
}
</script>