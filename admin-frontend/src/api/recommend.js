/**
 * @file            /src/api/recommend.js
 * @description     推荐模块相关接口定义（首页推荐、个性推荐等）
 * @author          taichilei
 * @date            2025-04-23
 * @version         1.0.0
 */

import request from '@/utils/request'

// 获取通用推荐（首页、菜单页推荐分类）
export function getRecommendList() {
  return request({
    url: '/api/recommend',
    method: 'get',
  })
}

// 获取个性化推荐（需要 userId）
export function getPersonalRecommend(userId) {
  return request({
    url: `/api/recommend/personal`,
    method: 'get',
    params: { userId },
  })
}

// 获取某分类下热门推荐菜品（用于分类页冷启动）
export function getCategoryRecommend(categoryId) {
  return request({
    url: `/api/recommend/category/${categoryId}`,
    method: 'get',
  })
}

// 获取推荐理由说明（可选，用于解释“为什么推荐此菜品”）
export function getRecommendReason(userId, dishId) {
  return request({
    url: '/api/recommend/reason',
    method: 'get',
    params: { userId, dishId },
  })
}
