/**
 * @file         src/utils/request.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {useUserStore} from '@/stores/user'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

export function request(options = {}) {
    const userStore = useUserStore()
    const token = userStore.token

    return new Promise((resolve, reject) => {
        // TODO：临时打印请求参数，开发完删除
        console.log('[request.js] 发起请求', {
            url: BASE_URL + options.url,
            method: options.method || 'GET',
            token,
            headers: {
                'Content-Type': 'application/json',
                ...(token ? {Authorization: `Bearer ${token}`} : {}),
                ...options.header,
            },
            data: options.data || {},
        })

        uni.request({
            url: BASE_URL + options.url,
            method: options.method || 'GET',
            data: options.data || {},
            header: {
                'Content-Type': 'application/json',
                ...(token ? {Authorization: `Bearer ${token}`} : {}),
                ...options.header,
            },
            success: (res) => {
                const {statusCode, data} = res
                if (statusCode === 200) {
                    resolve(data)
                } else if (statusCode === 401) {
                    uni.showToast({title: '请先登录', icon: 'none'})
                    uni.navigateTo({url: '/pages/auth/login'})
                    reject(data)
                } else {
                    uni.showToast({title: data.message || '请求失败', icon: 'none'})
                    reject(data)
                }
            },
            fail: (err) => {
                uni.showToast({title: '网络错误', icon: 'none'})
                reject(err)
            }
        })
    })
}
