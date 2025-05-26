/**
 * @file            dish.js
 * @description
 * @author          taichilei
 * @date            2025-04-18
 * @version         1.0.0
 */

import request from '@/utils/request'

// 菜品相关接口

// 新增菜品
export const createDish = (dish) => request.post('/dishes/', dish)

// 获取菜品详情
export const getDishDetail = (dishId) => request.get(`/dishes/${dishId}`)

// 获取菜品列表
export const getDishList = () => request.get('/dishes/')

// 修改菜品
export const updateDish = (dishId, dish) => request.put(`/dishes/${dishId}`, dish)

// 删除菜品
export const deleteDish = (dishId) => request.delete(`/dishes/${dishId}`)

// 获取某用户的菜品列表（门店专属）
export const getStoreDishes = (params) => request.post('/dishes/store/list', params)

// 以下方法不再使用，已由 RESTful 路由替代
// export const removeDish = (dish) => request.post('/dishes/remove', dish)
// export const searchDish = (params) => request.post('/dishes/info', params)


// 标签相关接口
export const getAllTags = () => request.get('/tags/')
export const createTag = (name) => request.post('/tags/', { name })
export const deleteTag = (tagId) => request.delete(`/tags/${tagId}`)
