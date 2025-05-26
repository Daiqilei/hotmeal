<template>
  <view class="main-container">
    <view class="sidebar-wrapper">
      <view class="nav-like-button" @click="handleSpecialCategoryClick('featured')">
        🌟 精选
      </view>
      <CategorySidebar
          :active-id="activeCategoryId"
          @select="handleCategoryChange"
      />
    </view>
    <scroll-view class="scroll-container" scroll-y>
      <view class="page">
        <Navbar title="点餐菜单"/>
        <u-list>
          <u-list-item v-for="(dish, index) in filteredDishes" :key="dish.name">
            <DishCard :dish="dish" @add-to-cart="addToCart"/>
          </u-list-item>
        </u-list>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import DishCard from './components/DishCard.vue'
import CategorySidebar from './components/CategorySidebar.vue'
import Navbar from '@/components/Navbar.vue'
import {useCartStore} from '@/stores/cart'
import {getDishList} from '@/api/dish'
import {getRecommendations} from '@/api/recommend'

const cartStore = useCartStore()

const activeCategoryId = ref(null)
const allDishes = ref([])
const recommendedDishes = ref([])

function addToCart(dish) {
  if (!dish.dish_id) {
    console.warn('尝试加入的不是菜品，忽略:', dish)
    return
  }
  cartStore.addToCart(dish)
  uni.showToast({
    title: `已加入购物车: ${dish.name}`,
    icon: 'success',
  })
}

async function handleCategoryChange(id) {
  activeCategoryId.value = id
  if (id === 'recommend') {
    const res = await getRecommendations()
    recommendedDishes.value = (res.data || []).filter(d =>
        typeof d.dish_id === 'number' &&
        typeof d.name === 'string' && d.name.trim() !== '' &&
        typeof d.price === 'string' && d.price.trim() !== ''
    )
  } else {
    const res = await getDishList({category_id: id})
    allDishes.value = (res.data || []).filter(d =>
        typeof d.dish_id === 'number' &&
        typeof d.name === 'string' && d.name.trim() !== '' &&
        typeof d.price === 'string' && d.price.trim() !== ''
    )
  }
}

onMounted(async () => {
  const res = await getDishList()
  allDishes.value = (res.data || []).filter(d =>
      typeof d.dish_id === 'number' &&
      typeof d.name === 'string' && d.name.trim() !== '' &&
      typeof d.price === 'string' && d.price.trim() !== ''
  )
})

async function handleSpecialCategoryClick(id) {
  console.log('点击精选按钮，当前 activeCategoryId:', activeCategoryId.value, '即将设置为:', id)
  activeCategoryId.value = id
  const res = await getDishList()
  console.log('[getDishList 返回]', res.data)
  recommendedDishes.value = (res.data || []).filter(d =>
      typeof d.dish_id === 'number' &&
      typeof d.name === 'string' && d.name.trim() !== '' &&
      typeof d.price === 'string' && d.price.trim() !== ''
  )
}

const filteredDishes = computed(() => {
  if (activeCategoryId.value === 'recommend' || activeCategoryId.value === 'featured') {
    return recommendedDishes.value
  }
  return allDishes.value
})
</script>

<style scoped>
.main-container {
  display: flex;
  height: 100vh;
}

.sidebar-wrapper {
  width: 200rpx;
  background-color: #f5f5f5;
}

.scroll-container {
  flex: 1;
  overflow-y: auto;
}

.page {
  padding: 0 20rpx 20rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  box-sizing: border-box;
  min-height: 100%;
}

.dish-image {
  width: 100%;
  height: 180rpx;
  border-radius: 12rpx;
  object-fit: cover;
  margin-bottom: 10rpx;
}
</style>
.nav-like-button {
height: 88rpx;
line-height: 88rpx;
text-align: center;
color: #666;
font-size: 24rpx;
background-color: #fff;
border-bottom: 1px solid #eee;
}
.nav-like-button:active {
background-color: #f0f0f0;
}
.top-action-button {
padding: 20rpx;
background-color: #ffffff;
text-align: center;
border-bottom: 1px solid #ddd;
font-weight: bold;
color: #333;
}
.top-action-button:hover {
background-color: #f0f0f0;
}