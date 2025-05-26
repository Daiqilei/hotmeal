<!--
@File        : .vue
@Author      : ChiLei Tai
@Date        : 2025-04-01
@Description : Ordering System
-->
<template>
  <h2>修改个人信息</h2>
  <el-form-item class="upusna" label="新用户名称" prop="username">
    <el-input
      v-model="loginForm.username"
      placeholder="请输入名称"
      style="height: 40px; width: 300px"
      clearable
    ></el-input>
  </el-form-item>
  <el-form-item class="upuspa" label="新用户密码" prop="password">
    <el-input
      v-model="loginForm.password"
      placeholder="请输入密码"
      style="height: 40px; width: 300px"
      clearable
    ></el-input>
  </el-form-item>
  <el-button class="upmyinfo-button" type="primary" @click="update">修改</el-button>
</template>
<script setup>
  import { reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import { updateUserInfo } from '@/api/user'

  const router = useRouter()

  const loginForm = reactive({
    username: sessionStorage.getItem('username'),
    password: sessionStorage.getItem('password'),
  })

  function update() {
    updateUserInfo({
      username: loginForm.username,
      password: loginForm.password,
      id: sessionStorage.getItem('userid'),
    }).then((res) => {
      if (res.data.code === 200) {
        ElMessage.success('修改成功')
        router.push('/user/user')
      } else {
        ElMessage.error('修改失败')
      }
    })
  }
</script>
<style>
  .upusna {
    position: absolute;
    left: 10%;
    top: 120%;
    font-size: 25px;
  }
  .upuspa {
    position: absolute;
    left: 10%;
    top: 200%;
    font-size: 25px;
  }
  .upmyinfo-button {
    position: absolute;
    left: 130%;
    top: 320%;
  }
</style>
