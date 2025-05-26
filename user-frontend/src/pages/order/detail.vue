<!--
 * @file         src/pages/order/detail.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  订单详情页
-->

<!-- src/pages/order -->

<template>
  <Loading :show="isLoading" text="加载订单详情中..."/>
  <view v-if="order" class="order-detail-page">
    <Navbar title="订单详情"/>
    <view style="height: 64px;"/>
    <view class="order-info">
      <view class="order-id">订单号：{{ order.order_id }}</view>
      <view class="order-status">{{ order.state }}</view>
    </view>

    <view class="order-items">
      <view v-for="(item, index) in order.items" :key="index" class="item">
        <image :src="item.image_url" class="item-image" mode="aspectFill"/>
        <view class="item-info">
          <view class="item-name">{{ item.dish_name }}</view>
          <view class="item-quantity">x{{ item.quantity }}</view>
        </view>
        <view class="item-price">¥{{ item.total_price }}</view>
      </view>
    </view>

    <view class="order-summary">
      <view>支付方式：{{ order.payment_method }}</view>
      <view>总价：¥{{ order.price }}</view>
      <view>下单时间：{{ order.created_at }}</view>
    </view>
    <view v-if="order.state === 'PENDING'" class="cancel-button-wrapper">
      <u-button text="取消订单" type="error" @click="handleCancelOrder"/>
    </view>
  </view>
  <view v-else>
    <view style="padding: 40rpx; text-align: center; color: #999;">加载失败</view>
  </view>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Loading from '@/components/Loading.vue'
import {ref} from 'vue'
import {onLoad} from '@dcloudio/uni-app'
import {useUserStore} from '@/stores/user'

const order = ref(null)
const isLoading = ref(true)
const userStore = useUserStore()

onLoad(async (query) => {
  const orderId = query.order_id
  // try {
  //   const res = await uni.request({
  //     url: `http://localhost:5000/api/orders/${orderId}`,
  //     method: 'GET',
  //     header: {
  //       Authorization: `Bearer ${userStore.token}`
  //     }
  //   })
  //   if (res[1].statusCode === 200) {
  //     order.value = res[1].data.data
  //   } else {
  //     uni.showToast({title: '订单加载失败', icon: 'none'})
  //   }
  // } catch (err) {
  //   uni.showToast({title: '网络错误', icon: 'none'})
  // } finally {
  //   isLoading.value = false
  // }

  // 模拟数据用于测试跳转流程
  order.value = {
    order_id: orderId,
    state: 'PAID',
    payment_method: '微信支付',
    price: 58.8,
    created_at: '2025-04-30 15:00',
    items: [
      {dish_name: '红烧牛肉', quantity: 1, total_price: 28.8, image_url: '/static/dish/beef.jpg'},
      {dish_name: '鱼香肉丝', quantity: 2, total_price: 30.0, image_url: '/static/dish/pork.jpg'}
    ]
  }
  isLoading.value = false
})

const handleCancelOrder = async () => {
  uni.showModal({
    title: '提示',
    content: '确定要取消该订单吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const cancelRes = await uni.request({
            url: `http://localhost:5000/api/orders/${order.value.order_id}/cancel`,
            method: 'POST',
            header: {
              Authorization: `Bearer ${userStore.token}`
            }
          })
          if (cancelRes[1].statusCode === 200) {
            uni.showToast({title: '订单已取消', icon: 'success'})
            order.value.state = 'CANCELED'
          } else {
            uni.showToast({title: '取消失败', icon: 'none'})
          }
        } catch (err) {
          uni.showToast({title: '网络错误', icon: 'none'})
        }
      }
    }
  })
}
</script>

<style scoped>
.order-detail-page {
  padding: 20rpx;
}

.order-info {
  margin-bottom: 30rpx;
}

.order-id {
  font-size: 28rpx;
  color: #333;
}

.order-status {
  font-size: 26rpx;
  color: #4caf50;
  margin-top: 10rpx;
}

.order-items {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 30rpx;
}

.item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.item-image {
  width: 100rpx;
  height: 100rpx;
  border-radius: 8rpx;
  margin-right: 20rpx;
  object-fit: cover;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 28rpx;
}

.item-quantity {
  font-size: 24rpx;
  color: #999;
  margin-top: 6rpx;
}

.item-price {
  font-size: 28rpx;
  color: #e54d42;
}

.order-summary {
  font-size: 26rpx;
  color: #666;
  line-height: 2;
}

.cancel-button-wrapper {
  margin-top: 40rpx;
}
</style>