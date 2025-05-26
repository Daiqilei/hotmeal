/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type OrderUpdateInput = {
    /**
     * 订单状态 (例如: PAID, COMPLETED)
     */
    state?: string;
    /**
     * 支付方式 (例如: WECHAT, ALIPAY)
     */
    payment_method?: string;
    /**
     * 支付凭证图片 URL
     */
    image_url?: string;
};

