/**
 * @file            src/stores/categoryStore.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useCategoryStore = defineStore('category', () => {
  const categoryList = ref([])
  const selectedCategoryId = ref(null)
  const searchKeyword = ref('')
  const pagination = reactive({
    page: 1,
    pageSize: 10,
  })
  const total = ref(0)

  function setCategoryList(categories) {
    categoryList.value = categories
  }

  function setSelectedCategory(id) {
    selectedCategoryId.value = id
  }

  function setSearchKeyword(keyword) {
    searchKeyword.value = keyword
  }

  function setPagination(page, pageSize) {
    pagination.page = page
    pagination.pageSize = pageSize
  }

  function setTotal(val) {
    total.value = val
  }

  function resetFilters() {
    selectedCategoryId.value = null
    searchKeyword.value = ''
    pagination.page = 1
    pagination.pageSize = 10
  }

  return {
    categoryList,
    selectedCategoryId,
    searchKeyword,
    pagination,
    total,
    setCategoryList,
    setSelectedCategory,
    setSearchKeyword,
    setPagination,
    setTotal,
    resetFilters,
  }
})
