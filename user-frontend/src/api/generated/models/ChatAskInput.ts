/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ChatAskInput = {
    /**
     * 用户的问题或内容
     */
    question: string;
    /**
     * 消息类型
     */
    message_type?: ChatAskInput.message_type;
    /**
     * 图片 URL (如果消息类型是 IMAGE)
     */
    image_url?: string;
    /**
     * 标签 (逗号分隔)
     */
    tags?: string;
    /**
     * 是否立即尝试获取 AI 回复 (默认 True)
     */
    process_sync?: boolean;
};
export namespace ChatAskInput {
    /**
     * 消息类型
     */
    export enum message_type {
        TEXT = 'TEXT',
        VOICE = 'VOICE',
        IMAGE = 'IMAGE',
    }
}

