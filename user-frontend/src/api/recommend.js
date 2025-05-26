/**
 * @file         src/api/recommend.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {request} from '@/utils/request'

// 获取推荐菜品列表
export function getRecommendations(limit = 10) {
    return request({
        url: '/recommendations/',
        method: 'GET',
        params: {
            limit
        }
    })
}