<template>
  <div class="w-full">
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <div class="relative">
      <!-- Иконка слева -->
      <div
        v-if="leftIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <component :is="leftIcon" class="h-5 w-5 text-gray-400" />
      </div>

      <!-- Поле ввода -->
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :class="[
          'block w-full rounded-lg border transition duration-200',
          leftIcon ? 'pl-10' : 'pl-3',
          rightIcon ? 'pr-10' : 'pr-3',
          error
            ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          className
        ]"
        v-bind="$attrs"
        @input="onInput"
        @blur="onBlur"
      />

      <!-- Иконка справа (очистка/показать пароль) -->
      <div
        v-if="showClearButton && modelValue"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <button
          type="button"
          @click="clearInput"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
        >
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>

      <!-- Кнопка показа пароля -->
      <div
        v-else-if="type === 'password'"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <button
          type="button"
          @click="togglePasswordVisibility"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
        >
          <component
            :is="showPassword ? EyeSlashIcon : EyeIcon"
            class="h-5 w-5"
          />
        </button>
      </div>

      <!-- Иконка справа (кастомная) -->
      <div
        v-else-if="rightIcon"
        class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none"
      >
        <component :is="rightIcon" class="h-5 w-5 text-gray-400" />
      </div>
    </div>

    <!-- Сообщение об ошибке -->
    <p v-if="error" class="mt-1 text-sm text-red-600">
      {{ error }}
    </p>

    <!-- Вспомогательный текст -->
    <p v-if="hint && !error" class="mt-1 text-sm text-gray-500">
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { XMarkIcon, EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  leftIcon: {
    type: Object,
    default: null
  },
  rightIcon: {
    type: Object,
    default: null
  },
  clearable: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'clear'])

const id = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const showPassword = ref(false)
const inputType = computed(() => {
  if (props.type === 'password' && showPassword.value) {
    return 'text'
  }
  return props.type
})

const showClearButton = computed(() => {
  return props.clearable && props.type !== 'password' && !props.disabled && !props.readonly
})

const onInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const onBlur = (event) => {
  emit('blur', event)
}

const clearInput = () => {
  emit('update:modelValue', '')
  emit('clear')
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>