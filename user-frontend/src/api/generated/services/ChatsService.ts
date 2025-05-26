/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AiChatInput } from '../models/AiChatInput';
import type { AiChatOutput } from '../models/AiChatOutput';
import type { ChatAskInput } from '../models/ChatAskInput';
import type { ChatHistoryOutput } from '../models/ChatHistoryOutput';
import type { ChatOutput } from '../models/ChatOutput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ChatsService {
    /**
     * 用户发起新的聊天提问
     * @param payload
     * @returns ChatOutput 聊天记录创建成功
     * @throws ApiError
     */
    public static createChat(
        payload: ChatAskInput,
    ): CancelablePromise<ChatOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chats/',
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                404: `用户不存在`,
                500: `创建或处理失败`,
            },
        });
    }
    /**
     * 获取当前登录用户的聊天记录（分页）
     * @param perPage 每页数量
     * @param page 页码
     * @returns ChatHistoryOutput 成功获取聊天记录
     * @throws ApiError
     */
    public static getMyChatHistory(
        perPage: number = 20,
        page: number = 1,
    ): CancelablePromise<ChatHistoryOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/chats/',
            query: {
                'per_page': perPage,
                'page': page,
            },
            errors: {
                401: `需要认证`,
                500: `获取记录失败`,
            },
        });
    }
    /**
     * 直接调用 AI 模型进行对话 (不保存记录)
     * @param payload
     * @returns AiChatOutput AI 回复成功
     * @throws ApiError
     */
    public static directAiChat(
        payload: AiChatInput,
    ): CancelablePromise<AiChatOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chats/ai_direct',
            body: payload,
            errors: {
                400: `输入消息为空`,
                401: `需要认证`,
                429: `请求过于频繁`,
                500: `AI 服务调用失败`,
            },
        });
    }
    /**
     * 获取待处理 (Pending 或 Processing) 的聊天记录列表 (仅管理员/员工)
     * @param limit 最大返回数量
     * @returns ChatOutput 成功获取待处理列表
     * @throws ApiError
     */
    public static listPendingChats(
        limit: number = 100,
    ): CancelablePromise<Array<ChatOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/chats/pending',
            query: {
                'limit': limit,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                500: `获取失败`,
            },
        });
    }
    /**
     * 获取指定 ID 的聊天记录详情
     * @param chatId 聊天记录 ID
     * @returns ChatOutput 成功获取聊天详情
     * @throws ApiError
     */
    public static getChatDetail(
        chatId: number,
    ): CancelablePromise<ChatOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/chats/{chat_id}',
            path: {
                'chat_id': chatId,
            },
            errors: {
                401: `需要认证`,
                403: `无权查看此聊天记录`,
                404: `聊天记录未找到`,
                500: `获取失败`,
            },
        });
    }
    /**
     * 触发对指定聊天记录的 AI 回复处理 (仅管理员/员工)
     * @param chatId 聊天记录 ID
     * @returns ChatOutput 聊天记录处理成功
     * @throws ApiError
     */
    public static processChatAnswer(
        chatId: number,
    ): CancelablePromise<ChatOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chats/{chat_id}/process',
            path: {
                'chat_id': chatId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                404: `聊天记录未找到`,
                409: `聊天记录状态无法处理`,
                500: `处理失败`,
            },
        });
    }
}
