<!--
 * @file         src/pages/profile/setting.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  setting page
-->

<!-- src/pages/profile -->

<template>
  <view class="setting-page">
    <Navbar title="设置"/>
    <view style="height: 64px;"/>
    <view class="settings-list">
      <u-cell isLink title="隐私政策"/>
      <u-cell isLink title="用户协议"/>
      <u-cell isLink title="关于我们" to="/pages/about/index"/>
    </view>
    <view class="logout-button-wrapper">
      <u-button type="error" @click="handleLogout">退出登录</u-button>
    </view>
  </view>
</template>

<script setup>

import Navbar from '@/components/Navbar.vue'
import {useUserStore} from '@/stores/user'

console.log('userStore', useUserStore)

const userStore = useUserStore()

const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确认退出登录？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.showToast({title: '已退出', icon: 'none'})
        setTimeout(() => {
          uni.reLaunch({url: '/pages/profile/index'})
        }, 500)
      }
    }
  })
}
</script>

<style scoped>
.setting-page {
  padding: 20rpx;
}

.settings-list {
  margin-top: 40rpx;
}

.logout-button-wrapper {
  margin-top: 80rpx;
}
</style>