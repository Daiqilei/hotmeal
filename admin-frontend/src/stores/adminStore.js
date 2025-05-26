/**
 * @file            src/stores/adminStore.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useAdminStore = defineStore('admin', () => {
  const stats = ref({})
  const chartData = ref({})
  const filters = reactive({
    dateRange: [],
    categoryId: null,
  })

  function setStats(data) {
    stats.value = data
  }

  function setChartData(data) {
    chartData.value = data
  }

  function updateFilter(key, value) {
    filters[key] = value
  }

  function resetFilters() {
    filters.dateRange = []
    filters.categoryId = null
  }

  return {
    stats,
    chartData,
    filters,
    setStats,
    setChartData,
    updateFilter,
    resetFilters,
  }
})
