/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemOutput } from './OrderItemOutput';
export type OrderOutput = {
    /**
     * 订单 ID
     */
    order_id?: number;
    /**
     * 用户 ID
     */
    user_id?: number;
    /**
     * 区域 ID
     */
    area_id?: number;
    /**
     * 订单状态
     */
    state?: string;
    /**
     * 订单总金额 (字符串)
     */
    price?: string;
    /**
     * 支付方式
     */
    payment_method?: string;
    /**
     * 支付凭证 URL
     */
    image_url?: string;
    /**
     * 创建时间 (ISO 格式)
     */
    created_at?: string;
    /**
     * 更新时间 (ISO 格式)
     */
    updated_at?: string;
    /**
     * 删除时间 (ISO 格式)
     */
    deleted_at?: string;
    /**
     * 订单项列表
     */
    order_items?: Array<OrderItemOutput>;
};

