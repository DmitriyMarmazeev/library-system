import { ref } from 'vue'

export function useNotifications() {
  const notifications = ref([])

  const addNotification = (notification) => {
    const id = Date.now()
    const defaultNotification = {
      id,
      type: 'info',
      message: '',
      duration: 5000,
      ...notification
    }

    notifications.value.push(defaultNotification)

    if (defaultNotification.duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, defaultNotification.duration)
    }

    return id
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  const success = (message, options = {}) => {
    return addNotification({ type: 'success', message, ...options })
  }

  const error = (message, options = {}) => {
    return addNotification({ type: 'error', message, ...options })
  }

  const warning = (message, options = {}) => {
    return addNotification({ type: 'warning', message, ...options })
  }

  const info = (message, options = {}) => {
    return addNotification({ type: 'info', message, ...options })
  }

  const clearAll = () => {
    notifications.value = []
  }

  return {
    notifications,
    success,
    error,
    warning,
    info,
    removeNotification,
    clearAll
  }
}