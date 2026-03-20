import { defineStore } from 'pinia'
import { loansApi } from '@/api/loans'

export const useLoansStore = defineStore('loans', {
  state: () => ({
    loans: [],
    activeLoans: [],
    overdueLoans: [],
    userLoans: [],
    currentLoan: null,
    stats: null,
    isLoading: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      perPage: 20
    }
  }),

  getters: {
    activeLoansCount: (state) => state.activeLoans.length,
    overdueLoansCount: (state) => state.overdueLoans.length,
    myLoans: (state) => state.userLoans,
    myActiveLoans: (state) => state.userLoans.filter(l => l.status === 'active'),
    myOverdueLoans: (state) => state.userLoans.filter(l => l.status === 'overdue')
  },

  actions: {
    async fetchMyLoans(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getMyLoans({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.userLoans = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки истории выдач'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchMyActiveLoans() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getMyActiveLoans()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки активных выдач'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchMyBorrowStatus() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getMyBorrowStatus()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка проверки статуса'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchAllLoans(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getAll({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.loans = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки выдач'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchActiveLoans(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getActive({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.activeLoans = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки активных выдач'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchOverdueLoans() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getOverdue()
        this.overdueLoans = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки просроченных выдач'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchStats() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getStats()
        this.stats = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки статистики'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchUserLoans(userId, params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getUserLoans(userId, {
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки выдач пользователя'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchLoanById(id) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.getById(id)
        this.currentLoan = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки выдачи'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createLoan(loanData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.create(loanData)
        await this.fetchActiveLoans()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка создания выдачи'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async returnLoan(id, returnData = null) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.return(id, returnData)
        await this.fetchActiveLoans()
        await this.fetchOverdueLoans()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка возврата книги'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async extendLoan(id, extendData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.extend(id, extendData)
        await this.fetchActiveLoans()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка продления выдачи'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async runDailyProcess() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await loansApi.runDailyProcess()
        await this.fetchOverdueLoans()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка запуска ежедневной обработки'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    setPagination(page, perPage) {
      this.pagination.page = page
      this.pagination.perPage = perPage
    },

    clearCurrentLoan() {
      this.currentLoan = null
    },

    clearError() {
      this.error = null
    }
  }
})