/**
 * @file         src/utils/auth.js
 * @author       taichilei
 * @date         2025-04-29
 * @description
 */

import {useUserStore} from '@/stores/user'

/**
 * 判断用户是否登录，未登录则跳转登录页
 * @param {boolean} redirect - 是否自动跳转登录页（默认true）
 * @returns {boolean} 是否已登录
 */
export function requireLogin(redirect = true) {
    const userStore = useUserStore()
    if (!userStore.token) {
        if (redirect) {
            uni.showToast({title: '请先登录', icon: 'none'})
            setTimeout(() => {
                uni.navigateTo({url: '/pages/auth/login'})
            }, 500)
        }
        return false
    }
    return true
}
