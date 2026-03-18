// Проверка наличия роли у пользователя
export const hasRole = (user, role) => {
  if (!user || !user.roles) return false
  return user.roles.some(r => r.name === role)
}

// Проверка наличия любой из ролей
export const hasAnyRole = (user, roles) => {
  if (!user || !user.roles) return false
  return roles.some(role => hasRole(user, role))
}

// Проверка наличия всех ролей
export const hasAllRoles = (user, roles) => {
  if (!user || !user.roles) return false
  return roles.every(role => hasRole(user, role))
}

// Получение имени пользователя для отображения
export const getDisplayName = (user) => {
  if (!user) return 'Неизвестный пользователь'
  const { first_name, last_name } = user
  return `${last_name} ${first_name[0]}.`
}

// Получение цвета для аватарки по имени
export const getAvatarColor = (name) => {
  const colors = [
    'bg-red-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500',
    'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500'
  ]
  const index = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[index % colors.length]
}

// Получение инициалов
export const getInitials = (user) => {
  if (!user) return '?'
  const { first_name, last_name } = user
  return `${last_name[0]}${first_name[0]}`.toUpperCase()
}

// Пагинация
export const getPaginationRange = (currentPage, totalPages) => {
  const delta = 2
  const range = []
  const rangeWithDots = []
  let l

  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
      range.push(i)
    }
  }

  range.forEach(i => {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1)
      } else if (i - l !== 1) {
        rangeWithDots.push('...')
      }
    }
    rangeWithDots.push(i)
    l = i
  })

  return rangeWithDots
}

// Фильтрация по поисковому запросу
export const filterBySearch = (items, searchTerm, fields) => {
  if (!searchTerm) return items
  
  const term = searchTerm.toLowerCase()
  return items.filter(item => 
    fields.some(field => {
      const value = getNestedValue(item, field)
      return value && value.toString().toLowerCase().includes(term)
    })
  )
}

// Получение вложенного значения по пути
export const getNestedValue = (obj, path) => {
  return path.split('.').reduce((current, key) => {
    return current && current[key] !== undefined ? current[key] : undefined
  }, obj)
}

// Сортировка
export const sortItems = (items, field, direction = 'asc') => {
  return [...items].sort((a, b) => {
    const aVal = getNestedValue(a, field)
    const bVal = getNestedValue(b, field)
    
    if (aVal === bVal) return 0
    
    const comparison = aVal > bVal ? 1 : -1
    return direction === 'asc' ? comparison : -comparison
  })
}

// Группировка по полю
export const groupBy = (items, field) => {
  return items.reduce((groups, item) => {
    const key = getNestedValue(item, field)
    if (!groups[key]) {
      groups[key] = []
    }
    groups[key].push(item)
    return groups
  }, {})
}

// Дебаунс
export const debounce = (fn, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}