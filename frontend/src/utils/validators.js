import * as yup from 'yup'

// Регулярные выражения
const PHONE_REGEX = /^\+?[0-9]{10,15}$/
const ISBN_REGEX = /^(?:\d{10}|\d{13})$/

// Схемы валидации
export const loginSchema = yup.object({
  email: yup
    .string()
    .email('Введите корректный email')
    .required('Email обязателен'),
  password: yup
    .string()
    .min(6, 'Пароль должен содержать минимум 6 символов')
    .required('Пароль обязателен')
})

export const registerSchema = yup.object({
  email: yup
    .string()
    .email('Введите корректный email')
    .required('Email обязателен'),
  password: yup
    .string()
    .min(6, 'Пароль должен содержать минимум 6 символов')
    .required('Пароль обязателен'),
  password_confirm: yup
    .string()
    .oneOf([yup.ref('password')], 'Пароли не совпадают')
    .required('Подтверждение пароля обязательно'),
  first_name: yup
    .string()
    .min(2, 'Имя должно содержать минимум 2 символа')
    .max(50, 'Имя слишком длинное')
    .required('Имя обязательно'),
  last_name: yup
    .string()
    .min(2, 'Фамилия должна содержать минимум 2 символа')
    .max(50, 'Фамилия слишком длинная')
    .required('Фамилия обязательна'),
  middle_name: yup
    .string()
    .max(50, 'Отчество слишком длинное')
    .nullable(),
  phone: yup
    .string()
    .matches(PHONE_REGEX, 'Введите корректный номер телефона')
    .nullable()
})

export const bookSchema = yup.object({
  title: yup
    .string()
    .min(2, 'Название должно содержать минимум 2 символа')
    .max(255, 'Название слишком длинное')
    .required('Название обязательно'),
  isbn: yup
    .string()
    .matches(ISBN_REGEX, 'ISBN должен содержать 10 или 13 цифр')
    .nullable(),
  publication_year: yup
    .number()
    .min(1400, 'Год должен быть не ранее 1400')
    .max(new Date().getFullYear(), 'Год не может быть в будущем')
    .nullable(),
  pages: yup
    .number()
    .min(1, 'Количество страниц должно быть больше 0')
    .max(10000, 'Слишком много страниц')
    .nullable(),
  publisher: yup
    .string()
    .max(100, 'Название издательства слишком длинное')
    .nullable(),
  author_ids: yup
    .array()
    .min(1, 'Добавьте хотя бы одного автора')
    .of(yup.number())
})

export const loanSchema = yup.object({
  copy_id: yup
    .number()
    .required('Выберите экземпляр книги'),
  user_id: yup
    .number()
    .required('Выберите читателя'),
  due_date: yup
    .date()
    .min(new Date(), 'Дата возврата не может быть в прошлом')
    .max(new Date(new Date().setMonth(new Date().getMonth() + 1)), 'Максимальный срок - 1 месяц')
    .required('Дата возврата обязательна')
})

export const copySchema = yup.object({
  book_id: yup
    .number()
    .required('Выберите книгу'),
  location: yup
    .string()
    .max(100, 'Местоположение слишком длинное')
    .nullable()
})

export const copyBulkSchema = yup.object({
  book_id: yup
    .number()
    .required('Выберите книгу'),
  count: yup
    .number()
    .min(1, 'Количество должно быть больше 0')
    .max(100, 'Не более 100 экземпляров за раз')
    .required('Количество обязательно'),
  location: yup
    .string()
    .max(100, 'Местоположение слишком длинное')
    .nullable()
})

export const userSchema = yup.object({
  email: yup
    .string()
    .email('Введите корректный email')
    .required('Email обязателен'),
  first_name: yup
    .string()
    .min(2, 'Имя должно содержать минимум 2 символа')
    .max(50, 'Имя слишком длинное')
    .required('Имя обязательно'),
  last_name: yup
    .string()
    .min(2, 'Фамилия должна содержать минимум 2 символа')
    .max(50, 'Фамилия слишком длинная')
    .required('Фамилия обязательна'),
  middle_name: yup
    .string()
    .max(50, 'Отчество слишком длинное')
    .nullable(),
  phone: yup
    .string()
    .matches(PHONE_REGEX, 'Введите корректный номер телефона')
    .nullable()
})

export const passwordChangeSchema = yup.object({
  current_password: yup
    .string()
    .required('Текущий пароль обязателен'),
  new_password: yup
    .string()
    .min(6, 'Новый пароль должен содержать минимум 6 символов')
    .required('Новый пароль обязателен'),
  new_password_confirm: yup
    .string()
    .oneOf([yup.ref('new_password')], 'Пароли не совпадают')
    .required('Подтверждение пароля обязательно')
})