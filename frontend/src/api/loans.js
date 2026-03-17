import api from './index'

export const loansApi = {
  // User endpoints
  getMyLoans: (params) => api.get('/loans/my-loans', { params }),
  getMyActiveLoans: () => api.get('/loans/my-active-loans'),
  getMyBorrowStatus: () => api.get('/loans/my-borrow-status'),

  // Librarian/Admin endpoints
  getAll: (params) => api.get('/loans/', { params }),
  getActive: (params) => api.get('/loans/active', { params }),
  getOverdue: () => api.get('/loans/overdue'),
  getStats: () => api.get('/loans/stats'),
  getUserLoans: (userId, params) => api.get(`/loans/user/${userId}`, { params }),
  getCopyHistory: (copyId) => api.get(`/loans/copy/${copyId}/history`),
  getById: (id) => api.get(`/loans/${id}`),
  create: (data) => api.post('/loans/', data),
  return: (id, data) => api.post(`/loans/${id}/return`, data),
  extend: (id, data) => api.post(`/loans/${id}/extend`, data),
  runDailyProcess: () => api.post('/loans/daily-process'),
}