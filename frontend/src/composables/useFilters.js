import { ref, computed, watch } from 'vue'
import { debounce } from '@/utils/helpers'

export function useFilters(options = {}) {
  const {
    initialFilters = {},
    debounceDelay = 300,
    onFilterChange = null
  } = options

  const filters = ref({ ...initialFilters })
  const searchQuery = ref('')

  const activeFiltersCount = computed(() => {
    return Object.values(filters.value).filter(v => 
      v !== null && v !== undefined && v !== ''
    ).length
  })

  const hasActiveFilters = computed(() => activeFiltersCount.value > 0)

  const setFilter = (key, value) => {
    filters.value = {
      ...filters.value,
      [key]: value
    }
  }

  const removeFilter = (key) => {
    const newFilters = { ...filters.value }
    delete newFilters[key]
    filters.value = newFilters
  }

  const resetFilters = () => {
    filters.value = { ...initialFilters }
    searchQuery.value = ''
  }

  const clearSearch = () => {
    searchQuery.value = ''
  }

  // Debounced filter change handler
  const debouncedFilterChange = debounce(() => {
    if (onFilterChange) {
      onFilterChange({
        filters: filters.value,
        search: searchQuery.value
      })
    }
  }, debounceDelay)

  // Watch for changes
  watch([filters, searchQuery], () => {
    debouncedFilterChange()
  }, { deep: true })

  return {
    filters,
    searchQuery,
    activeFiltersCount,
    hasActiveFilters,
    setFilter,
    removeFilter,
    resetFilters,
    clearSearch
  }
}