import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import { usersApi } from '@/api/users'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    isLoading: false,
    error: null,
    initialized: false // Добавляем флаг инициализации
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    userRoles: (state) => state.user?.roles || [],
    hasRole: (state) => (role) => {
      if (!state.user || !state.user.roles) return false
      return state.user.roles.some(r => r.name === role)
    },
    isReader: (state) => {
      if (!state.user || !state.user.roles) return false
      return state.user.roles.some(r => r.name === 'reader')
    },
    isLibrarian: (state) => {
      if (!state.user || !state.user.roles) return false
      return state.user.roles.some(r => r.name === 'librarian')
    },
    isAdmin: (state) => {
      if (!state.user || !state.user.roles) return false
      return state.user.roles.some(r => r.name === 'admin')
    }
  },

  actions: {
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken
      this.refreshToken = refreshToken
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
    },

    clearTokens() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    async login(credentials, role) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await authApi.login(credentials)
        this.setTokens(response.data.access_token, response.data.refresh_token)
        await this.fetchUser()
        
        // Перенаправляем в зависимости от роли
        if (this.isAdmin) {
          router.push('/admin/dashboard')
        } else if (this.isLibrarian) {
          router.push('/librarian/dashboard')
        } else {
          router.push('/reader/dashboard')
        }
        
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка входа'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await authApi.register(userData)
        this.setTokens(response.data.access_token, response.data.refresh_token)
        await this.fetchUser()
        router.push('/reader/dashboard')
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка регистрации'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchUser() {
      if (!this.accessToken) {
        this.initialized = true
        return null
      }
      
      this.isLoading = true
      try {
        const response = await usersApi.getMe()
        this.user = response.data
        this.initialized = true
        return response.data
      } catch (error) {
        console.error('Error fetching user:', error)
        if (error.response?.status === 401) {
          this.clearTokens()
        }
        this.initialized = true
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async refreshToken() {
      if (!this.refreshToken) {
        this.logout()
        return null
      }

      try {
        const response = await authApi.refresh({
          refresh_token: this.refreshToken
        })
        this.setTokens(response.data.access_token, response.data.refresh_token)
        return response.data
      } catch (error) {
        console.error('Error refreshing token:', error)
        this.logout()
        throw error
      }
    },

    logout() {
      this.clearTokens()
      router.push('/login')
    },

    async initAuth() {
      if (this.initialized) return
      
      if (this.accessToken) {
        try {
          await this.fetchUser()
        } catch (error) {
          console.error('Error initializing auth:', error)
          // Пробуем обновить токен
          try {
            await this.refreshToken()
            await this.fetchUser()
          } catch (refreshError) {
            this.clearTokens()
          }
        }
      } else {
        this.initialized = true
      }
    },

    // Вспомогательный метод для получения корректного маршрута дашборда
    getDashboardRoute() {
      if (this.isAdmin) return '/admin/dashboard'
      if (this.isLibrarian) return '/librarian/dashboard'
      if (this.isReader) return '/reader/dashboard'
      return '/'
    }
  }
})