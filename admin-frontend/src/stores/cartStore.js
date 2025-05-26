/**
 * @file            cartStore.js
 * @description
 * @author          taichilei
 * @date            2025-04-24
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // 使用组合式 API 定义状
  //直接在函数内使用 ref() 定义响应式状态
  const items = ref([]) // 购物车商品列表
  //用 computed() 定义计算属性
  const count = computed(() => items.value.length)
  // actions 可以用函数定义
  //用普通函数定义操作
  function addItem(product) {
    items.value.push(product)
  }
  function removeItem(productId) {
    items.value = items.value.filter((item) => item.id !== productId)
  }
  // 暴露 state 和 actions
  return { items, count, addItem, removeItem }
})
