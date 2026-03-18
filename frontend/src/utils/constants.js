export const ROLES = {
  READER: 'reader',
  LIBRARIAN: 'librarian',
  ADMIN: 'admin'
}

export const COPY_STATUS = {
  AVAILABLE: 'available',
  BORROWED: 'borrowed',
  DAMAGED: 'damaged',
  LOST: 'lost'
}

export const LOAN_STATUS = {
  ACTIVE: 'active',
  RETURNED: 'returned',
  OVERDUE: 'overdue'
}

export const COPY_STATUS_COLORS = {
  [COPY_STATUS.AVAILABLE]: 'bg-green-100 text-green-800',
  [COPY_STATUS.BORROWED]: 'bg-blue-100 text-blue-800',
  [COPY_STATUS.DAMAGED]: 'bg-yellow-100 text-yellow-800',
  [COPY_STATUS.LOST]: 'bg-red-100 text-red-800'
}

export const LOAN_STATUS_COLORS = {
  [LOAN_STATUS.ACTIVE]: 'bg-green-100 text-green-800',
  [LOAN_STATUS.RETURNED]: 'bg-gray-100 text-gray-800',
  [LOAN_STATUS.OVERDUE]: 'bg-red-100 text-red-800'
}

export const COPY_STATUS_LABELS = {
  [COPY_STATUS.AVAILABLE]: 'Доступен',
  [COPY_STATUS.BORROWED]: 'Выдан',
  [COPY_STATUS.DAMAGED]: 'Поврежден',
  [COPY_STATUS.LOST]: 'Утерян'
}

export const LOAN_STATUS_LABELS = {
  [LOAN_STATUS.ACTIVE]: 'Активен',
  [LOAN_STATUS.RETURNED]: 'Возвращен',
  [LOAN_STATUS.OVERDUE]: 'Просрочен'
}