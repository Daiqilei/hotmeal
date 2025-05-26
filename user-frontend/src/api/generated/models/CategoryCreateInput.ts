/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CategoryCreateInput = {
    /**
     * 分类名称 (必须唯一)
     */
    name: string;
    /**
     * 分类描述
     */
    description?: string;
    /**
     * 图片链接 (URL)
     */
    img_url?: string;
    /**
     * 父分类 ID (可选, 用于创建子分类)
     */
    parent_category_id?: number;
};

