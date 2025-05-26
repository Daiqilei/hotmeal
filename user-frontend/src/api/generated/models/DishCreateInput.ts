/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DishCreateInput = {
    /**
     * 菜品名称
     */
    name: string;
    /**
     * 价格 (格式如 "19.99")
     */
    price: string;
    /**
     * 库存数量 (非负整数)
     */
    stock: number;
    /**
     * 所属分类 ID
     */
    category_id: number;
    /**
     * 图片链接 (URL)
     */
    image_url?: string;
    /**
     * 初始销量 (非负整数)
     */
    sales?: number;
    /**
     * 初始评分 (0.0-5.0)
     */
    rating?: number;
    /**
     * 菜品描述
     */
    description?: string;
    /**
     * 是否上架
     */
    is_available?: boolean;
};

