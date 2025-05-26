/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CategoryOutput = {
    /**
     * 分类 ID
     */
    category_id?: number;
    /**
     * 分类名称
     */
    name?: string;
    /**
     * 描述
     */
    description?: string;
    /**
     * 图片 URL
     */
    img_url?: string;
    /**
     * 父分类 ID
     */
    parent_category_id?: number;
    /**
     * 子分类数量
     */
    subcategories_count?: number;
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
};

