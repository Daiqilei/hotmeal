/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DishItemInput } from './DishItemInput';
export type OrderCreateInput = {
    /**
     * 订购的菜品列表 (至少包含一项)
     */
    dish_list: Array<DishItemInput>;
    /**
     * 用餐区域 ID (可选)
     */
    area_id?: number;
};

