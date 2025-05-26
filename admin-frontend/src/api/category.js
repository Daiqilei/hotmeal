/**
 * @file            category.js
 * @description
 * @author          taichilei
 * @date            2025-04-20
 * @version         1.0.0
 */

import request from '@/utils/request'

// 获取分类列表
export function getCategoryList() {
  return request({
    url: '/categories/',
    method: 'get',
  })
}

// 创建分类
export function createCategory(data) {
  return request({
    url: '/categories/',
    method: 'post',
    data,
  })
}

// 更新分类
export function updateCategory(id, data) {
  return request({
    url: `/categories/${id}`,
    method: 'put',
    data,
  })
}

// 删除分类
export function deleteCategoryById(id) {
  return request({
    url: `/categories/${id}`,
    method: 'delete',
  })
}
