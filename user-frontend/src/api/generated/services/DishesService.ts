/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DishCreateInput } from '../models/DishCreateInput';
import type { DishOutput } from '../models/DishOutput';
import type { DishUpdateInput } from '../models/DishUpdateInput';
import type { SetAvailabilityInput } from '../models/SetAvailabilityInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DishesService {
    /**
     * 创建新菜品 (仅管理员)
     * @param payload
     * @returns DishOutput 菜品创建成功
     * @throws ApiError
     */
    public static createDish(
        payload: DishCreateInput,
    ): CancelablePromise<DishOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dishes/',
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                409: `菜品名称已存在`,
                500: `创建失败`,
            },
        });
    }
    /**
     * 获取所有可用的菜品列表 (公开访问)
     * @param categoryId 按分类 ID 过滤 (可选)
     * @returns DishOutput 成功获取可用菜品列表
     * @throws ApiError
     */
    public static listAvailableDishes(
        categoryId?: number,
    ): CancelablePromise<Array<DishOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dishes/',
            query: {
                'category_id': categoryId,
            },
            errors: {
                500: `获取列表失败`,
            },
        });
    }
    /**
     * 更新指定 ID 的菜品信息 (仅管理员)
     * @param dishId 菜品 ID
     * @param payload
     * @returns DishOutput 菜品更新成功
     * @throws ApiError
     */
    public static updateDish(
        dishId: number,
        payload: DishUpdateInput,
    ): CancelablePromise<DishOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/dishes/{dish_id}',
            path: {
                'dish_id': dishId,
            },
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `菜品未找到`,
                409: `菜品名称已存在`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 获取指定 ID 的菜品详情 (公开访问)
     * @param dishId 菜品 ID
     * @returns DishOutput 成功获取菜品详情
     * @throws ApiError
     */
    public static getDishDetail(
        dishId: number,
    ): CancelablePromise<DishOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dishes/{dish_id}',
            path: {
                'dish_id': dishId,
            },
            errors: {
                404: `菜品未找到`,
                500: `获取详情失败`,
            },
        });
    }
    /**
     * 永久删除指定 ID 的菜品 (硬删除，仅管理员)
     * @param dishId 菜品 ID
     * @returns void
     * @throws ApiError
     */
    public static deleteDishPermanently(
        dishId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/dishes/{dish_id}',
            path: {
                'dish_id': dishId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `菜品未找到`,
                409: `无法删除，存在关联数据`,
                500: `删除失败`,
            },
        });
    }
    /**
     * 设置菜品的上架或下架状态 (仅管理员)
     * @param dishId 菜品 ID
     * @param payload
     * @returns any 菜品可用性设置成功
     * @throws ApiError
     */
    public static setDishAvailability(
        dishId: number,
        payload: SetAvailabilityInput,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/dishes/{dish_id}/availability',
            path: {
                'dish_id': dishId,
            },
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `菜品未找到`,
                500: `设置失败`,
            },
        });
    }
}
