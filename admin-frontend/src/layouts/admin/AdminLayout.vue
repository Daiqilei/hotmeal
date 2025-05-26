<template>
  <!-- 管理员后台整体布局容器 -->
  <div class="admin-layout">
    <!-- 顶部导航栏组件 -->
    <Header role="admin" />
    <!-- 页面主体区域 -->
    <div class="layout-body">
      <Sidebar class="sidebar-container" :menus="adminMenus" :isCollapse="isCollapse" />
      <!-- 页面主内容区域：支持插槽与嵌套路由 -->
      <main class="main-content">
        <slot />
        <router-view />
      </main>
    </div>
    <!-- 页面底部组件 -->
    <Footer />
  </div>
</template>

<script setup>
  import Header from '@/components/common/NavigationBar.vue'
  import Footer from '@/components/common/Footer.vue'
  import Sidebar from '@/components/common/Sidebar.vue'
  import { ref } from 'vue'
  import adminMenus from '@/menus/admin.js'

  const isCollapse = ref(false)
</script>

<style>
  .admin-layout {
    display: flex;
    flex-direction: column;
    background-color: #ffffff; /* 白色背景 */
    color: #333;
    overflow: hidden;
  }

  .layout-body {
    display: flex;
    flex: 1;
    min-height: 0;

    overflow: hidden;
  }

  /* 顶部导航栏链接样式 */
  .footer-center a,
  .footer-right a {
    margin: 0 8px;
    color: #666;
    text-decoration: none;
    font-size: 13px;
  }

  /* 底部图标样式 */
  .footer-right i {
    font-size: 16px;
  }
  /* 主内容区域样式 */
  .main-content {
    flex: 1;
    padding: 20px;
    background-color: #f5f5f5;
    overflow-y: auto;
  }

  .sidebar-container {
    width: 200px;
    min-width: 200px;
    background-color: #2d3a4b;
    color: #fff;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
</style>
