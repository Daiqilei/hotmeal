<template>
  <div class="view-container">
    <NavigationBar role="user" />
    <div class="login-container">
      <div class="login-form">
        <el-avatar :src="logoUrl" shape="circle" size="large" style="margin-bottom: 20px" />

        <h1>{{ t('auth.login.welcome') }}</h1>

        <el-form label-position="top" @submit.prevent="handleLogin">
          <el-form-item>
            <el-input
              v-model="account"
              :placeholder="t('auth.login.account')"
              prefix-icon="el-icon-user"
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="password"
              :placeholder="t('auth.login.password')"
              prefix-icon="el-icon-lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <div class="button-group">
              <el-button class="login-btn" type="primary" @click="handleLogin">
                <span class="icon"><i class="el-icon-check" /></span>
                <span class="text">{{ t('auth.login.loginButton') }}</span>
              </el-button>

              <el-button class="register-btn" type="info" @click="goToRegister">
                <span class="icon"><i class="el-icon-edit" /></span>
                <span class="text">{{ t('auth.register.title') }}</span>
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import { ElMessage } from 'element-plus'
  import logo from '@/assets/logo.png'
  import { login } from '@/api/user'
  import { useUserStore } from '@/stores/userStore'

  import NavigationBar from '@/components/common/NavigationBar.vue'
  import Footer from '@/components/common/Footer.vue'

  const { t } = useI18n()
  const router = useRouter()
  const userStore = useUserStore()

  const account = ref('')
  const password = ref('')
  const logoUrl = logo + ''

  async function handleLogin() {
    // 表单验证
    if (!account.value || !password.value) {
      ElMessage.warning(t('auth.emptyFields'))
      return
    }
    // 登录请求
    try {
      const res = await login({
        account: account.value,
        password: password.value,
      })
      //console.log('Login response:', res)
      const data = res.data?.data
      const token = data?.token
      const user = data?.user

      if (token && user) {
        localStorage.setItem('token', token)
        ElMessage(t('auth.login.success'))

        userStore.login(user.username, token)
        //console.log('[Login] Stored token:', token)
        //console.log('[Login] Stored username:', user.username)

        const role = user.role?.toLowerCase()
        if (role === 'admin') {
          await router.push('/admin')
        } else if (role === 'staff') {
          await router.push('/staff')
        } else {
          await router.push('/user') // 默认跳转到用户页面
        }
      } else {
        ElMessage.error(t('auth.login.failed'))
      }
    } catch (err) {
      ElMessage.error(t('auth.login.error'))
    }
  }

  function goToRegister() {
    router.push('/register')
  }
</script>

<style scoped>
  /* ===============================
1. 登录页面 - 外层容器样式
=============================== */
  .login-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ===============================
2. 登录页面 - 表单区域样式
=============================== */
  .login-form {
    background-color: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    width: 400px;
    text-align: center;
  }

  /* ===============================
3. 登录页面 - 标题样式
=============================== */
  h1 {
    margin-bottom: 30px;
    color: #333;
  }

  /* ===============================
4. 登录页面 - 按钮组样式
=============================== */
  .button-group {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    margin-top: 12px;
  }

  .button-group .el-button i {
    font-size: 18px;
    width: 1.2em;
    text-align: center;
    display: inline-block;
    vertical-align: middle;
  }

  .button-group .icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: auto;
  }

  .button-group .text {
    display: inline-block;
    text-align: center;
    width: 100%;
  }

  /* ===============================
5. 登录页面 - 按钮文字样式
=============================== */
  .login-btn,
  .register-btn {
    font-size: 16px;
    text-align: center;
  }
</style>
