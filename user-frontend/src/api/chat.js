/**
 * @file         src/api/chat.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */

import {request} from '@/utils/request'

// 发起新聊天提问
export function createChat(data) {
    return request({
        url: '/chats/',
        method: 'POST',
        data,
    })
}

// 获取聊天记录（分页）
export function getChatHistory(params) {
    return request({
        url: '/chats/',
        method: 'GET',
        params,
    })
}

// 获取聊天详情
export function getChatDetail(chatId) {
    return request({
        url: `/chats/${chatId}`,
        method: 'GET',
    })
}

// AI 直接回复（不保存）
export function directAIChat(data) {
    return request({
        url: '/chats/ai_direct',
        method: 'POST',
        data,
    })
}

// 获取待处理聊天列表（管理员/员工）
export function listPendingChats(params) {
    return request({
        url: '/chats/pending',
        method: 'GET',
        params,
    })
}

// 处理指定聊天记录
export function processChat(chatId) {
    return request({
        url: `/chats/${chatId}/process`,
        method: 'POST',
    })
}