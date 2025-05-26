/**
 * @file            /src/api/chart.js
 * @description
 * @author          taichilei
 * @date            2025-04-23
 * @version         1.0.0
 */

import request from '@/utils/request'

export function getMonthlyRevenue() {
  return request.post('/buy/admin/revenue')
}

export function getCategoryVolume() {
  return request.post('/buy/cate/volume')
}

export function getCategoryCount() {
  return request.post('/buy/cate/count')
}
