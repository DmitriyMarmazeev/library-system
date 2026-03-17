import api from './index'

export const usersApi = {
  getAll: (params) => api.get('/users/', { params }),
  getById: (id) => api.get(`/users/${id}`),
  getMe: () => api.get('/users/me'),
  search: (q) => api.get('/users/search', { params: { q } }),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
  changePassword: (id, data) => api.post(`/users/${id}/change-password`, data),
  getRoles: (id) => api.get(`/users/${id}/roles`),
  addRole: (id, data) => api.post(`/users/${id}/roles`, data),
  toggleActive: (id) => api.post(`/users/${id}/toggle-active`),
}