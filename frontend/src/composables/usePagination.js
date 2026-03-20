import { ref, computed } from 'vue'
import { getPaginationRange } from '@/utils/helpers'

export function usePagination(options = {}) {
  const {
    initialPage = 1,
    initialPerPage = 10,
    initialTotal = 0
  } = options

  const currentPage = ref(initialPage)
  const perPage = ref(initialPerPage)
  const total = ref(initialTotal)

  const totalPages = computed(() => Math.ceil(total.value / perPage.value))

  const offset = computed(() => (currentPage.value - 1) * perPage.value)

  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const paginationRange = computed(() => 
    getPaginationRange(currentPage.value, totalPages.value)
  )

  const setPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  const nextPage = () => {
    if (hasNextPage.value) {
      currentPage.value++
    }
  }

  const prevPage = () => {
    if (hasPrevPage.value) {
      currentPage.value--
    }
  }

  const setPerPage = (newPerPage) => {
    perPage.value = newPerPage
    currentPage.value = 1 // ???????????????????? ???? ???????????? ????????????????
  }

  const setTotal = (newTotal) => {
    total.value = newTotal
  }

  const resetPagination = () => {
    currentPage.value = initialPage
    perPage.value = initialPerPage
    total.value = initialTotal
  }

  return {
    // State
    currentPage,
    perPage,
    total,
    
    // Computed
    totalPages,
    offset,
    hasNextPage,
    hasPrevPage,
    paginationRange,
    
    // Methods
    setPage,
    nextPage,
    prevPage,
    setPerPage,
    setTotal,
    resetPagination
  }
}