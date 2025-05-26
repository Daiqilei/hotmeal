/**
 * @file            staff.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default [
  {
    path: '/staff',
    component: () => import('@/layouts/staff/StaffLayout.vue'),
    redirect: '/staff/dashboard',
    meta: { role: 'staff' },
    children: [
      {
        path: 'dashboard',
        name: 'StaffDashboard',
        component: () => import('@/views/staff/dashboard/index.vue'),
      },
      {
        path: 'dish',
        name: 'StaffDish',
        component: () => import('@/views/staff/dish/index.vue'),
      },
      {
        path: 'profile',
        name: 'StaffProfile',
        component: () => import('@/views/staff/profile/MyInfo.vue'),
      },
    ],
  },
]
