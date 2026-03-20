import { defineStore } from 'pinia'
import { copiesApi } from '@/api/copies'

export const useCopiesStore = defineStore('copies', {
  state: () => ({
    copies: [],
    currentCopy: null,
    isLoading: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      perPage: 20
    }
  }),

  getters: {
    availableCopies: (state) => state.copies.filter(c => c.status === 'available'),
    borrowedCopies: (state) => state.copies.filter(c => c.status === 'borrowed'),
    damagedCopies: (state) => state.copies.filter(c => c.status === 'damaged'),
    lostCopies: (state) => state.copies.filter(c => c.status === 'lost'),
    copiesByBook: (state) => (bookId) => state.copies.filter(c => c.book_id === bookId)
  },

  actions: {
    async fetchCopies(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getAll({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.copies = response.data
        this.pagination.total = parseInt(response.headers?.['x-total-count']) || this.copies.length
        return this.copies
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ??????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchCopyById(id) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getById(id)
        this.currentCopy = response.data
        return this.currentCopy
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchCopiesByBook(bookId, params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getByBook(bookId, {
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ?????????????????????? ??????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchCopiesByStatus(status, params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getByStatus(status, {
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ?????????????????????? ???? ??????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async searchByLocation(query) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.searchByLocation(query)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????? ???? ????????????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async getBookSummary(bookId) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getBookSummary(bookId)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ?????????????????? ???????????? ???? ??????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchCopyLoanHistory(copyId, params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.getLoanHistory(copyId, params)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ?????????????? ??????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createCopy(copyData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.create(copyData)
        await this.fetchCopies()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createCopiesBulk(bulkData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.createBulk(bulkData)
        await this.fetchCopies()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ?????????????????? ???????????????? ??????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateCopy(id, copyData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.update(id, copyData)
        if (this.currentCopy?.id === id) {
          this.currentCopy = response.data
        }
        await this.fetchCopies()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????????? ????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateCopyStatus(id, statusData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await copiesApi.updateStatus(id, statusData)
        if (this.currentCopy?.id === id) {
          this.currentCopy = response.data
        }
        await this.fetchCopies()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????????? ??????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deleteCopy(id) {
      this.isLoading = true
      this.error = null
      
      try {
        await copiesApi.delete(id)
        await this.fetchCopies()
        if (this.currentCopy?.id === id) {
          this.currentCopy = null
        }
      } catch (error) {
        this.error = error.response?.data?.detail || '???????????? ???????????????? ????????????????????'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    setPagination(page, perPage) {
      this.pagination.page = page
      this.pagination.perPage = perPage
    },

    clearCurrentCopy() {
      this.currentCopy = null
    },

    clearError() {
      this.error = null
    }
  }
})