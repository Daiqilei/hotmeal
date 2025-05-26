<!--
 * @file         src/pages/profile/index.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  （这里补充页面/组件简要描述）
-->

<!-- src/pages/profile -->

<template>
  <view class="profile-page">
    <Navbar title="我的"/>
    <view style="height: 64px;"/>
    <view class="user-info">
      <image :src="userStore.userInfo.avatar || '/static/logo.png'" class="avatar" mode="aspectFill"/>
      <view class="user-name">{{ userStore.token ? userStore.userInfo.account : 'tourist account' }}</view>
      <u-button
          v-if="!userStore.token"
          class="login-button"
          size="mini"
          type="primary"
          @click="goLogin"
      >
        登录账号
      </u-button>
    </view>
    <view class="settings-list">
      <u-cell isLink title="编辑资料" @click="goEditProfile"/>
      <u-cell isLink title="账号设置" @click="goSetting"/>
      <u-cell isLink title="我的订单" @click="goOrderList"/>
    </view>
  </view>
</template>

<script setup>
import {useUserStore} from '@/stores/user'
import {onShow} from '@dcloudio/uni-app'
import Navbar from '@/components/Navbar.vue'
// 无需引入 login 相关接口

const userStore = useUserStore()

onShow(() => {
  // 同步 userStore.userInfo
  userStore.userInfo = {...userStore.userInfo}
  
})

const goLogin = () => {
  uni.navigateTo({
    url: '/pages/auth/login'
  })
}

const goEditProfile = () => {
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}

const goSetting = () => {
  uni.navigateTo({
    url: '/pages/profile/setting'
  })
}

const goOrderList = () => {
  // 临时跳转测试，不联调接口
  uni.navigateTo({
    url: '/pages/order/list'
  })
}
</script>

<style scoped>
.profile-page {
  padding: 20rpx;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40rpx 0;
}

.avatar {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20rpx;
}

.user-name {
  font-size: 32rpx;
  font-weight: bold;
}

.settings-list {
  margin-top: 30rpx;
}

.login-button {
  margin-top: 20rpx;
}
</style>