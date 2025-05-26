<!--
 * @file         src/pages/cart/components/CartItem.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  购物车项组件，展示菜品图片、名称、价格和数量，支持增加、减少数量及删除操作
-->

<!-- src/pages/cart/components -->

<template>
  <view class="cart-item">
    <image :src="item.imageUrl" class="item-image" mode="aspectFill"/>
    <view class="item-info">
      <view class="item-header">
        <view class="item-name">{{ item.name }}</view>
        <u-icon name="trash" size="36" @click="handleDelete"/>
      </view>
      <view class="item-bottom">
        <view class="item-price">¥{{ item.price }}</view>
        <view class="item-quantity-control">
          <u-icon name="minus-circle" size="32" @click="decreaseQuantity"/>
          <text class="quantity">{{ item.quantity }}</text>
          <u-icon name="plus-circle" size="32" @click="increaseQuantity"/>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['increase', 'decrease', 'delete'])

const increaseQuantity = () => {
  emit('increase')
}

const decreaseQuantity = () => {
  emit('decrease')
}

const handleDelete = () => {
  emit('delete')
}
</script>

<style scoped>
.cart-item {
  display: flex;
  padding: 20rpx;
  background-color: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 20rpx;
}

.item-image {
  width: 120rpx;
  height: 120rpx;
  border-radius: 8rpx;
  margin-right: 20rpx;
  object-fit: cover;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-name {
  font-size: 28rpx;
  font-weight: bold;
}

.item-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-price {
  color: #e54d42;
  font-size: 28rpx;
}

.item-quantity-control {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.quantity {
  font-size: 28rpx;
  min-width: 40rpx;
  text-align: center;
}
</style>