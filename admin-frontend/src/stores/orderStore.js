/**
 * @file            src/stores/orderStore.js
 * @description
 * @author          taichilei
 * @date            2025-04-24
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './userStore'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])

  function placeOrder(orderData) {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) {
      throw new Error('请先登录！')
    }
    orderData.userId = userStore.userId
    orders.value.push(orderData)
  }

  function setOrders(orderList) {
    orders.value = orderList
  }

  function clearOrders() {
    orders.value = []
  }

  function removeOrder(orderId) {
    orders.value = orders.value.filter((order) => order.orderId !== orderId)
  }

  return {
    orders,
    placeOrder,
    setOrders,
    clearOrders,
    removeOrder,
  }
})
