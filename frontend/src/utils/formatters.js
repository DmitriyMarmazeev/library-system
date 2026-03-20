import { format, formatDistance, formatRelative, differenceInDays } from 'date-fns'
import { ru } from 'date-fns/locale'

export const formatDate = (date) => {
  if (!date) return '-'
  return format(new Date(date), 'dd.MM.yyyy', { locale: ru })
}

export const formatDateTime = (date) => {
  if (!date) return '-'
  return format(new Date(date), 'dd.MM.yyyy HH:mm', { locale: ru })
}

export const formatRelativeDate = (date) => {
  if (!date) return '-'
  return formatRelative(new Date(date), new Date(), { locale: ru })
}

export const formatDistanceToNow = (date) => {
  if (!date) return '-'
  return formatDistance(new Date(date), new Date(), { 
    locale: ru,
    addSuffix: true 
  })
}

export const formatDaysRemaining = (dueDate) => {
  if (!dueDate) return '-'
  const days = differenceInDays(new Date(dueDate), new Date())
  
  if (days > 0) return `${days} дн.`
  if (days === 0) return 'Сегодня'
  return `Просрочено на ${Math.abs(days)} дн.`
}

export const formatFullName = (user) => { // Переименовано с getDisplayName на formatFullName
  if (!user) return ''
  const { last_name, first_name, middle_name } = user
  return [last_name, first_name, middle_name].filter(Boolean).join(' ')
}

export const formatPhone = (phone) => {
  if (!phone) return ''
  // Формат: +7 (999) 999-99-99
  const cleaned = phone.replace(/\D/g, '')
  const match = cleaned.match(/^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})$/)
  if (match) {
    return `+${match[1]} (${match[2]}) ${match[3]}-${match[4]}-${match[5]}`
  }
  return phone
}