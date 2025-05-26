<template>
  <nav>
    <!-- 可插入自定义 logo 区域 -->
    <slot name="logo">
      <div class="logo">
        <img alt="Logo" src="@/assets/icon.png" />
        <span class="logo-text">{{ t('navigator.title') }}</span>
      </div>
    </slot>

    <!-- 根据 role 显示不同菜单项 -->
    <ul>
      <li>
        <router-link to="/">{{ t('navigator.home') }}</router-link>
      </li>
      <li v-if="role === 'admin'">
        <router-link to="/admin/stats">{{ t('navigator.dashboard') }}</router-link>
      </li>
      <li v-if="role === 'staff'">
        <router-link to="/staff/orders">{{ t('navigator.orders') }}</router-link>
      </li>
      <li v-if="role === 'user'">
        <router-link to="/menu">{{ t('navigator.menu') }}</router-link>
      </li>
      <li>
        <router-link to="/about">{{ t('navigator.about') }}</router-link>
      </li>
      <li>
        <router-link to="/contact">{{ t('navigator.contact') }}</router-link>
      </li>
    </ul>

    <!-- 用户头像菜单 -->
    <div class="user-menu">
      <el-dropdown trigger="click">
        <span class="user-info">
          <el-avatar :size="30" :src="userAvatar" />
          <span class="username">{{ userName }}</span>
          <el-icon><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="router.push('/profile')">
              {{ t('navigator.profile') }}
            </el-dropdown-item>

            <el-dropdown-item divided @click="handleLogout"
              >{{ t('navigator.logout') }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- 插槽可自定义右侧附加按钮，例如主题或语言 -->
    <slot name="tools" />
  </nav>
</template>

<script setup>
  import { computed } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRouter } from 'vue-router'
  import { ElAvatar, ElDropdown, ElDropdownItem, ElDropdownMenu, ElIcon } from 'element-plus'
  import { ArrowDown } from '@element-plus/icons-vue'
  import { useUserStore } from '@/stores/userStore' // 根据你的实际路径调整

  const props = defineProps({
    role: { type: String, required: true },
  })

  const { t } = useI18n()
  const store = useUserStore()
  const router = useRouter()
  const userName = computed(() => store.username || store.account || '访客')
  const userAvatar = computed(() => store.avatar || '')

  const handleLogout = () => {
    store.logout()
    localStorage.removeItem('user_info')
    router.push('/login')
  }
</script>

<style scoped>
  nav {
    display: flex;
    align-items: center;
    background-color: #f8f9fa;
    padding: 10px 20px;
  }

  .logo {
    display: flex;
    align-items: center;
    margin-right: 2rem;
  }

  .logo img {
    width: 40px;
    margin-right: 10px;
  }

  .logo-text {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
  }

  ul {
    display: flex;
    flex-grow: 1;
    list-style: none;
    gap: 20px;
    padding: 0;
    margin: 0;
  }

  li a {
    color: #333;
    text-decoration: none;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 6px;
    transition: all 0.3s ease;
  }

  li a:hover {
    background-color: #007bff;
    color: #fff;
  }

  .user-menu {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .username {
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
