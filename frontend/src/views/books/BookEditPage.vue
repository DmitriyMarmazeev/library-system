<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Редактирование книги</h1>
      <p class="text-gray-600 mt-2">
        Измените информацию о книге
      </p>
    </div>

    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Форма -->
    <div v-else-if="book" class="bg-white rounded-lg shadow-sm p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Название -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Название книги <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            class="input-field"
            :class="{ 'border-red-500': errors.title }"
            placeholder="Введите название"
          />
          <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
        </div>

        <!-- Авторы -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Авторы <span class="text-red-500">*</span>
          </label>
          <div class="space-y-3">
            <div
              v-for="(author, index) in form.author_ids"
              :key="index"
              class="flex gap-2"
            >
              <select
                v-model="form.author_ids[index]"
                class="input-field flex-1"
                :class="{ 'border-red-500': errors.author_ids }"
              >
                <option value="">Выберите автора</option>
                <option
                  v-for="author in authors"
                  :key="author.id"
                  :value="author.id"
                >
                  {{ formatFullName(author) }}
                </option>
              </select>
              <button
                type="button"
                @click="removeAuthor(index)"
                class="text-red-600 hover:text-red-800"
              >
                <XMarkIcon class="h-5 w-5" />
              </button>
            </div>
            
            <button
              type="button"
              @click="addAuthor"
              class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
            >
              <PlusIcon class="h-4 w-4" />
              Добавить автора
            </button>
          </div>
          <p v-if="errors.author_ids" class="mt-1 text-sm text-red-600">{{ errors.author_ids }}</p>
        </div>

        <!-- Жанры -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Жанры
          </label>
          <div class="space-y-3">
            <div
              v-for="(genre, index) in form.genre_ids"
              :key="index"
              class="flex gap-2"
            >
              <select
                v-model="form.genre_ids[index]"
                class="input-field flex-1"
              >
                <option value="">Выберите жанр</option>
                <option
                  v-for="genre in genres"
                  :key="genre.id"
                  :value="genre.id"
                >
                  {{ genre.name }}
                </option>
              </select>
              <button
                type="button"
                @click="removeGenre(index)"
                class="text-red-600 hover:text-red-800"
              >
                <XMarkIcon class="h-5 w-5" />
              </button>
            </div>
            
            <button
              type="button"
              @click="addGenre"
              class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
            >
              <PlusIcon class="h-4 w-4" />
              Добавить жанр
            </button>
          </div>
        </div>

        <!-- ISBN -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            ISBN
          </label>
          <input
            v-model="form.isbn"
            type="text"
            class="input-field"
            :class="{ 'border-red-500': errors.isbn }"
            placeholder="978-5-699-12345-6"
          />
          <p v-if="errors.isbn" class="mt-1 text-sm text-red-600">{{ errors.isbn }}</p>
        </div>

        <!-- Издательство и год -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Издательство
            </label>
            <input
              v-model="form.publisher"
              type="text"
              class="input-field"
              placeholder="Название издательства"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Год издания
            </label>
            <input
              v-model.number="form.publication_year"
              type="number"
              class="input-field"
              :class="{ 'border-red-500': errors.publication_year }"
              placeholder="2024"
              min="1400"
              :max="new Date().getFullYear()"
            />
            <p v-if="errors.publication_year" class="mt-1 text-sm text-red-600">{{ errors.publication_year }}</p>
          </div>
        </div>

        <!-- Количество страниц -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Количество страниц
          </label>
          <input
            v-model.number="form.pages"
            type="number"
            class="input-field"
            :class="{ 'border-red-500': errors.pages }"
            placeholder="300"
            min="1"
          />
          <p v-if="errors.pages" class="mt-1 text-sm text-red-600">{{ errors.pages }}</p>
        </div>

        <!-- Описание -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Описание
          </label>
          <textarea
            v-model="form.description"
            rows="5"
            class="input-field"
            placeholder="Краткое описание книги..."
          ></textarea>
        </div>

        <!-- Кнопки -->
        <div class="flex justify-end gap-4 pt-4">
          <router-link
            :to="`/admin/books/${bookId}`"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
          >
            Отмена
          </router-link>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PlusIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { useBooksStore } from '@/stores/books'
import { useUIStore } from '@/stores/ui'
import { bookSchema } from '@/utils/validators'
import { formatFullName } from '@/utils/formatters'
import * as yup from 'yup'

const route = useRoute()
const router = useRouter()
const booksStore = useBooksStore()
const uiStore = useUIStore()

const bookId = parseInt(route.params.id)
const book = ref(null)
const authors = ref([])
const genres = ref([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const errors = ref({})

const form = reactive({
  title: '',
  author_ids: [],
  genre_ids: [],
  isbn: '',
  publisher: '',
  publication_year: null,
  pages: null,
  description: ''
})

const fetchBook = async () => {
  isLoading.value = true
  try {
    book.value = await booksStore.fetchBookById(bookId)
    
    // Заполняем форму
    form.title = book.value.title
    form.author_ids = book.value.authors?.map(a => a.id) || []
    form.genre_ids = book.value.genres?.map(g => g.id) || []
    form.isbn = book.value.isbn || ''
    form.publisher = book.value.publisher || ''
    form.publication_year = book.value.publication_year || null
    form.pages = book.value.pages || null
    form.description = book.value.description || ''
  } catch (error) {
    console.error('Error fetching book:', error)
    uiStore.error('Ошибка загрузки книги')
    router.push('/admin/books')
  } finally {
    isLoading.value = false
  }
}

const fetchData = async () => {
  try {
    const [authorsRes, genresRes] = await Promise.all([
      booksStore.fetchAuthors({ limit: 1000 }),
      booksStore.fetchGenres({ limit: 1000 })
    ])
    authors.value = authorsRes
    genres.value = genresRes
  } catch (error) {
    console.error('Error fetching data:', error)
    uiStore.error('Ошибка загрузки данных')
  }
}

const addAuthor = () => {
  form.author_ids.push('')
}

const removeAuthor = (index) => {
  form.author_ids.splice(index, 1)
}

const addGenre = () => {
  form.genre_ids.push('')
}

const removeGenre = (index) => {
  form.genre_ids.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    errors.value = {}
    
    // Валидация
    await bookSchema.validate(form, { abortEarly: false })
    
    // Фильтруем пустые значения
    const submitData = {
      ...form,
      author_ids: form.author_ids.filter(id => id !== ''),
      genre_ids: form.genre_ids.filter(id => id !== '')
    }
    
    isSubmitting.value = true
    await booksStore.updateBook(bookId, submitData)
    uiStore.success('Книга успешно обновлена')
    router.push(`/admin/books/${bookId}`)
  } catch (err) {
    if (err instanceof yup.ValidationError) {
      const validationErrors = {}
      err.inner.forEach((error) => {
        validationErrors[error.path] = error.message
      })
      errors.value = validationErrors
    } else {
      console.error('Error updating book:', err)
      uiStore.error('Ошибка при обновлении книги')
    }
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchData()
  fetchBook()
})
</script>