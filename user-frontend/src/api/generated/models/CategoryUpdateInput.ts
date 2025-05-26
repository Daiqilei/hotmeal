/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CategoryUpdateInput = {
    /**
     * 新分类名称
     */
    name?: string;
    /**
     * 新分类描述
     */
    description?: string;
    /**
     * 新图片链接
     */
    img_url?: string;
    /**
     * 新的父分类 ID (设置 null 表示顶级分类)
     */
    parent_category_id?: number;
};

