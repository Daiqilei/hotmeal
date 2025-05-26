<!--
 * @file         src/pages/about/index.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  关于页面，展示项目信息和开发者信息
-->

<template>
  <view class="about-page">
    <Navbar title="关于我们"/>
    <view style="height: 64px;"/>
    <view class="content">
      <view class="title">点餐小程序</view>
      <view class="subtitle">版本：1.0.0</view>
      <view class="description">
        本项目为计算机专业毕业设计作品，基于 Vue3 + UniApp 开发，旨在提供简洁、易用的点餐体验。
      </view>
      <view class="author">作者：Tai ChiLei</view>
    </view>
  </view>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.about-page {
  padding: 20rpx;
}

.content {
  margin-top: 80rpx;
  text-align: center;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #888;
  margin-bottom: 40rpx;
}

.description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 60rpx;
  padding: 0 40rpx;
}

.author {
  font-size: 26rpx;
  color: #333;
}
</style>