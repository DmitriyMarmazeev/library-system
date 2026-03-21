<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">О проекте</h1>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        LibraryMS - современная система управления библиотекой с открытым доступом к каталогу
      </p>
    </div>

    <!-- Основная информация -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
      <div>
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Наша миссия</h2>
        <p class="text-gray-600 leading-relaxed mb-4">
          Мы стремимся сделать чтение доступным для всех, предоставляя удобный инструмент для поиска и бронирования книг. Наша платформа объединяет читателей, библиотекарей и администраторов в едином информационном пространстве.
        </p>
        <p class="text-gray-600 leading-relaxed">
          LibraryMS разработана с учетом современных требований к библиотечным системам и предоставляет все необходимые функции для эффективного управления библиотечным фондом.
        </p>
      </div>

      <div>
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Возможности системы</h2>
        <ul class="space-y-3">
          <li v-for="feature in features" :key="feature.title" class="flex items-start gap-3">
            <CheckCircleIcon class="h-6 w-6 text-green-500 flex-shrink-0" />
            <div>
              <h3 class="font-medium text-gray-900">{{ feature.title }}</h3>
              <p class="text-sm text-gray-600">{{ feature.description }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Для кого предназначена система -->
    <div class="mb-16">
      <h2 class="text-2xl font-semibold text-gray-900 text-center mb-8">Для кого предназначена система</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="role in roles" :key="role.title" class="bg-white rounded-lg shadow-sm p-6 text-center">
          <div class="flex justify-center mb-4">
            <component :is="role.icon" class="h-12 w-12 text-blue-600" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ role.title }}</h3>
          <p class="text-gray-600">{{ role.description }}</p>
        </div>
      </div>
    </div>

    <!-- Технические детали -->
    <div class="bg-gray-50 rounded-lg p-8 mb-16">
      <h2 class="text-2xl font-semibold text-gray-900 text-center mb-6">Технические детали</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-3">Бэкенд</h3>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-center gap-2">
              <ServerIcon class="h-4 w-4 text-gray-400" />
              FastAPI - современный веб-фреймворк
            </li>
            <li class="flex items-center gap-2">
              <ServerIcon class="h-4 w-4 text-gray-400" />
              PostgreSQL - надежная база данных
            </li>
            <li class="flex items-center gap-2">
              <CodeBracketIcon class="h-4 w-4 text-gray-400" />
              SQLAlchemy - ORM для работы с БД
            </li>
            <li class="flex items-center gap-2">
              <LockClosedIcon class="h-4 w-4 text-gray-400" />
              JWT - безопасная аутентификация
            </li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-3">Фронтенд</h3>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-center gap-2">
              <CodeBracketIcon class="h-4 w-4 text-gray-400" />
              Vue 3 - прогрессивный фреймворк
            </li>
            <li class="flex items-center gap-2">
              <ServerIcon class="h-4 w-4 text-gray-400" />
              Pinia - управление состоянием
            </li>
            <li class="flex items-center gap-2">
              <PaintBrushIcon class="h-4 w-4 text-gray-400" />
              Tailwind CSS - стилизация
            </li>
            <li class="flex items-center gap-2">
              <RocketLaunchIcon class="h-4 w-4 text-gray-400" />
              Vite - быстрая сборка
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Контакты -->
    <div class="text-center">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">Свяжитесь с нами</h2>
      <p class="text-gray-600 mb-6">
        Если у вас есть вопросы или предложения, мы всегда рады помочь
      </p>
      <div class="flex justify-center gap-6">
        <a
          href="mailto:info@libraryms.ru"
          class="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition"
        >
          <EnvelopeIcon class="h-5 w-5" />
          info@libraryms.ru
        </a>
        <a
          href="tel:+78001234567"
          class="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition"
        >
          <PhoneIcon class="h-5 w-5" />
          8 (800) 123-45-67
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  UserIcon,
  BookOpenIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
  EnvelopeIcon,
  PhoneIcon,
  ServerIcon,
  CodeBracketIcon,
  LockClosedIcon,
  PaintBrushIcon,
  RocketLaunchIcon
} from '@heroicons/vue/24/outline'

const features = [
  {
    title: 'Удобный каталог',
    description: 'Поиск книг по названию, автору, жанру и году издания'
  },
  {
    title: 'Личный кабинет',
    description: 'Отслеживание взятых книг и истории чтения'
  },
  {
    title: 'Управление выдачами',
    description: 'Автоматизация процессов выдачи и возврата книг'
  },
  {
    title: 'Статистика',
    description: 'Анализ популярности книг и активности читателей'
  },
  {
    title: 'Многоролевая система',
    description: 'Разграничение доступа для читателей, библиотекарей и администраторов'
  },
  {
    title: 'Бронирование',
    description: 'Возможность забронировать книгу онлайн'
  }
]

const roles = [
  {
    icon: UserIcon,
    title: 'Читатели',
    description: 'Поиск книг, бронирование, просмотр истории, личный кабинет'
  },
  {
    icon: BookOpenIcon,
    title: 'Библиотекари',
    description: 'Управление выдачами, каталогом, читателями и экземплярами книг'
  },
  {
    icon: ShieldCheckIcon,
    title: 'Администраторы',
    description: 'Полный доступ к системе, управление пользователями и ролями'
  }
]
</script>