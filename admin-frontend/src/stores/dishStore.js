/**
 * @file            src/stores/dishStore.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import { defineStore } from 'pinia'

export const useDishStore = defineStore('dish', {
  state: () => ({
    dishList: [],
    selectedCategoryId: null,
    searchKeyword: '',
    pagination: {
      page: 1,
      pageSize: 10,
    },
    total: 0,
  }),
  actions: {
    setDishList(dishes) {
      this.dishList = dishes
    },
    setSelectedCategory(id) {
      this.selectedCategoryId = id
    },
    setSearchKeyword(keyword) {
      this.searchKeyword = keyword
    },
    setPagination(page, pageSize) {
      this.pagination.page = page
      this.pagination.pageSize = pageSize
    },
    setTotal(total) {
      this.total = total
    },
    resetFilters() {
      this.selectedCategoryId = null
      this.searchKeyword = ''
      this.pagination = {
        page: 1,
        pageSize: 10,
      }
    },
  },
})
