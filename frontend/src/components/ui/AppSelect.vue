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
      <select
        :id="id"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :class="[
          'block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200',
          error ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          className
        ]"
        v-bind="$attrs"
        @change="onChange"
        @blur="onBlur"
      >
        <!-- Пустая опция -->
        <option v-if="placeholder" value="" disabled selected>
          {{ placeholder }}
        </option>

        <!-- Опции из пропсов -->
        <template v-if="options">
          <option
            v-for="option in options"
            :key="getOptionValue(option)"
            :value="getOptionValue(option)"
            :disabled="getOptionDisabled(option)"
          >
            {{ getOptionLabel(option) }}
          </option>
        </template>

        <!-- Слот для кастомных опций -->
        <slot v-else />
      </select>

      <!-- Иконка стрелки -->
      <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <ChevronDownIcon class="h-4 w-4 text-gray-400" />
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
import { computed } from 'vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: ''
  },
  options: {
    type: Array,
    default: null
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
  required: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  },
  // Настройки для отображения опций
  optionLabel: {
    type: String,
    default: 'label'
  },
  optionValue: {
    type: String,
    default: 'value'
  },
  optionDisabled: {
    type: String,
    default: 'disabled'
  }
})

const emit = defineEmits(['update:modelValue', 'blur'])

const id = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

const getOptionLabel = (option) => {
  if (typeof option === 'string' || typeof option === 'number') {
    return option
  }
  return option[props.optionLabel] || option.label || option.name || String(option)
}

const getOptionValue = (option) => {
  if (typeof option === 'string' || typeof option === 'number') {
    return option
  }
  return option[props.optionValue] !== undefined ? option[props.optionValue] : option.id || option.value
}

const getOptionDisabled = (option) => {
  if (typeof option === 'object') {
    return option[props.optionDisabled] || false
  }
  return false
}

const onChange = (event) => {
  emit('update:modelValue', event.target.value)
}

const onBlur = (event) => {
  emit('blur', event)
}
</script>