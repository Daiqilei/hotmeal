/****
 * @file            /src/api/order.js
 * @description
 * @author          taichilei
 * @date            2025-04-18
 * @version         1.0.0
 */

import request from '@/utils/request'

// 订单相关API

// 获取订单列表
export function getOrderList(query) {
  return request.get('/orders/', { params: query })
}

// 搜索订单
export const searchOrder = ({ orderId, username }) => request.post('/orders', { orderId, username })

// 更新订单
export const updateOrder = (row) => request.post('/orders/update', row)

// 删除订单
export const deleteOrder = (orderId) => request.post('/orders/remove', { orderId })

// 用户端：添加商品到购物车（用于“推荐”页卡片操作）
export const addToCart = (data) => request.post('/buy/add', data)

// 用户端：获取当前用户订单列表
export const getUserOrders = (params) => request.get('/orders/me', { params })

// 获取未发货订单列表（用户端）
export const getUnsentOrders = (params) => request.get('/orders/unsent', { params })

// 搜索订单详情（更精准，区别于 searchOrder 用于管理端模糊搜索）
export const searchOrderInfo = (params) => request.post('/orders/search', params)

// 发货操作（状态修改）
export const sendOrder = (data) => request.post('/orders/send', data)

// 商家端：获取当前商家的所有订单（按 userId 过滤）
export const getSellerOrders = (params) => request.get('/orders/seller', { params })

// 商家端：根据订单号或用户名模糊搜索订单
export const searchOrderByIdOrName = ({ orderId, username }) =>
  request.post('/orders/search', { orderId, username })
