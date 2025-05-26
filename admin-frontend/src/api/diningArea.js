/**
 * @file            /src/api/diningArea.js
 * @description
 * @author          taichilei
 * @date            2025-04-18
 * @version         1.0.0
 */

import request from '@/utils/request'

// 添加餐区
export const addDiningArea = (data) => {
  console.log('addDiningArea Called')
  console.log('data:', JSON.stringify(data)) // 打印 json 字符串
  return request.post('/dining-areas/', data)
}

// 获取餐区详情
export const getDiningAreaDetail = (id) => {
  return request.get(`/dining-areas/${id}`)
}

// 获取餐区列表
export const getDiningAreaList = (params = {}) => {
  return request.get('/dining-areas', { params })
}

// 修改餐区
export const updateDiningArea = (id, max) => {
  return request.put(`/dining-areas/${id}`, { max })
}

// 使用餐区
export const useDiningArea = (id) => {
  return request.put(`/dining-areas/${id}/use`)
}

// 删除餐区
export const deleteDiningArea = (id) => {
  return request.delete(`/dining-areas/${id}`)
}
