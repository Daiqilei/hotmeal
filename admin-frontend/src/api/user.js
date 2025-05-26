/****
 * @file            user.js
 * @description     用户相关 API 接口封装
 * @author          taichilei
 * @date            2025-04-18
 * @version         1.0.0
 */

import request from '@/utils/request'

//ADD USER
export const addUser = (user) => {
  return request.post('/users', user)
}

// LOGIN
export const login = (credentials) => {
  return request.post('/auth/token', credentials)
}

// 获取用户列表（支持分页、模糊搜索）
export const getUserList = (query = {}) => {
  return request.get('/admin/users', { params: query })
}

//用户本人查看自己的信息
export const getUserInfo = () => {
  return request.get('/users/me')
}

// 获取用户信息
export const searchUserByAccount = (account) => {
  return request.post('/users/me', { account })
}

// 更新用户信息（管理员）
export const updateUser = (user_id, updateData) => {
  if (!user_id) {
    console.error('user_id is missing in updateUser request')
    throw new Error('Missing user_id in updateUser request')
  }
  return request.put(`/admin/users/${user_id}`, updateData)
}

// 更新当前登录用户信息
export const updateUserInfo = (userInfo) => {
  return request.put('/users/me', userInfo)
}

// 删除用户
export const deleteUser = (id) => {
  return request.post('/users/remove', { id })
}
