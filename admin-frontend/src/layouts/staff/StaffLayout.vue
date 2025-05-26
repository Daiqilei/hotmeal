<template>
  <!-- 员工后台整体布局容器 -->
  <div class="staff-layout">
    <Header role="staff" />
    <div class="layout-body">
      <!-- 左侧菜单栏 -->
      <Sidebar :role="'staff'" class="sidebar" :menus="staffMenus" :isCollapse="isCollapse" />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
  // 修正 Sidebar 引入路径，移除无效组件
  import Header from '@/components/common/NavigationBar.vue'
  import Sidebar from '@/components/common/Sidebar.vue'
  import { ref } from 'vue'
  import staffMenus from '@/menus/staff.js'

  const isCollapse = ref(false)
</script>

<style scoped>
  .staff-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .layout-body {
    display: flex;
    flex: 1;
  }

  .main-content {
    flex: 1;
    padding: 24px;
    background-color: #f5f5f5;
  }

  .sidebar {
    width: 200px;
    flex-shrink: 0;
  }

  .content-area {
    display: flex;
    flex-direction: column;
    flex: 1;
  }
</style>
