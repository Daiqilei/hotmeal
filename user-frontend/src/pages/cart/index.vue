<!--
 * @file         src/pages/cart/index.vue
 * @author       taichilei
 * @date         2025-04-30
 * @description  The cart page of the application.
-->

<!-- src/pages/cart -->

<template>
  <view class="cart-page">
    <scroll-view class="cart-list" scroll-y="true">
      <view v-for="item in cartList" :key="item.dishId">
        <CartItem
            :item="item"
            @decrease="() => decreaseQuantity(item.dishId)"
            @delete="() => removeItem(item.dishId)"
            @increase="() => increaseQuantity(item.dishId)"
        />
      </view>
    </scroll-view>
    <view class="checkout-bar-fixed">
      <text>总价: {{ totalPrice }}</text>
      <u-button type="primary" @click="handleCheckout">去结算</u-button>
    </view>
  </view>
</template>

<script setup>
import {useCartStore} from '@/stores/cart'
import {useOrderStore} from '@/stores/order'
import {computed, onMounted, watch} from 'vue'
import CartItem from './components/CartItem.vue'

const cartStore = useCartStore()
const cartList = computed(() => cartStore.cartList)
const orderStore = useOrderStore()
const totalPrice = computed(() => cartStore.totalPrice)

function handleCheckout() {
  console.log('[checkout] 开始检查购物车')

  if (cartStore.cartList.length === 0) {
    uni.showToast({title: '购物车为空', icon: 'none'})
    console.log('[checkout] 购物车为空，终止跳转')
    return
  }

  console.log('[checkout] 当前购物车数据:', cartStore.cartList)

  const dishList = cartStore.cartList.map(item => ({
    dish_id: item.dishId,
    quantity: item.quantity
  }))

  console.log('[checkout] 构造后的 dishList:', dishList)

  orderStore.setDraftOrderData(dishList, null)  // area_id 暂为 null
  orderStore.setDraftDisplayList(cartStore.cartList)

  console.log('[checkout] 即将跳转至: /pages/order/pay')

  uni.navigateTo({
    url: '/pages/order/pay'
  })
}

const increaseQuantity = (dishId) => {
  cartStore.increaseQuantity(dishId)
}

const decreaseQuantity = (dishId) => {
  cartStore.decreaseQuantity(dishId)
}

const removeItem = (dishId) => {
  cartStore.removeFromCart(dishId)
}

onMounted(() => {
  console.log('[cart] 当前购物车项目数量:', cartList.value.length)
  cartList.value.forEach(item => {
    console.log('[cart] 购物车项内容:', item)
  })
})

watch(cartList, (newList) => {
  console.log('[cart] 购物车变更:', newList)
}, {deep: true})
</script>


<style scoped>
.cart-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: relative;
}

.cart-list {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 120rpx; /* 给底部按钮留空间 */
}

.checkout-bar-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 20rpx 30rpx;
  box-shadow: 0 -2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}
</style>