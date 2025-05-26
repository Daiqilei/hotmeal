/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ChatOutput = {
    /**
     * 聊天记录 ID
     */
    chat_id?: number;
    /**
     * 用户 ID
     */
    user_id?: number;
    /**
     * 用户问题/内容
     */
    question?: string;
    /**
     * AI/人工回复内容
     */
    answer?: string;
    /**
     * 状态
     */
    status?: string;
    /**
     * 创建时间 (ISO 格式)
     */
    created_at?: string;
    /**
     * 更新时间 (ISO 格式)
     */
    updated_at?: string;
    /**
     * AI 响应时间 (秒)
     */
    response_time?: number;
    /**
     * AI 置信度
     */
    confidence?: number;
    /**
     * 回复来源 (AI/人工)
     */
    source?: string;
    /**
     * 标签
     */
    tags?: string;
    /**
     * 消息类型
     */
    message_type?: string;
    /**
     * AI 处理时长 (秒)
     */
    response_duration?: number;
    /**
     * 图片 URL
     */
    image_url?: string;
};

