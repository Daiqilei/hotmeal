/**
 * @file            public.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default [
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/public/profile/Profile.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/public/NotFound.vue'),
  },
  {
    path: '/about',
    name: 'AboutUs',
    component: () => import('@/views/public/AboutUs.vue'),
  },
  {
    path: '/contact',
    name: 'ContactUs',
    component: () => import('@/views/public/ContactUs.vue'),
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/views/public/Menu.vue'),
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: () => import('@/views/public/PrivacyPolicy.vue'),
  },
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404',
  },
]
