import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { hasRole, hasAnyRole, hasAllRoles } from '@/utils/helpers'

export function useAuth() {
  const authStore = useAuthStore()

  const user = computed(() => authStore.user)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isLoading = computed(() => authStore.isLoading)

  const checkRole = (role) => hasRole(user.value, role)
  const checkAnyRole = (roles) => hasAnyRole(user.value, roles)
  const checkAllRoles = (roles) => hasAllRoles(user.value, roles)

  const isReader = computed(() => checkRole('reader'))
  const isLibrarian = computed(() => checkRole('librarian'))
  const isAdmin = computed(() => checkRole('admin'))

  const login = async (credentials, role) => {
    return authStore.login(credentials, role)
  }

  const logout = () => {
    authStore.logout()
  }

  const register = async (userData) => {
    return authStore.register(userData)
  }

  const refreshUser = async () => {
    return authStore.fetchUser()
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    isReader,
    isLibrarian,
    isAdmin,
    checkRole,
    checkAnyRole,
    checkAllRoles,
    login,
    logout,
    register,
    refreshUser
  }
}