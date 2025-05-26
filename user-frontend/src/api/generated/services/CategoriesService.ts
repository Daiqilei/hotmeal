/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CategoryCreateInput } from '../models/CategoryCreateInput';
import type { CategoryOutput } from '../models/CategoryOutput';
import type { CategoryUpdateInput } from '../models/CategoryUpdateInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CategoriesService {
    /**
     * 创建新分类 (仅管理员)
     * @param payload
     * @returns CategoryOutput 分类创建成功
     * @throws ApiError
     */
    public static createCategory(
        payload: CategoryCreateInput,
    ): CancelablePromise<CategoryOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/categories/',
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                409: `分类名称已存在`,
                500: `创建失败`,
            },
        });
    }
    /**
     * 获取分类列表 (可选按父 ID 过滤，可选包含已删除)
     * @param parentId 按父分类 ID 过滤 (不传表示获取顶级分类)
     * @param includeDeleted 是否包含已删除的分类 (true/false)
     * @returns CategoryOutput 成功获取分类列表
     * @throws ApiError
     */
    public static listCategories(
        parentId?: number,
        includeDeleted: boolean = false,
    ): CancelablePromise<Array<CategoryOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/categories/',
            query: {
                'parent_id': parentId,
                'include_deleted': includeDeleted,
            },
            errors: {
                500: `获取列表失败`,
            },
        });
    }
    /**
     * 更新指定 ID 的分类信息 (仅管理员)
     * @param categoryId 分类 ID
     * @param payload
     * @returns CategoryOutput 分类更新成功
     * @throws ApiError
     */
    public static updateCategory(
        categoryId: number,
        payload: CategoryUpdateInput,
    ): CancelablePromise<CategoryOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `分类未找到`,
                409: `分类名称已存在或父分类无效`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 获取指定 ID 的分类详情 (可选包含已删除)
     * @param categoryId 分类 ID
     * @param includeDeleted 是否包含已删除的分类 (true/false)
     * @returns CategoryOutput 成功获取分类详情
     * @throws ApiError
     */
    public static getCategoryDetail(
        categoryId: number,
        includeDeleted: boolean = false,
    ): CancelablePromise<CategoryOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            query: {
                'include_deleted': includeDeleted,
            },
            errors: {
                404: `分类未找到`,
                500: `获取详情失败`,
            },
        });
    }
    /**
     * 删除指定 ID 的分类 (默认为软删除，可选永久删除，仅管理员)
     * @param categoryId 分类 ID
     * @param permanent 是否永久删除 (true/false)，默认为软删除
     * @returns void
     * @throws ApiError
     */
    public static deleteCategory(
        categoryId: number,
        permanent: boolean = false,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            query: {
                'permanent': permanent,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `分类未找到`,
                409: `无法删除，存在子分类或关联数据`,
                500: `删除失败`,
            },
        });
    }
    /**
     * 恢复软删除的分类 (仅管理员)
     * @param categoryId 分类 ID
     * @returns CategoryOutput 分类恢复成功
     * @throws ApiError
     */
    public static restoreCategory(
        categoryId: number,
    ): CancelablePromise<CategoryOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/categories/{category_id}/restore',
            path: {
                'category_id': categoryId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `分类未找到或无需恢复`,
                409: `无法恢复（例如父分类已删除）`,
                500: `恢复失败`,
            },
        });
    }
}
