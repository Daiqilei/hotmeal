<!--
 * @file         src/pages/profile/edit.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  编辑个人资料页面
-->

<template>
  <view class="edit-profile-page">
    <Navbar title="编辑资料"/>
    <view style="height: 64px;"/>
    <view class="form">
      <view class="avatar-section">
        <image :src="avatar" class="avatar" mode="aspectFill" @click="chooseAvatar"/>
        <view class="avatar-tip">点击更换头像</view>
      </view>
      <u-input v-model="nickname" clearable placeholder="请输入昵称"/>
      <u-input v-model="phoneNumber" clearable placeholder="请输入手机号"/>
      <u-input v-model="email" clearable placeholder="请输入邮箱"/>
      <u-button class="save-button" type="primary" @click="saveProfile">保存资料</u-button>
    </view>
  </view>
</template>

<script setup>

import {ref} from 'vue'
import {useUserStore} from '@/stores/user'
import {onShow} from '@dcloudio/uni-app'
import {updateUserProfile} from '@/api/user'
import Navbar from '@/components/Navbar.vue'
import {requireLogin} from '@/utils/auth'


const userStore = useUserStore()

onShow(() => {
  if (!requireLogin()) {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })
    uni.navigateTo({
      url: '/pages/login/index'
    })
  }
})

const nickname = ref(userStore.userInfo.nickname)
const avatar = ref(userStore.userInfo.avatar)
const phoneNumber = ref(userStore.userInfo.phoneNumber)
const email = ref(userStore.userInfo.email)

const chooseAvatar = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      avatar.value = res.tempFilePaths[0]
    }
  })
}

const saveProfile = async () => {
  try {
    //开始调用后端的接口更新用户信息

    await updateUserProfile({
      username: nickname.value,
      phone_number: phoneNumber.value,
      email: email.value,
      // 可选字段如 favorite_cuisine 此处暂不处理
    })

    //更新本地缓存的用户信息
    await userStore.updateProfile({
      nickname: nickname.value,
      avatar: avatar.value,
      phoneNumber: phoneNumber.value,
      email: email.value
    })
    uni.showToast({
      title: '保存成功',
      icon: 'success'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 800)
  } catch (error) {
    console.error('[edit.vue] 保存资料失败', error)
    uni.showToast({
      title: '保存失败',
      icon: 'none'
    })
  }
}
</script>

<style scoped>
.edit-profile-page {
  padding: 20rpx;
}

.form {
  margin-top: 40rpx;
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40rpx;
}

.avatar {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-tip {
  font-size: 24rpx;
  color: #888;
  margin-top: 10rpx;
}

.save-button {
  margin-top: 40rpx;
}
</style>