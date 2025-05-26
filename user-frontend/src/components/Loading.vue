<!--
 * @file         src/components/Loading.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  （这里补充页面/组件简要描述）
-->

<!-- src/components -->

<template>
  <!-- 注释原来的内容以避免 u-loading 报错 -->
  <!--
  <view v-if="show" class="loading-overlay">
    <view class="loading-content">
      <u-loading :mode="mode" :size="size"/>
      <text class="loading-text">{{ text }}</text>
    </view>
  </view>
  -->
  <view v-if="false"></view> <!-- 占位避免报错 -->
</template>

<script setup>
defineProps({
  show: Boolean,
  text: {
    type: String,
    default: '加载中...'
  },
  mode: {
    type: String,
    default: 'circle'
  },
  size: {
    type: [String, Number],
    default: 40
  }
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-text {
  margin-top: 10rpx;
  font-size: 28rpx;
  color: #666;
}
</style>