/**
 * @file            /src/router/admin.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default [
  {
    path: '/admin',
    component: () => import('@/layouts/admin/AdminLayout.vue'),
    redirect: '/admin/dashboard',
    meta: { role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/dashboard/AdminDashboard.vue'),
      },
      {
        path: 'charts',
        name: 'AdminCharts',
        component: () => import('@/views/admin/chart/ChartPanel.vue'),
      },
      {
        path: 'orders',
        name: 'AdminOrder',
        component: () => import('@/views/admin/order/OrderPanel.vue'),
      },
      {
        path: 'user',
        name: 'AdminUser',
        component: () => import('@/views/admin/user/UserPanel.vue'),
      },
      {
        path: 'staff',
        name: 'AdminStaff',
        component: () => import('@/views/admin/staff/StaffPanel.vue'),
      },
      {
        path: 'dish',
        name: 'AdminDish',
        component: () => import('@/views/admin/dish/DishPanel.vue'),
      },
      {
        path: 'category',
        name: 'AdminCategory',
        component: () => import('@/views/admin/category/CategoryPanel.vue'),
      },
      {
        path: 'tag',
        name: 'AdminTag',
        component: () => import('@/views/admin/tag/TagPanel.vue'),
      },
      {
        path: 'dining-area',
        name: 'AdminDiningArea',
        component: () => import('@/views/admin/dining-area/DiningAreaPanel.vue'),
      },
      {
        path: 'recommend',
        name: 'AdminRecommend',
        component: () => import('@/views/admin/recommend/RecommendPanel.vue'),
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/settings/Settings.vue'),
      },
    ],
  },
]
