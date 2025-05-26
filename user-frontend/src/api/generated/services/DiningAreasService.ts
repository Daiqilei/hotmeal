/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DiningAreaAssignInput } from '../models/DiningAreaAssignInput';
import type { DiningAreaCreateInput } from '../models/DiningAreaCreateInput';
import type { DiningAreaOutput } from '../models/DiningAreaOutput';
import type { DiningAreaUpdateInput } from '../models/DiningAreaUpdateInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DiningAreasService {
    /**
     * 创建新的用餐区域 (仅管理员)
     * @param payload
     * @returns DiningAreaOutput 用餐区域创建成功
     * @throws ApiError
     */
    public static createDiningArea(
        payload: DiningAreaCreateInput,
    ): CancelablePromise<DiningAreaOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dining-areas/',
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                409: `区域名称已存在`,
                500: `创建失败`,
            },
        });
    }
    /**
     * 获取用餐区域列表 (可选按类型和状态过滤)
     * @param state 按状态过滤 (FREE, OCCUPIED)
     * @param areaType 按区域类型过滤 (PRIVATE, TABLE, BAR)
     * @returns DiningAreaOutput 成功获取用餐区域列表
     * @throws ApiError
     */
    public static listDiningAreas(
        state?: string,
        areaType?: string,
    ): CancelablePromise<Array<DiningAreaOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dining-areas/',
            query: {
                'state': state,
                'area_type': areaType,
            },
            errors: {
                400: `无效的过滤参数`,
                500: `获取列表失败`,
            },
        });
    }
    /**
     * 更新指定 ID 的用餐区域信息 (仅管理员)
     * @param areaId 用餐区域 ID
     * @param payload
     * @returns DiningAreaOutput 用餐区域更新成功
     * @throws ApiError
     */
    public static updateDiningArea(
        areaId: number,
        payload: DiningAreaUpdateInput,
    ): CancelablePromise<DiningAreaOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/dining-areas/{area_id}',
            path: {
                'area_id': areaId,
            },
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `用餐区域未找到`,
                409: `名称冲突`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 获取指定 ID 的用餐区域详情 (仅管理员)
     * @param areaId 用餐区域 ID
     * @returns DiningAreaOutput 成功获取用餐区域详情
     * @throws ApiError
     */
    public static getDiningAreaDetail(
        areaId: number,
    ): CancelablePromise<DiningAreaOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dining-areas/{area_id}',
            path: {
                'area_id': areaId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `用餐区域未找到`,
                500: `获取失败`,
            },
        });
    }
    /**
     * 永久删除指定 ID 的用餐区域 (仅管理员)
     * @param areaId 用餐区域 ID
     * @returns void
     * @throws ApiError
     */
    public static deleteDiningArea(
        areaId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/dining-areas/{area_id}',
            path: {
                'area_id': areaId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `用餐区域未找到`,
                409: `区域被占用或有关联数据，无法删除`,
                500: `删除失败`,
            },
        });
    }
    /**
     * 将空闲区域分配给指定用户 (仅管理员/员工)
     * @param areaId 用餐区域 ID
     * @param payload
     * @returns DiningAreaOutput 用餐区域分配成功
     * @throws ApiError
     */
    public static assignDiningArea(
        areaId: number,
        payload: DiningAreaAssignInput,
    ): CancelablePromise<DiningAreaOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dining-areas/{area_id}/assign',
            path: {
                'area_id': areaId,
            },
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                404: `区域或User not found`,
                409: `区域已被占用`,
                500: `分配失败`,
            },
        });
    }
    /**
     * 释放一个占用的用餐区域 (仅管理员/员工)
     * @param areaId 用餐区域 ID
     * @returns DiningAreaOutput 用餐区域释放成功
     * @throws ApiError
     */
    public static releaseDiningArea(
        areaId: number,
    ): CancelablePromise<DiningAreaOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dining-areas/{area_id}/release',
            path: {
                'area_id': areaId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                404: `区域未找到`,
                500: `释放失败`,
            },
        });
    }
}
