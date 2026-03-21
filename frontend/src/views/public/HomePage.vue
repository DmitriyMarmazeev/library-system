<template>
  <div class="min-h-screen">
    <!-- Hero секция -->
    <section class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            Добро пожаловать в LibraryMS
          </h1>
          <p class="text-xl md:text-2xl mb-8 text-blue-100">
            Современная система управления библиотекой с открытым доступом к каталогу
          </p>
          <div class="flex justify-center gap-4">
            <router-link
              to="/books"
              class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Начать поиск
            </router-link>
            <router-link
              to="/register"
              class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition"
            >
              Зарегистрироваться
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Статистика -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div v-for="stat in statistics" :key="stat.label" class="text-center">
            <div class="text-3xl font-bold text-blue-600">{{ stat.value }}</div>
            <div class="text-gray-600 mt-2">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Рекомендуемые книги -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center mb-12">Рекомендуемые книги</h2>
        
        <div v-if="isLoading" class="flex justify-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <BookCard
            v-for="book in featuredBooks"
            :key="book.id"
            :book="book"
            :compact="true"
          />
        </div>

        <div class="text-center mt-8">
          <router-link
            to="/books"
            class="text-blue-600 hover:text-blue-800 font-medium"
          >
            Смотреть все книги →
          </router-link>
        </div>
      </div>
    </section>

    <!-- Преимущества -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center mb-12">Наши преимущества</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" class="text-center">
            <div class="flex justify-center mb-4">
              <component :is="feature.icon" class="h-12 w-12 text-blue-600" />
            </div>
            <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="bg-blue-600 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold mb-4">Готовы начать?</h2>
        <p class="text-xl text-blue-100 mb-8">
          Присоединяйтесь к нашей библиотеке сегодня
        </p>
        <div class="flex justify-center gap-4">
          <router-link
            to="/register"
            class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Зарегистрироваться
          </router-link>
          <router-link
            to="/login"
            class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition"
          >
            Войти
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { BookOpenIcon, UserGroupIcon, ClockIcon, ChartBarIcon } from '@heroicons/vue/24/outline'
import BookCard from '@/components/books/BookCard.vue'
import { booksApi } from '@/api/books'

const isLoading = ref(false)
const featuredBooks = ref([])

const statistics = ref([
  { label: 'Книг в каталоге', value: '10,000+' },
  { label: 'Авторов', value: '2,500+' },
  { label: 'Читателей', value: '5,000+' },
  { label: 'Ежедневных выдач', value: '100+' }
])

const features = ref([
  {
    icon: BookOpenIcon,
    title: 'Богатый каталог',
    description: 'Тысячи книг различных жанров и направлений'
  },
  {
    icon: UserGroupIcon,
    title: 'Удобный поиск',
    description: 'Поиск по названию, автору, жанру и году издания'
  },
  {
    icon: ClockIcon,
    title: 'Круглосуточный доступ',
    description: 'Доступ к каталогу 24/7 из любой точки мира'
  },
  {
    icon: ChartBarIcon,
    title: 'Личный кабинет',
    description: 'Отслеживайте свои книги и историю чтения'
  }
])

const fetchFeaturedBooks = async () => {
  isLoading.value = true
  try {
    const response = await booksApi.getAll({ limit: 4 })
    featuredBooks.value = response.data
  } catch (error) {
    console.error('Error fetching featured books:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchFeaturedBooks()
})
</script>