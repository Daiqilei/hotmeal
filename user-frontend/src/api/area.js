/**
 * @file         src/api/area.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {request} from '@/utils/request'

// 获取餐区列表
export function getDiningAreaList(params = {}) {
    return request({
        url: '/dining-areas/',
        method: 'GET',
        params
    })
}

// 创建餐区（管理员权限）
export function createDiningArea(data) {
    return request({
        url: '/dining-areas/',
        method: 'POST',
        data
    })
}

// 获取餐区详情
export function getDiningAreaDetail(areaId) {
    return request({
        url: `/dining-areas/${areaId}`,
        method: 'GET'
    })
}

// 更新餐区信息（管理员权限）
export function updateDiningArea(areaId, data) {
    return request({
        url: `/dining-areas/${areaId}`,
        method: 'PUT',
        data
    })
}

// 删除餐区（管理员权限）
export function deleteDiningArea(areaId) {
    return request({
        url: `/dining-areas/${areaId}`,
        method: 'DELETE'
    })
}

// 分配餐区给指定用户（管理员/员工权限）
export function assignDiningArea(areaId, data) {
    return request({
        url: `/dining-areas/${areaId}/assign`,
        method: 'POST',
        data
    })
}

// 释放餐区（管理员/员工权限）
export function releaseDiningArea(areaId) {
    return request({
        url: `/dining-areas/${areaId}/release`,
        method: 'POST'
    })
}