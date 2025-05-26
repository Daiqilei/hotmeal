<!--
 * @file         src/pages/order/components/OrderCard.vue
 * @author       taichilei
 * @date         2025-04-30
 * @description  （这里补充页面/组件简要描述）
-->

<!-- src/pages/order/components -->

<template>
  <view class="order-card" @click="$emit('click', order.orderId)">
    <view class="order-header">
      <view class="order-id">订单号：{{ order.orderId }}</view>
      <view class="order-status">{{ order.status }}</view>
    </view>
    <view class="order-body">
      <view class="order-price">总价：¥{{ order.totalPrice }}</view>
      <view class="order-time">{{ order.createdAt }}</view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  order: Object
})
</script>

<style scoped>
.order-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.order-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10rpx;
}

.order-id {
  font-size: 28rpx;
  color: #333;
}

.order-status {
  font-size: 26rpx;
  color: #4caf50;
}

.order-body {
  display: flex;
  justify-content: space-between;
  font-size: 26rpx;
  color: #666;
}

.order-price {
  font-weight: bold;
}
</style>