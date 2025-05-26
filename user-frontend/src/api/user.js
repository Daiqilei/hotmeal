/**
 * @file         src/api/user.js
 * @author       taichilei
 * @date         2025-04-29
 * @description
 */

import {request} from '@/utils/request'

// 用户注册
export function registerUser(data) {
    return request({
        url: '/users/register',
        method: 'POST',
        data
    })
}

// 用户登录
export function loginUser(data) {
    return request({
        url: '/auth/token',// 这里的url是后端提供的接口
        // url: '/users/login',
        method: 'POST',
        data
    })
}

// 获取个人资料
export function getProfile() {
    return request({
        url: '/users/me',
        method: 'GET'
    })
}

/**
 * 更新当前登录用户的个人资料（需要登录）
 * @param {Object} data - 包含 username、email、phone_number、favorite_cuisine 等字段
 * @returns {Promise} 请求结果
 */
export function updateUserProfile(data) {
    return request({
        url: '/users/me',
        method: 'PUT',
        data
    })
}

// 更新头像
export function updateAvatar(data) {
    return request({
        url: '/users/me/avatar',
        method: 'PUT',
        data
    })
}