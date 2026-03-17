import api from './index'

export const copiesApi = {
  getAll: (params) => api.get('/copies/', { params }),
  getById: (id) => api.get(`/copies/${id}`),
  getByBook: (bookId, params) => api.get(`/copies/by-book/${bookId}`, { params }),
  getByStatus: (status, params) => api.get(`/copies/status/${status}`, { params }),
  searchByLocation: (q) => api.get('/copies/search/location', { params: { q } }),
  getBookSummary: (bookId) => api.get(`/copies/book-summary/${bookId}`),
  getLoanHistory: (copyId, params) => api.get(`/copies/${copyId}/history`, { params }),
  create: (data) => api.post('/copies/', data),
  createBulk: (data) => api.post('/copies/bulk', data),
  update: (id, data) => api.put(`/copies/${id}`, data),
  updateStatus: (id, data) => api.patch(`/copies/${id}/status`, data),
  delete: (id) => api.delete(`/copies/${id}`),
}