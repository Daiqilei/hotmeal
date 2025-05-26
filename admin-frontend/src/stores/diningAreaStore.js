/**
 * @file            src/stores/diningAreaStore.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useDiningAreaStore = defineStore('diningArea', () => {
  const areaList = ref([])
  const selectedAreaId = ref(null)
  const searchKeyword = ref('')
  const pagination = reactive({
    page: 1,
    pageSize: 10,
  })
  const total = ref(0)

  function setAreaList(areas) {
    areaList.value = areas
  }

  function setSelectedArea(id) {
    selectedAreaId.value = id
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
    selectedAreaId.value = null
    searchKeyword.value = ''
    pagination.page = 1
    pagination.pageSize = 10
  }

  return {
    areaList,
    selectedAreaId,
    searchKeyword,
    pagination,
    total,
    setAreaList,
    setSelectedArea,
    setSearchKeyword,
    setPagination,
    setTotal,
    resetFilters,
  }
})
