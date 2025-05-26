/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DiningAreaOutput = {
    /**
     * 区域 ID
     */
    area_id?: number;
    /**
     * 区域名称
     */
    area_name?: string;
    /**
     * 当前状态
     */
    state?: string;
    /**
     * 区域类型
     */
    area_type?: string;
    /**
     * 最大容量
     */
    max_capacity?: number;
    /**
     * 使用次数
     */
    usage_count?: number;
    /**
     * 当前占用用户 ID
     */
    assigned_user_id?: number;
    /**
     * 当前占用用户名
     */
    assigned_username?: string;
    /**
     * 上次使用时间 (ISO 格式)
     */
    last_used?: string;
    /**
     * 创建时间 (ISO 格式)
     */
    created_at?: string;
    /**
     * 更新时间 (ISO 格式)
     */
    updated_at?: string;
};

