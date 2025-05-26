<!--
 * @file         src/pages/auth/login.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  登录页面
-->

<template>
  <view class="login-page">
    <Navbar title="登录"/>
    <view style="height: 64px;"/>
    <view class="form">
      <u-input v-model="account" clearable placeholder="请输入账号"/>
      <u-input v-model="password" clearable placeholder="请输入密码" type="password"/>
      <u-button class="login-button" type="primary" @click="handleLogin">登录</u-button>
    </view>
    <view class="register-link">
      <text>还没有账号？</text>
      <text class="link" @click="goToRegister">立即注册</text>
    </view>
  </view>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import {ref} from 'vue'
import {useUserStore} from '@/stores/user'
import {loginUser} from '@/api/user'

const userStore = useUserStore()
const account = ref('')
const password = ref('')

const handleLogin = async () => {
  if (!account.value || !password.value) {
    uni.showToast({
      title: '账号或密码不能为空',
      icon: 'none'
    })
    return
  }

  try {
    const res = await loginUser({
      account: account.value,
      password: password.value
    })

    //const token = res?.token
    const token = res?.data?.token
    if (!token) throw new Error('无效的响应')

    // 设置 token
    userStore.setToken(token)

    const userInfoRes = await userStore.fetchUserInfo()
    if (!userInfoRes) throw new Error('获取用户信息失败')

    uni.showToast({
      title: '登录成功',
      icon: 'success'
    })

    setTimeout(() => {
      uni.switchTab({
        url: '/pages/profile/index'
      })
    }, 500)
  } catch (err) {
    uni.showToast({
      title: err.message || '登录失败',
      icon: 'none'
    })
  }
}

const goToRegister = () => {
  uni.navigateTo({
    url: '/pages/auth/register'
  })
}
</script>

<style scoped>
.login-page {
  padding: 20rpx;
}

.form {
  margin-top: 60rpx;
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.login-button {
  margin-top: 40rpx;
}

.register-link {
  display: flex;
  justify-content: center;
  margin-top: 20rpx;
  font-size: 26rpx;
  color: #666;
}

.register-link .link {
  color: #2979ff;
  margin-left: 10rpx;
  text-decoration: underline;
}
</style>