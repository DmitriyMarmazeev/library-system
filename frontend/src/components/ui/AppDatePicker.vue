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
      <!-- Иконка календаря -->
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <CalendarIcon class="h-5 w-5 text-gray-400" />
      </div>

      <!-- Поле ввода даты -->
      <input
        :id="id"
        :type="type"
        :value="displayValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="minDate"
        :max="maxDate"
        :class="[
          'block w-full rounded-lg border pl-10 pr-3 py-2 transition duration-200',
          error
            ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          className
        ]"
        v-bind="$attrs"
        @input="onInput"
        @blur="onBlur"
        @change="onChange"
      />
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
import { computed } from 'vue'
import { CalendarIcon } from '@heroicons/vue/24/outline'
import { format, parseISO, isValid } from 'date-fns'

const props = defineProps({
  modelValue: {
    type: [String, Date, Number],
    default: null
  },
  type: {
    type: String,
    default: 'date',
    validator: (value) => ['date', 'datetime-local', 'month', 'week', 'time'].includes(value)
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
  minDate: {
    type: String,
    default: ''
  },
  maxDate: {
    type: String,
    default: ''
  },
  format: {
    type: String,
    default: 'yyyy-MM-dd'
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'change'])

const id = computed(() => `datepicker-${Math.random().toString(36).substr(2, 9)}`)

const displayValue = computed(() => {
  if (!props.modelValue) return ''
  
  try {
    let date
    if (props.modelValue instanceof Date) {
      date = props.modelValue
    } else if (typeof props.modelValue === 'string') {
      date = parseISO(props.modelValue)
    } else if (typeof props.modelValue === 'number') {
      date = new Date(props.modelValue)
    }
    
    if (date && isValid(date)) {
      return format(date, props.format)
    }
  } catch (e) {
    console.warn('Error formatting date:', e)
  }
  
  return props.modelValue
})

const onInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const onBlur = (event) => {
  emit('blur', event)
}

const onChange = (event) => {
  emit('change', event.target.value)
}
</script>