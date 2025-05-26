/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DiningAreaUpdateInput = {
    /**
     * 新区域名称
     */
    area_name?: string;
    /**
     * 新最大容量 (正整数)
     */
    max_capacity?: number;
    /**
     * 新区域类型
     */
    area_type?: DiningAreaUpdateInput.area_type;
};
export namespace DiningAreaUpdateInput {
    /**
     * 新区域类型
     */
    export enum area_type {
        PRIVATE = 'PRIVATE',
        TABLE = 'TABLE',
        BAR = 'BAR',
    }
}

