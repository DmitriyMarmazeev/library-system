import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    sidebarOpen: false,
    darkMode: false,
    notifications: [],
    modals: [],
    loading: {
      global: false,
      requests: {}
    },
    theme: 'light'
  }),

  getters: {
    isSidebarOpen: (state) => state.sidebarOpen,
    isDarkMode: (state) => state.darkMode,
    currentTheme: (state) => state.theme,
    hasActiveModals: (state) => state.modals.length > 0,
    isLoading: (state) => (key) => state.loading.requests[key] || false,
    isGlobalLoading: (state) => state.loading.global
  },

  actions: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    setSidebar(state) {
      this.sidebarOpen = state
    },

    toggleDarkMode() {
      this.darkMode = !this.darkMode
      this.theme = this.darkMode ? 'dark' : 'light'
      
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      
      localStorage.setItem('theme', this.theme)
    },

    initTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.darkMode = savedTheme === 'dark'
      this.theme = savedTheme
      
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      }
    },

    // Уведомления
    addNotification(notification) {
      const id = Date.now()
      const newNotification = {
        id,
        type: 'info',
        duration: 5000,
        ...notification
      }
      
      this.notifications.push(newNotification)
      
      if (newNotification.duration > 0) {
        setTimeout(() => {
          this.removeNotification(id)
        }, newNotification.duration)
      }
      
      return id
    },

    removeNotification(id) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index !== -1) {
        this.notifications.splice(index, 1)
      }
    },

    clearNotifications() {
      this.notifications = []
    },

    success(message, options = {}) {
      return this.addNotification({ type: 'success', message, ...options })
    },

    error(message, options = {}) {
      return this.addNotification({ type: 'error', message, ...options })
    },

    warning(message, options = {}) {
      return this.addNotification({ type: 'warning', message, ...options })
    },

    info(message, options = {}) {
      return this.addNotification({ type: 'info', message, ...options })
    },

    // Модальные окна
    openModal(modal) {
      const id = Date.now()
      const newModal = {
        id,
        ...modal
      }
      this.modals.push(newModal)
      return id
    },

    closeModal(id) {
      const index = this.modals.findIndex(m => m.id === id)
      if (index !== -1) {
        this.modals.splice(index, 1)
      }
    },

    closeAllModals() {
      this.modals = []
    },

    // Управление загрузкой
    startLoading(key = 'global') {
      if (key === 'global') {
        this.loading.global = true
      } else {
        this.loading.requests[key] = true
      }
    },

    stopLoading(key = 'global') {
      if (key === 'global') {
        this.loading.global = false
      } else {
        this.loading.requests[key] = false
      }
    },

    setLoading(key, status) {
      if (key === 'global') {
        this.loading.global = status
      } else {
        this.loading.requests[key] = status
      }
    },

    resetUI() {
      this.sidebarOpen = false
      this.notifications = []
      this.modals = []
      this.loading = {
        global: false,
        requests: {}
      }
    }
  }
})