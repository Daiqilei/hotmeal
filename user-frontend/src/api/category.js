/**
 * @file         src/api/category.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {request} from '@/utils/request'

const BASE_URL = '/categories'

// 获取分类列表（可选包含已删除）
export const getCategoryList = (params = {}) => {
    return request({
        url: BASE_URL,
        method: 'GET',
        params
    })
}

// 创建新分类
export const createCategory = (data) => {
    return request({
        url: BASE_URL,
        method: 'POST',
        data
    })
}

// 获取分类详情
export const getCategoryDetail = (categoryId, params = {}) => {
    return request({
        url: `${BASE_URL}/${categoryId}`,
        method: 'GET',
        params
    })
}

// 更新分类
export const updateCategory = (categoryId, data) => {
    return request({
        url: `${BASE_URL}/${categoryId}`,
        method: 'PUT',
        data
    })
}

// 删除分类（支持软删除/永久删除）
export const deleteCategory = (categoryId, permanent = false) => {
    return request({
        url: `${BASE_URL}/${categoryId}`,
        method: 'DELETE',
        params: {permanent}
    })
}

// 恢复分类
export const restoreCategory = (categoryId) => {
    return request({
        url: `${BASE_URL}/${categoryId}/restore`,
        method: 'POST'
    })
}