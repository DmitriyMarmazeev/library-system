import { defineStore } from 'pinia'
import { booksApi } from '@/api/books'

export const useBooksStore = defineStore('books', {
  state: () => ({
    books: [],
    authors: [],
    genres: [],
    currentBook: null,
    currentAuthor: null,
    currentGenre: null,
    isLoading: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      perPage: 20
    }
  }),

  getters: {
    booksCount: (state) => state.books.length,
    authorsCount: (state) => state.authors.length,
    genresCount: (state) => state.genres.length,
    availableBooks: (state) => state.books.filter(b => b.available_copies > 0)
  },

  actions: {
    async fetchBooks(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getAll({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.books = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки книг'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchBookById(id) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getById(id)
        this.currentBook = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки книги'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createBook(bookData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.create(bookData)
        await this.fetchBooks()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка создания книги'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateBook(id, bookData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.update(id, bookData)
        if (this.currentBook?.id === id) {
          this.currentBook = response.data
        }
        await this.fetchBooks()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка обновления книги'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deleteBook(id) {
      this.isLoading = true
      this.error = null
      
      try {
        await booksApi.delete(id)
        await this.fetchBooks()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка удаления книги'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async searchBooks(searchParams) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.search({
          ...searchParams,
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage
        })
        this.books = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка поиска книг'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Authors
    async fetchAuthors(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getAuthors({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.authors = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки авторов'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchAuthorById(id) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getAuthorById(id)
        this.currentAuthor = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки автора'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createAuthor(authorData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.createAuthor(authorData)
        await this.fetchAuthors()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка создания автора'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateAuthor(id, authorData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.updateAuthor(id, authorData)
        if (this.currentAuthor?.id === id) {
          this.currentAuthor = response.data
        }
        await this.fetchAuthors()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка обновления автора'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deleteAuthor(id) {
      this.isLoading = true
      this.error = null
      
      try {
        await booksApi.deleteAuthor(id)
        await this.fetchAuthors()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка удаления автора'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Genres
    async fetchGenres(params = {}) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getGenres({
          skip: (this.pagination.page - 1) * this.pagination.perPage,
          limit: this.pagination.perPage,
          ...params
        })
        this.genres = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки жанров'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchGenreById(id) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.getGenreById(id)
        this.currentGenre = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки жанра'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createGenre(genreData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.createGenre(genreData)
        await this.fetchGenres()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка создания жанра'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateGenre(id, genreData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await booksApi.updateGenre(id, genreData)
        if (this.currentGenre?.id === id) {
          this.currentGenre = response.data
        }
        await this.fetchGenres()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка обновления жанра'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deleteGenre(id) {
      this.isLoading = true
      this.error = null
      
      try {
        await booksApi.deleteGenre(id)
        await this.fetchGenres()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка удаления жанра'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    setPagination(page, perPage) {
      this.pagination.page = page
      this.pagination.perPage = perPage
    },

    clearCurrentBook() {
      this.currentBook = null
    },

    clearCurrentAuthor() {
      this.currentAuthor = null
    },

    clearCurrentGenre() {
      this.currentGenre = null
    },

    clearError() {
      this.error = null
    }
  }
})