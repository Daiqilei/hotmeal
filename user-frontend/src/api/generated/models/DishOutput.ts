/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type DishOutput = {
    /**
     * 菜品 ID
     */
    dish_id?: number;
    /**
     * 菜品名称
     */
    name?: string;
    /**
     * 价格
     */
    price?: string;
    /**
     * 库存数量
     */
    stock?: number;
    /**
     * 图片链接
     */
    image_url?: string;
    /**
     * 销量
     */
    sales?: number;
    /**
     * 评分
     */
    rating?: number;
    /**
     * 描述
     */
    description?: string;
    /**
     * 分类 ID
     */
    category_id?: number;
    /**
     * 分类名称
     */
    category_name?: string;
    /**
     * 是否上架
     */
    is_available?: boolean;
    /**
     * 创建时间 (ISO 格式)
     */
    created_at?: string;
    /**
     * 更新时间 (ISO 格式)
     */
    updated_at?: string;
};

