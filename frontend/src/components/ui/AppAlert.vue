<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="transform scale-95 opacity-0"
    enter-to-class="transform scale-100 opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="transform scale-100 opacity-100"
    leave-to-class="transform scale-95 opacity-0"
  >
    <div
      v-if="show"
      :class="[
        'rounded-lg p-4',
        variantClasses[variant],
        className
      ]"
      role="alert"
    >
      <div class="flex items-start">
        <!-- Иконка -->
        <div class="flex-shrink-0">
          <component
            :is="iconComponent"
            :class="[
              'h-5 w-5',
              variantIconClasses[variant]
            ]"
          />
        </div>

        <!-- Контент -->
        <div class="ml-3 flex-1">
          <h3 v-if="title" :class="['text-sm font-medium', variantTitleClasses[variant]]">
            {{ title }}
          </h3>
          <div :class="['text-sm', variantTextClasses[variant]]">
            <slot>
              <p>{{ message }}</p>
            </slot>
          </div>

          <!-- Действия -->
          <div v-if="$slots.actions" class="mt-4">
            <slot name="actions" />
          </div>
        </div>

        <!-- Кнопка закрытия -->
        <button
          v-if="closable"
          @click="close"
          :class="[
            'ml-auto -mx-1.5 -my-1.5 rounded-lg p-1.5 inline-flex focus:outline-none focus:ring-2 focus:ring-offset-2',
            variantCloseClasses[variant]
          ]"
        >
          <span class="sr-only">Закрыть</span>
          <XMarkIcon class="h-4 w-4" />
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  show: {
    type: Boolean,
    default: true
  },
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  closable: {
    type: Boolean,
    default: true
  },
  duration: {
    type: Number,
    default: 0
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'update:show'])

const isVisible = ref(props.show)

const variantClasses = {
  success: 'bg-green-50 border border-green-200',
  error: 'bg-red-50 border border-red-200',
  warning: 'bg-yellow-50 border border-yellow-200',
  info: 'bg-blue-50 border border-blue-200'
}

const variantIconClasses = {
  success: 'text-green-400',
  error: 'text-red-400',
  warning: 'text-yellow-400',
  info: 'text-blue-400'
}

const variantTitleClasses = {
  success: 'text-green-800',
  error: 'text-red-800',
  warning: 'text-yellow-800',
  info: 'text-blue-800'
}

const variantTextClasses = {
  success: 'text-green-700',
  error: 'text-red-700',
  warning: 'text-yellow-700',
  info: 'text-blue-700'
}

const variantCloseClasses = {
  success: 'bg-green-50 text-green-500 hover:bg-green-100 focus:ring-green-600 focus:ring-offset-green-50',
  error: 'bg-red-50 text-red-500 hover:bg-red-100 focus:ring-red-600 focus:ring-offset-red-50',
  warning: 'bg-yellow-50 text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600 focus:ring-offset-yellow-50',
  info: 'bg-blue-50 text-blue-500 hover:bg-blue-100 focus:ring-blue-600 focus:ring-offset-blue-50'
}

const iconComponent = computed(() => {
  switch (props.variant) {
    case 'success':
      return CheckCircleIcon
    case 'error':
      return XCircleIcon
    case 'warning':
      return ExclamationTriangleIcon
    default:
      return InformationCircleIcon
  }
})

const close = () => {
  isVisible.value = false
  emit('update:show', false)
  emit('close')
}

watch(() => props.show, (newVal) => {
  isVisible.value = newVal
})

onMounted(() => {
  if (props.duration > 0) {
    setTimeout(() => {
      close()
    }, props.duration)
  }
})
</script>