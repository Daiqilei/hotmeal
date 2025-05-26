/**
 * @file            src/stores/userStore.js
 * @description     user Pinia store
 * @author          taichilei
 * @date            2025-04-24
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useUserStore = defineStore(
  'user',
  () => {
    const userId = ref('')
    // 当前登录用户的唯一标识符，由后端生成，前端只读
    const account = ref('')
    const username = ref('游客')
    const avatar = ref('')
    const phoneNumber = ref('')
    const email = ref('')
    const role = ref('USER')
    const status = ref('ACTIVE')
    const favoriteCuisine = ref('')
    const isLoggedIn = ref(false)
    const token = ref('')

    // 优先展示 username，其次 account，最后 fallback 为 "游客"
    const displayName = computed(() => username.value || account.value || '游客')

    const welcomeMessage = computed(() => (isLoggedIn.value ? `欢迎，${username.value}` : '请登录'))

    function login(name, tkn) {
      username.value = name
      token.value = tkn
      isLoggedIn.value = true
    }

    /**
     * 执行完整的登出流程，推荐在用户点击“退出登录”时调用。
     * - 调用 reset() 清空所有用户状态字段
     * - 清除 localStorage 中的 'user_info'（配合 pinia-plugin-persist）
     * - 可扩展添加如服务端注销 token 等操作
     */
    function logout() {
      reset()
      localStorage.removeItem('user_info') // 清除持久化缓存
    }

    /**
     * 重置用户状态，仅清空本地 Pinia 中的用户相关字段。
     * 不触发任何登出流程或跳转，用于切换账号、刷新会话、初始化状态等场景。
     * 注意：不会清除 localStorage 中的持久化数据（由 logout 控制）。
     */
    function reset() {
      userId.value = ''
      account.value = ''
      username.value = '游客'
      avatar.value = ''
      phoneNumber.value = ''
      email.value = ''
      role.value = 'USER'
      status.value = 'ACTIVE'
      favoriteCuisine.value = ''
      isLoggedIn.value = false
      token.value = ''
      // do not reset persist!
    }

    return {
      userId,
      account,
      username,
      avatar,
      phoneNumber,
      email,
      role,
      status,
      favoriteCuisine,
      isLoggedIn,
      token,
      welcomeMessage,
      displayName,
      login,
      logout,
      reset,
    }
  },
  {
    persist: true,
  },
)
