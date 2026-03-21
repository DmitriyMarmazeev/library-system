<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Загрузка -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-center py-12">
      <ExclamationCircleIcon class="h-16 w-16 text-red-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Ошибка загрузки</h3>
      <p class="text-gray-600">{{ error }}</p>
      <router-link to="/admin/books" class="mt-4 inline-block text-blue-600 hover:text-blue-800">
        ← Вернуться к списку
      </router-link>
    </div>

    <!-- Детали книги -->
    <div v-else-if="book" class="space-y-6">
      <!-- Заголовок -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-white mb-2">{{ book.title }}</h1>
              <p class="text-blue-100 text-lg">
                {{ authorNames }}
              </p>
            </div>
            <div class="flex gap-2">
              <router-link
                :to="`/admin/books/${book.id}/edit`"
                class="bg-white text-yellow-600 px-4 py-2 rounded-lg hover:bg-gray-100 transition flex items-center gap-2"
              >
                <PencilIcon class="h-5 w-5" />
                Редактировать
              </router-link>
              <button
                @click="confirmDelete"
                class="bg-white text-red-600 px-4 py-2 rounded-lg hover:bg-gray-100 transition flex items-center gap-2"
              >
                <TrashIcon class="h-5 w-5" />
                Удалить
              </button>
            </div>
          </div>
        </div>

        <!-- Основная информация -->
        <div class="p-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Левая колонка: детали -->
            <div class="lg:col-span-2 space-y-6">
              <!-- Аннотация -->
              <div v-if="book.description">
                <h2 class="text-xl font-semibold text-gray-900 mb-3">Аннотация</h2>
                <p class="text-gray-700 leading-relaxed">{{ book.description }}</p>
              </div>

              <!-- Детали -->
              <div>
                <h2 class="text-xl font-semibold text-gray-900 mb-3">Детали</h2>
                <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-if="book.isbn">
                    <dt class="text-sm text-gray-500">ISBN</dt>
                    <dd class="text-sm font-medium text-gray-900">{{ book.isbn }}</dd>
                  </div>
                  <div v-if="book.publication_year">
                    <dt class="text-sm text-gray-500">Год издания</dt>
                    <dd class="text-sm font-medium text-gray-900">{{ book.publication_year }}</dd>
                  </div>
                  <div v-if="book.publisher">
                    <dt class="text-sm text-gray-500">Издательство</dt>
                    <dd class="text-sm font-medium text-gray-900">{{ book.publisher }}</dd>
                  </div>
                  <div v-if="book.pages">
                    <dt class="text-sm text-gray-500">Количество страниц</dt>
                    <dd class="text-sm font-medium text-gray-900">{{ book.pages }}</dd>
                  </div>
                </dl>
              </div>

              <!-- Жанры -->
              <div v-if="book.genres && book.genres.length > 0">
                <h2 class="text-xl font-semibold text-gray-900 mb-3">Жанры</h2>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="genre in book.genres"
                    :key="genre.id"
                    class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                  >
                    {{ genre.name }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Правая колонка: статистика -->
            <div class="lg:col-span-1">
              <div class="bg-gray-50 rounded-lg p-6 sticky top-6">
                <h2 class="text-lg font-semibold text-gray-900 mb-4">Статистика</h2>
                
                <dl class="space-y-4">
                  <div>
                    <dt class="text-sm text-gray-500">Всего экземпляров</dt>
                    <dd class="text-2xl font-bold text-gray-900">{{ book.total_copies || 0 }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm text-gray-500">Доступно сейчас</dt>
                    <dd class="text-2xl font-bold text-green-600">{{ book.available_copies || 0 }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm text-gray-500">Выдано</dt>
                    <dd class="text-2xl font-bold text-yellow-600">
                      {{ (book.total_copies || 0) - (book.available_copies || 0) }}
                    </dd>
                  </div>
                </dl>

                <div class="mt-6 pt-6 border-t border-gray-200">
                  <router-link
                    :to="`/admin/copies?book=${book.id}`"
                    class="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center gap-1"
                  >
                    <CubeIcon class="h-4 w-4" />
                    Управление экземплярами →
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Экземпляры книги -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900">Экземпляры книги</h2>
          <button
            @click="showAddCopyModal = true"
            class="bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 transition text-sm flex items-center gap-1"
          >
            <PlusIcon class="h-4 w-4" />
            Добавить экземпляр
          </button>
        </div>

        <div class="p-6">
          <div v-if="copies.length > 0" class="space-y-3">
            <div
              v-for="copy in copies"
              :key="copy.id"
              class="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
            >
              <div class="flex items-center gap-4">
                <span class="text-sm font-medium text-gray-900">#{{ copy.id }}</span>
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    COPY_STATUS_COLORS[copy.status]
                  ]"
                >
                  {{ COPY_STATUS_LABELS[copy.status] }}
                </span>
                <span class="text-sm text-gray-500">{{ copy.location || 'Местоположение не указано' }}</span>
              </div>
              <div class="flex gap-2">
                <button
                  @click="editCopy(copy)"
                  class="text-yellow-600 hover:text-yellow-800"
                  title="Редактировать"
                >
                  <PencilIcon class="h-4 w-4" />
                </button>
                <button
                  @click="deleteCopy(copy)"
                  class="text-red-600 hover:text-red-800"
                  title="Удалить"
                >
                  <TrashIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            У этой книги пока нет экземпляров
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно удаления книги -->
    <AppModal
      v-model="showDeleteModal"
      title="Подтверждение удаления"
      :show-actions="true"
      confirm-variant="danger"
      confirm-text="Удалить"
      @confirm="handleDelete"
    >
      <p class="text-gray-700">
        Вы уверены, что хотите удалить книгу
        <span class="font-semibold">"{{ book?.title }}"</span>?
      </p>
      <p class="text-sm text-red-600 mt-2">
        Внимание! Это действие нельзя отменить. Все связанные экземпляры также будут удалены.
      </p>
    </AppModal>

    <!-- Модальное окно добавления экземпляра -->
    <AppModal
      v-model="showAddCopyModal"
      title="Добавление экземпляра"
      :show-actions="true"
      @confirm="handleAddCopy"
    >
      <form class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Местоположение
          </label>
          <input
            v-model="newCopy.location"
            type="text"
            class="input-field"
            placeholder="Например: Абонемент, ряд 3, полка 5"
          />
        </div>
      </form>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ExclamationCircleIcon } from '@heroicons/vue/24/outline'
import { booksApi } from '@/api/books'
import { useAuthStore } from '@/stores/auth'
import { formatFullName } from '@/utils/formatters'

const route = useRoute()
const router = useRouter()
const booksStore = useBooksStore()
const copiesStore = useCopiesStore()
const uiStore = useUIStore()

const bookId = parseInt(route.params.id)
const book = ref(null)
const copies = ref([])
const isLoading = ref(false)
const error = ref('')

const showDeleteModal = ref(false)
const showAddCopyModal = ref(false)

const newCopy = ref({
  location: ''
})

const authorNames = computed(() => {
  if (!book.value?.authors || book.value.authors.length === 0) {
    return 'Автор не указан'
  }
  return book.value.authors.map(a => formatFullName(a)).join(', ')
})

const fetchBook = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    book.value = await booksStore.fetchBookById(bookId)
    await fetchCopies()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки книги'
    console.error('Error fetching book:', err)
  } finally {
    isLoading.value = false
  }
}

