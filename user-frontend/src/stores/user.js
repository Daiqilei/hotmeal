/**
 * @file         src/stores/user.js
 * @author       taichilei
 * @date         2025-04-29
 * @description  This file defines the user store.
 */

import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import {getProfile} from '@/api/user'

export const useUserStore = defineStore('user', () => {
    // 用户 token
    const token = ref('')
    // 用户信息
    const userInfo = ref({
        userId: '',
        account: '',
        nickname: '游客',
        avatar: '/static/logo.png',
        email: '',
        phoneNumber: '',
        favoriteCuisine: '',
        role: '',
        status: '',
    })

    // 是否已登录
    const isLogin = computed(() => !!token.value)

    function setToken(newToken) {
        token.value = newToken
    }

    function setUserInfo(newUserInfo) {
        userInfo.value = {...userInfo.value, ...newUserInfo}
    }

    // 登录（设置 token、用户信息）
    function login(payload) {
        token.value = payload.token
        userInfo.value = {...userInfo.value, ...payload.userInfo}
    }

    // 通用重置方法
    function resetUserInfo() {
        userInfo.value = {
            userId: '',
            account: '',
            nickname: '游客',
            avatar: '/static/logo.png',
            email: '',
            phoneNumber: '',
            favoriteCuisine: '',
            role: '',
            status: '',
        }
    }

    // 登出（清空所有信息）
    function logout() {
        //TODO: 临时处理，后续需优化
        console.log('logout called')
        token.value = ''
        resetUserInfo()
    }

    // 更新资料（只更新部分字段）
    function updateProfile(newProfile) {
        userInfo.value = {...userInfo.value, ...newProfile}
    }

    // 获取用户信息（从后端）
    async function fetchUserInfo() {
        try {
            const res = await getProfile()
            if (res?.data) {
                userInfo.value = {...userInfo.value, ...res.data}
                return res.data
            }
        } catch (err) {
            //TODO: 处理错误
            console.error('[userStore] 获取用户信息失败', err)
            uni.showToast({title: '获取用户信息失败', icon: 'none'})
            return null
        }
    }

    return {
        token,
        userInfo,
        isLogin,
        setToken,
        setUserInfo,
        login,
        logout,
        updateProfile,
        resetUserInfo,
        fetchUserInfo
    }
}, {
    persist: true
})