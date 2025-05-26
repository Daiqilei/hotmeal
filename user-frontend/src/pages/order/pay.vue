<!--
 * @file         src/pages/order/pay.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  支付页，展示订单信息、支付金额，选择支付方式并确认支付
-->

<!-- src/pages/order -->

<template>
  <view class="pay-page">
    <Navbar title="支付订单"/>
    <view style="height: 64px;"/>

    <view v-if="orderStore.draftDisplayList && orderStore.draftDisplayList.length" class="order-items">
      <view v-for="(item, index) in orderStore.draftDisplayList" :key="index" class="item">
        <text>菜名：{{ item.name }}</text>
      </view>
    </view>
    <view v-else>
      <text>加载中或无数据：</text>
      <text>{{ orderStore.draftDisplayList }}</text>
    </view>

    <!--
    <view class="payment-methods">
      <u-radio-group v-model="paymentMethod">
        <u-radio label="微信支付" name="微信支付"/>
        <u-radio label="支付宝" name="支付宝"/>
      </u-radio-group>
    </view>
    -->

    <view class="order-price">需支付金额：¥{{ totalPrice }}</view>

    <view class="pay-button-wrapper">
      <u-button type="primary" @click="handlePay">确认支付</u-button>
    </view>
  </view>
</template>

<script setup>
console.log('[pay.vue] 页面加载中...')
import {computed, ref, watchEffect} from 'vue'
import {onShow} from '@dcloudio/uni-app'
import {useUserStore} from '@/stores/user'
import {useOrderStore} from '@/stores/order'
import Navbar from '@/components/Navbar.vue'
import {requireLogin} from '@/utils/auth'


const userStore = useUserStore()
const orderStore = useOrderStore()

const paymentMethod = ref('微信支付')

// 登录检查
onShow(() => {
  if (!requireLogin()) {
    uni.showToast({
      title: 'login required',
      icon: 'none',
      duration: 2000
    })
    uni.switchTab({url: '/pages/index'})
  }
})

watchEffect(() => {
  console.log('[pay.vue] 当前展示菜品列表:', orderStore.draftDisplayList)
})

const totalPrice = computed(() =>
    orderStore.draftDisplayList.reduce((sum, item) => {
      return sum + item.price * item.quantity
    }, 0).toFixed(2)
)

const handlePay = async () => {
  try {
    // 模拟支付成功后跳转
    uni.showToast({title: '支付成功', icon: 'success'})
    setTimeout(() => {
      const orderId = 'mock-1234'
      uni.redirectTo({url: `/pages/order/detail?order_id=${orderId}`})
      orderStore.clearDraftOrder()
    }, 1000)

    // TODO: 启用后端接口请求时取消注释
    /*
    const res = await uni.request({
      url: 'http://localhost:5000/api/orders',
      method: 'POST',
      data: {
        dish_list: orderStore.draftOrder.dish_list,
        area_id: orderStore.draftOrder.area_id,
        payment_method: paymentMethod.value,
        image_url: null
      },
      header: {
        Authorization: `Bearer ${userStore.token}`
      }
    })

    if (res[1].statusCode === 201) {
      const orderId = res[1].data.data.order_id
      uni.showToast({title: '支付成功', icon: 'success'})
      setTimeout(() => {
        uni.redirectTo({url: `/pages/order/detail?order_id=${orderId}`})
        orderStore.clearDraftOrder()
      }, 1000)
    } else {
      throw new Error(res[1].data.message || '提交失败')
    }
    */
  } catch (err) {
    uni.showToast({title: '支付失败', icon: 'none'})
  }
}
</script>

<style scoped>
.pay-page {
  padding: 20rpx;
  padding-top: 40rpx;
}

.order-items {
  margin-bottom: 30rpx;
}

.item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.thumb {
  width: 80rpx;
  height: 80rpx;
  border-radius: 8rpx;
  margin-right: 20rpx;
}

.info {
  flex: 1;
}

.name {
  font-size: 28rpx;
  font-weight: bold;
}

.meta {
  font-size: 24rpx;
  color: #888;
}

.price {
  font-size: 28rpx;
  color: #e54d42;
}

.payment-methods {
  margin-bottom: 20rpx;
}

.order-price {
  font-size: 32rpx;
  font-weight: bold;
  margin: 30rpx 0;
  text-align: right;
  color: #333;
}

.pay-button-wrapper {
  margin-top: 30rpx;
}
</style>

// 全局页面级异常捕获
onError((err) => {
console.error('[pay.vue] 页面渲染层捕获错误：', err)
})