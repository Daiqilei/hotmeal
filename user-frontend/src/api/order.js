/**
 * @file         src/api/order.js
 * @author       taichilei
 * @date         2025-04-29
 * @description  订单相关接口
 */

import {request} from '@/utils/request'

// 创建订单
export function createOrder(data) {
    return request({
        url: '/orders/',
        method: 'POST',
        data
    })
}

// 获取当前用户订单列表
export function getMyOrders(params = {}) {
    return request({
        url: '/orders/me',
        method: 'GET',
        params
    })
}

// 获取订单详情
export function getOrderDetail(orderId, params = {}) {
    return request({
        url: `/orders/${orderId}`,
        method: 'GET',
        params
    })
}

// 更新订单（支付方式、支付状态）
export function updateOrder(orderId, data) {
    return request({
        url: `/orders/${orderId}`,
        method: 'PUT',
        data
    })
}

// 取消订单
export function cancelOrder(orderId) {
    return request({
        url: `/orders/${orderId}/cancel`,
        method: 'PUT'
    })
}

// 删除订单（软删除）
export function deleteOrder(orderId) {
    return request({
        url: `/orders/${orderId}/delete`,
        method: 'DELETE'
    })
}
