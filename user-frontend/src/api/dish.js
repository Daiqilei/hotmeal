/**
 * @file         src/api/dish.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {request} from '@/utils/request'

const BASE_URL = '/dishes'

// 获取菜品列表（可选传入 category_id）
export function getDishList(params = {}) {
    return request({
        url: BASE_URL + '/',
        method: 'GET',
        params
    })
}

// 获取菜品详情
export function getDishDetail(dishId) {
    return request({
        url: `${BASE_URL}/${dishId}`,
        method: 'GET'
    })
}

// 创建新菜品（仅限管理员）
export function createDish(data) {
    return request({
        url: BASE_URL + '/',
        method: 'POST',
        data
    })
}

// 更新菜品（仅限管理员）
export function updateDish(dishId, data) {
    return request({
        url: `${BASE_URL}/${dishId}`,
        method: 'PUT',
        data
    })
}

// 删除菜品（硬删除，仅限管理员）
export function deleteDish(dishId) {
    return request({
        url: `${BASE_URL}/${dishId}`,
        method: 'DELETE'
    })
}

// 设置菜品上下架状态（仅限管理员）
export function setDishAvailability(dishId, isAvailable) {
    return request({
        url: `${BASE_URL}/${dishId}/availability`,
        method: 'PUT',
        data: {is_available: isAvailable}
    })
}