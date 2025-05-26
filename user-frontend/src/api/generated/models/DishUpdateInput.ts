/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DishUpdateInput = {
    /**
     * 新菜品名称
     */
    name?: string;
    /**
     * 新价格 (格式如 "19.99")
     */
    price?: string;
    /**
     * 新库存数量 (非负整数)
     */
    stock?: number;
    /**
     * 新所属分类 ID
     */
    category_id?: number;
    /**
     * 新图片链接 (URL)
     */
    image_url?: string;
    /**
     * 新销量 (非负整数)
     */
    sales?: number;
    /**
     * 新评分 (0.0-5.0)
     */
    rating?: number;
    /**
     * 新菜品描述
     */
    description?: string;
    /**
     * 新上架状态
     */
    is_available?: boolean;
};

