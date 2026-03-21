<template>
  <component
    :is="tag"
    :to="to"
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center font-medium rounded-lg transition duration-200',
      variantClasses[variant],
      sizeClasses[size],
      { 'opacity-50 cursor-not-allowed': disabled || loading },
      className
    ]"
    v-bind="$attrs"
  >
    <!-- Иконка слева -->
    <component
      v-if="leftIcon"
      :is="leftIcon"
      class="h-5 w-5 mr-2"
      :class="{ 'animate-spin': loading && !leftIcon }"
    />

    <!-- Контент -->
    <slot>
      <span v-if="loading && !loadingText">Загрузка...</span>
      <span v-else>{{ text }}</span>
    </slot>

    <!-- Иконка справа -->
    <component
      v-if="rightIcon && !loading"
      :is="rightIcon"
      class="h-5 w-5 ml-2"
    />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // Варианты кнопки
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary',
      'secondary',
      'success',
      'danger',
      'warning',
      'outline',
      'ghost'
    ].includes(value)
  },

  // Размер
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },

  // Текст (если не используется слот)
  text: {
    type: String,
    default: ''
  },

  // Иконки
  leftIcon: {
    type: Object,
    default: null
  },
  rightIcon: {
    type: Object,
    default: null
  },

  // Состояния
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: ''
  },

  // Для ссылок
  to: {
    type: [String, Object],
    default: null
  },

  // Тип для кнопки
  type: {
    type: String,
    default: 'button'
  },

  // Дополнительные классы
  className: {
    type: String,
    default: ''
  }
})

const tag = computed(() => props.to ? 'router-link' : 'button')

const variantClasses = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2',
  success: 'bg-green-600 hover:bg-green-700 text-white focus:ring-2 focus:ring-green-500 focus:ring-offset-2',
  danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-2 focus:ring-red-500 focus:ring-offset-2',
  warning: 'bg-yellow-500 hover:bg-yellow-600 text-white focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2',
  outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
  ghost: 'text-gray-600 hover:bg-gray-100 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2'
}

const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
}
</script>