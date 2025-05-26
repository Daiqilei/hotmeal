<!--
 * @file         src/pages/error/404.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  404错误页面，展示错误提示信息并提供返回首页按钮
-->

<!-- src/pages/error -->

<template>
  <view class="error-page">
    <Navbar title="页面未找到"/>
    <view style="height: 64px;"/>
    <view class="content">
      <view class="error-code">404</view>
      <view class="error-message">很抱歉，您访问的页面不存在</view>
      <u-button class="home-button" type="primary" @click="goHome">返回首页</u-button>
    </view>
  </view>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'

const goHome = () => {
  uni.switchTab({
    url: '/pages/index/index'
  })
}
</script>

<style scoped>
.error-page {
  padding: 20rpx;
}

.content {
  margin-top: 100rpx;
  text-align: center;
}

.error-code {
  font-size: 80rpx;
  font-weight: bold;
  color: #e54d42;
  margin-bottom: 20rpx;
}

.error-message {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 40rpx;
}

.home-button {
  width: 60%;
  margin: 0 auto;
}
</style>