const fetchCopies = async () => {
  try {
    const response = await copiesStore.fetchCopiesByBook(bookId, { limit: 100 })
    copies.value = response
  } catch (err) {
    console.error('Error fetching copies:', err)
  }
}

const confirmDelete = () => {
  showDeleteModal.value = true
}

const handleDelete = async () => {
  try {
    await booksStore.deleteBook(bookId)
    uiStore.success('Книга успешно удалена')
    router.push('/admin/books')
  } catch (err) {
    console.error('Error deleting book:', err)
    uiStore.error('Ошибка при удалении книги')
  }
}

const handleAddCopy = async () => {
  try {
    await copiesStore.createCopy({
      book_id: bookId,
      location: newCopy.value.location || null
    })
    uiStore.success('Экземпляр успешно добавлен')
    showAddCopyModal.value = false
    newCopy.value.location = ''
    await fetchCopies()
  } catch (err) {
    console.error('Error adding copy:', err)
    uiStore.error('Ошибка при добавлении экземпляра')
  }
}

const editCopy = (copy) => {
  // TODO: Редактирование экземпляра
  uiStore.info('Функция редактирования экземпляра будет доступна позже')
}

const deleteCopy = async (copy) => {
  if (confirm('Вы уверены, что хотите удалить этот экземпляр?')) {
    try {
      await copiesStore.deleteCopy(copy.id)
      uiStore.success('Экземпляр успешно удален')
      await fetchCopies()
    } catch (err) {
      console.error('Error deleting copy:', err)
      uiStore.error('Ошибка при удалении экземпляра')
    }
  }
}

onMounted(() => {
  fetchBook()
})
</script>