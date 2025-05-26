/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RecommendationOutput } from '../models/RecommendationOutput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RecommendationsService {
    /**
     * 获取当前登录用户的推荐菜品列表
     * @param limit 返回的推荐数量上限
     * @returns RecommendationOutput 成功获取推荐列表
     * @throws ApiError
     */
    public static getRecommendations(
        limit: number = 10,
    ): CancelablePromise<RecommendationOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/recommendations/',
            query: {
                'limit': limit,
            },
            errors: {
                401: `需要认证或令牌无效`,
                500: `获取推荐时发生错误`,
            },
        });
    }
}
