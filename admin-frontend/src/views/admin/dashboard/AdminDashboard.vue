<template>
  <el-container class="dashboard-container">
    <el-container>
      <el-header class="header">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item v-for="bc in breadcrumbs" :key="bc">
            {{ bc }}
          </el-breadcrumb-item>
        </el-breadcrumb>
        <div class="header-actions">
          <el-input class="search-input" placeholder="Search..." prefix-icon="Search" />
          <el-badge :value="5" class="notification">
            <el-icon>
              <Bell />
            </el-icon>
          </el-badge>
          <el-avatar size="small" src="@/assets/avatar.jpg" />
        </div>
      </el-header>
      <el-main class="main-content">
        <el-row :gutter="20" class="stats-row">
          <el-col v-for="card in statsCards" :key="card.title" :span="6">
            <el-card class="stat-card">
              <div class="card-content">
                <div class="card-title">{{ card.title }}</div>
                <div class="card-value">{{ card.value }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" class="dashboard-charts">
          <el-col :span="14">
            <el-card>
              <template #header>📈 收入趋势（近7天）</template>
              <RevenueTrend />
            </el-card>
          </el-col>
          <el-col :span="10">
            <el-card>
              <template #header>🍽️ 热销菜品榜</template>
              <TopDishes />
            </el-card>
          </el-col>
        </el-row>
        <div class="content-area">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
  import { Bell } from '@element-plus/icons-vue'
  import { useUserStore } from '@/stores/userStore'
  import { defineAsyncComponent } from 'vue'

  const userStore = useUserStore()
  const breadcrumbs = ['Home', 'Dashboard']
  const statsCards = [
    { title: 'Users', value: 1024 },
    { title: 'Revenue', value: '$50K' },
    { title: 'Orders', value: 230 },
    { title: 'Feedback', value: 85 },
  ]

  const RevenueTrend = defineAsyncComponent(
    () => import('@/views/admin/dashboard/components/RevenueTrend.vue'),
  )
  const TopDishes = defineAsyncComponent(
    () => import('@/views/admin/dashboard/components/TopDishes.vue'),
  )
</script>

<style scoped>
  .dashboard-container {
    height: 100vh;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: #fff;
    border-bottom: 1px solid #ebeef5;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 15px;
  }

  .search-input {
    width: 200px;
  }

  .main-content {
    padding: 20px;
    background-color: #f5f7fa;
  }

  .stats-row {
    margin-bottom: 20px;
  }

  .stat-card {
    text-align: center;
  }

  .card-content .card-title {
    font-size: 14px;
    color: #909399;
  }

  .card-content .card-value {
    font-size: 24px;
    font-weight: bold;
    margin-top: 5px;
  }

  .content-area {
    background: #fff;
    padding: 20px;
    min-height: 400px;
  }

  /* 追加样式 */
  .dashboard-charts {
    margin-bottom: 20px;
  }
</style>
