/**
 * @file            staff.js
 * @description     员工相关 API 接口封装
 * @author          taichilei
 * @date            2025-04-22
 * @version         1.0.0
 */

import request from '@/utils/request'

// 添加员工
export function addStaff(data) {
  return request.post('/staff/users', { ...data, role: 'STAFF' })
}

// 获取员工详情
export function getStaffDetail(user_id) {
  return request.get(`/staff/users/${user_id}`)
}

// 获取员工列表
export function getStaffList(params = {}) {
  return request.get('/staff/users', { params: { ...params, role: 'STAFF' } })
}

// 更新员工信息
export function updateStaff(user_id, updateData) {
  console.log('updateStaff', user_id, updateData)
  console.log('前端调用 updateStaff')
  if (!user_id) {
    console.error('user_id is missing in updateStaff request')
    throw new Error('Missing user_id in updateStaff request')
  }
  return request.put(`/staff/users/${user_id}`, updateData)
}

// 删除员工
export function deleteStaff(user_id) {
  return request.delete(`/staff/users/${user_id}`)
}
