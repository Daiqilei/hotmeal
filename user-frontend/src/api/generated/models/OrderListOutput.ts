/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderOutput } from './OrderOutput';
export type OrderListOutput = {
    items?: Array<OrderOutput>;
    /**
     * 当前页码
     */
    page?: number;
    /**
     * 每页数量
     */
    per_page?: number;
    /**
     * 总项目数
     */
    total_items?: number;
    /**
     * 总页数
     */
    total_pages?: number;
};

