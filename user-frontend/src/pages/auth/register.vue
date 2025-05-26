<!--
 * @file         src/pages/auth/register.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  （这里补充页面/组件简要描述）
-->

<!-- src/pages/auth -->

<template>
  <view class="register-page">
    <Navbar title="注册"/>
    <view style="height: 64px;"/>
    <view class="form">
      <u-input v-model="account" clearable placeholder="请输入账号"/>
      <u-input v-model="password" clearable placeholder="请输入密码" type="password"/>
      <u-input v-model="confirmPassword" clearable placeholder="请确认密码" type="password"/>
      <u-button class="register-button" type="primary" @click="handleRegister">注册</u-button>
    </view>
  </view>
</template>

<script setup>
import {ref} from 'vue'
import {useUserStore} from '@/stores/user'
import Navbar from '@/components/Navbar.vue'
import {registerUser} from '@/api/user'

const account = ref('')
const password = ref('')
const confirmPassword = ref('')

const userStore = useUserStore()

const handleRegister = async () => {
  // 校验信息
  if (!account.value || !password.value || !confirmPassword.value) {
    uni.showToast({
      title: '请填写完整信息',
      icon: 'none'
    })
    return
  }
  // 校验密码
  if (password.value !== confirmPassword.value) {
    uni.showToast({
      title: '两次密码不一致',
      icon: 'none'
    })
    return
  }
  try {
    const apiRes = await registerUser({
          account: account.value,
          password: password.value
        }
    )
    if (apiRes.code === 200) {

      // 如果成功，store中保存用户信息
      const storeRes = await userStore.register({account: account.value, password: password.value})
      uni.showToast({title: '注册成功', icon: 'success'})
      uni.switchTab({url: 'pages/user/index'})

      if (storeRes?.error_code === 0) {
        userStore.setUserInfo(
            {
              account: account.value,
              token: apiRes.data.token,
            }
        )
        
      }

    } else {
      uni.showToast({title: apiRes.message || '注册失败', icon: 'none'})
    }
  } catch (err) {
    uni.showToast({title: '注册失败', icon: 'none'})
  }

}
</script>

<style scoped>
.register-page {
  padding: 20rpx;
}

.form {
  margin-top: 60rpx;
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.register-button {
  margin-top: 40rpx;
}
</style>