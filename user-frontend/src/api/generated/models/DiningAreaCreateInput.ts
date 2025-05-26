/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DiningAreaCreateInput = {
    /**
     * 区域名称 (必须唯一)
     */
    area_name: string;
    /**
     * 最大容量 (正整数)
     */
    max_capacity?: number;
    /**
     * 区域类型
     */
    area_type: DiningAreaCreateInput.area_type;
};
export namespace DiningAreaCreateInput {
    /**
     * 区域类型
     */
    export enum area_type {
        PRIVATE = 'PRIVATE',
        TABLE = 'TABLE',
        BAR = 'BAR',
    }
}

