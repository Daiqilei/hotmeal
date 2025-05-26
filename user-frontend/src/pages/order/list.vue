<!--
 * @file         src/pages/order/list.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  订单列表页
-->

<!-- src/pages/order -->

<template>
  <view class="order-list-page">
    <Navbar title="我的订单"/>
    <view style="height: 64px;"/>
    <u-list>
      <u-list-item
          v-for="(order, index) in orderList"
          :key="index"
      >
        <OrderCard :order="order" @click="goToOrderDetail"/>
      </u-list-item>
    </u-list>
  </view>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {useUserStore} from '@/stores/user'
import Navbar from '@/components/Navbar.vue'
import {requireLogin} from '@/utils/auth'
import OrderCard from './components/OrderCard.vue'

const orderList = ref([])
const userStore = useUserStore()

const goToOrderDetail = (orderId) => {
  uni.navigateTo({
    url: `/pages/order/detail?order_id=${orderId}`
  })
}
onMounted(() => {
  if (!requireLogin()) return

  console.log("成功进入订单列表页")
  console.log('orderList', orderList.value)
  console.log(userStore.token)
  console.log(userStore.userInfo)

  // 使用 mock 数据测试展示结构
  orderList.value = [
    {
      orderId: 'mock-001',
      status: '待支付',
      totalPrice: 58.8,
      createdAt: '2025-04-30 12:00:00'
    },
    {
      orderId: 'mock-002',
      status: '已完成',
      totalPrice: 89.9,
      createdAt: '2025-04-29 14:30:00'
    },
    {
      orderId: 'mock-003',
      status: '已取消',
      totalPrice: 39.0,
      createdAt: '2025-04-28 09:45:00'
    }
  ]
})
</script>

<style scoped>
.order-list-page {
  padding: 20rpx;
}
</style>