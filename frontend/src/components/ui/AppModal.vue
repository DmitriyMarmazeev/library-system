<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-50">
      <!-- Затемнение фона -->
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-50" />
      </TransitionChild>

      <!-- Модальное окно -->
      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
          :class="{
            'items-start pt-16': position === 'top',
            'items-center': position === 'center'
          }"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              :class="[
                'w-full transform overflow-hidden rounded-lg bg-white p-6 text-left align-middle shadow-xl transition-all',
                sizeClasses[size]
              ]"
            >
              <!-- Заголовок -->
              <DialogTitle
                v-if="title"
                as="h3"
                class="text-lg font-semibold leading-6 text-gray-900 mb-4"
              >
                {{ title }}
              </DialogTitle>

              <!-- Кнопка закрытия -->
              <button
                v-if="closable"
                @click="closeModal"
                class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon class="h-5 w-5" />
              </button>

              <!-- Контент -->
              <div class="mt-2">
                <slot>
                  <p class="text-sm text-gray-500">{{ content }}</p>
                </slot>
              </div>

              <!-- Действия -->
              <div v-if="$slots.actions || showActions" class="mt-6 flex justify-end gap-3">
                <slot name="actions">
                  <AppButton
                    v-if="cancelText"
                    variant="secondary"
                    size="sm"
                    @click="closeModal"
                  >
                    {{ cancelText }}
                  </AppButton>
                  <AppButton
                    v-if="confirmText"
                    :variant="confirmVariant"
                    size="sm"
                    @click="handleConfirm"
                  >
                    {{ confirmText }}
                  </AppButton>
                </slot>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import AppButton from './AppButton.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  position: {
    type: String,
    default: 'center',
    validator: (value) => ['top', 'center'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: false
  },
  cancelText: {
    type: String,
    default: 'Отмена'
  },
  confirmText: {
    type: String,
    default: 'Подтвердить'
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const sizeClasses = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
  full: 'max-w-7xl'
}

const closeModal = () => {
  emit('update:modelValue', false)
  emit('cancel')
}

const handleConfirm = () => {
  emit('confirm')
  if (props.closable) {
    closeModal()
  }
}
</script>