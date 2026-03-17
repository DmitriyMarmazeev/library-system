import api from './index'

export const booksApi = {
  // Books
  getAll: (params) => api.get('/books/', { params }),
  getById: (id) => api.get(`/books/${id}`),
  search: (params) => api.get('/books/search', { params }),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),

  // Authors
  getAuthors: (params) => api.get('/books/authors/all', { params }),
  searchAuthors: (q) => api.get('/books/authors/search', { params: { q } }),
  getAuthorById: (id) => api.get(`/books/authors/${id}`),
  createAuthor: (data) => api.post('/books/authors', data),
  updateAuthor: (id, data) => api.put(`/books/authors/${id}`, data),
  deleteAuthor: (id) => api.delete(`/books/authors/${id}`),

  // Genres
  getGenres: (params) => api.get('/books/genres/all', { params }),
  searchGenres: (q) => api.get('/books/genres/search', { params: { q } }),
  getGenreById: (id) => api.get(`/books/genres/${id}`),
  createGenre: (data) => api.post('/books/genres', data),
  updateGenre: (id, data) => api.put(`/books/genres/${id}`, data),
  deleteGenre: (id) => api.delete(`/books/genres/${id}`),
}