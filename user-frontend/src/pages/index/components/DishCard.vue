<!--
 * @file         src/pages/index/components/DishCard.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  The component of dish card in index page.
-->

<!-- src/pages/index/components -->

<template>
  <view class="dish-card" @click="goToDetail">
    <image :src="dish.imageUrl" class="dish-image" mode="aspectFill"/>
    <view class="dish-info">
      <view class="dish-name">{{ dish.name }}</view>
      <view class="dish-desc">{{ dish.description }}</view>
      <view class="dish-bottom">
        <view class="dish-price">￥{{ dish.price }}</view>
        <view class="add-button" @click.stop="addToCart">+</view>
      </view>
    </view>
  </view>
</template>

<script setup>

const props = defineProps({
  dish: {
    type: Object,
    required: true
  }
})

// 调试：输出接收到的 dish 数据
console.log('[DishCard] 接收到 dish:', props.dish)

const emit = defineEmits(['add-to-cart'])

const goToDetail = () => {
  uni.navigateTo({
    url: `/pages/dish/detail?dishId=${props.dish.dishId}`
  })
}

const addToCart = () => {
  if (
      !props.dish ||
      typeof props.dish.dishId !== 'number' ||
      !props.dish.name
  ) {
    console.warn('[DishCard] ⚠️ 非法 dish 数据，已阻止加入购物车：', props.dish)
    return
  }
  emit('add-to-cart', props.dish)
}
</script>

<style scoped>
.dish-card {
  display: flex;
  align-items: center;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 30rpx;
  background-color: #fff;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.05);
  height: 180rpx;
}

.dish-image {
  width: 180rpx;
  height: 180rpx;
  object-fit: cover;
  flex-shrink: 0; /* 防止图片被压缩 */
}

.dish-info {
  flex: 1;
  padding: 16rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.dish-name {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.dish-desc {
  font-size: 26rpx;
  color: #888;
  margin-bottom: 10rpx;
}

.dish-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dish-price {
  font-size: 28rpx;
  color: #e54d42;
  font-weight: 500;
}

.add-button {
  width: 60rpx;
  height: 60rpx;
  line-height: 60rpx;
  text-align: center;
  background-color: #e54d42;
  color: #fff;
  font-size: 40rpx;
  border-radius: 30rpx;
  user-select: none;
}
</style>