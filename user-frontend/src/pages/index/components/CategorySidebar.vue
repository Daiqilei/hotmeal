<template>
  <view v-if="loading" class="loading">加载中...</view>
  <scroll-view v-else class="sidebar" scroll-y style="height: 100vh;">
    <view
        v-for="category in categories"
        :key="category.category_id"
        :class="{ active: category.category_id === activeId }"
        class="sidebar-item"
        @click="handleSelect(category.category_id)"
    >
      {{ category.name }}
    </view>
  </scroll-view>
</template>

<script setup>
import {defineEmits, defineProps, onMounted, ref} from 'vue'
import {getCategoryList} from '@/api/category' // 你需要自己实现此接口函数

const props = defineProps({
  activeId: {
    type: [String, Number],
    default: null
  }
})
const emits = defineEmits(['select'])

const categories = ref([])
const loading = ref(true)

const handleSelect = (id) => {
  emits('select', id)
}

onMounted(async () => {
  try {
    const res = await getCategoryList()
    const fetched = res.data || []
    console.log('分类接口数据', fetched)

    categories.value = [{category_id: 'recommend', name: '🔥 推荐'}]
    categories.value.push(...fetched)
    console.log('最终分类列表', categories.value)
  } catch (err) {
    uni.showToast({
      icon: 'none',
      title: '分类加载失败'
    })
    // categories.value = [
    //   {category_id: 'recommend', name: '🔥 推荐'}
    // ]
  } finally {
    if (!props.activeId && categories.value.length > 0) {
      emits('select', categories.value[0].category_id)
    }
    loading.value = false
  }
})
</script>

<style scoped>
.sidebar {
  width: 200rpx;
  background-color: #f5f5f5;
  height: 100%;
}

.sidebar-item {
  padding: 20rpx;
  text-align: center;
  color: #333;
  border-bottom: 1px solid #eee;
}

.sidebar-item.active {
  background-color: #ffffff;
  color: #007aff;
  font-weight: bold;
}

.loading {
  padding: 40rpx;
  text-align: center;
  color: #999;
}
</style>