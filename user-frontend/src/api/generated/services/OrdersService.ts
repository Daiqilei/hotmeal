/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderCreateInput } from '../models/OrderCreateInput';
import type { OrderListOutput } from '../models/OrderListOutput';
import type { OrderOutput } from '../models/OrderOutput';
import type { OrderUpdateInput } from '../models/OrderUpdateInput';
import type { UpdateOrderItemQuantity } from '../models/UpdateOrderItemQuantity';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OrdersService {
    /**
     * 创建新订单
     * @param payload
     * @returns OrderOutput 订单创建成功
     * @throws ApiError
     */
    public static createOrder(
        payload: OrderCreateInput,
    ): CancelablePromise<OrderOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/orders/',
            body: payload,
            errors: {
                400: `输入参数无效`,
                401: `需要认证`,
                404: `用户、区域或菜品未找到`,
                409: `库存不足或菜品不可用`,
                500: `创建订单失败`,
            },
        });
    }
    /**
     * 获取所有订单的分页列表 (仅管理员/员工)
     * @param includeItems 是否包含订单项详情
     * @param perPage 每页数量
     * @param page 页码
     * @returns OrderListOutput 成功获取订单列表 (分页)
     * @throws ApiError
     */
    public static listAllOrders(
        includeItems: boolean = false,
        perPage: number = 10,
        page: number = 1,
    ): CancelablePromise<OrderListOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/orders/',
            query: {
                'include_items': includeItems,
                'per_page': perPage,
                'page': page,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                500: `获取列表失败`,
            },
        });
    }
    /**
     * 获取当前登录用户的订单列表
     * @param includeItems 是否包含订单项详情 (true/false)
     * @returns OrderOutput 成功获取我的订单列表
     * @throws ApiError
     */
    public static getMyOrders(
        includeItems: boolean = false,
    ): CancelablePromise<Array<OrderOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/orders/me',
            query: {
                'include_items': includeItems,
            },
            errors: {
                401: `需要认证`,
                500: `获取订单失败`,
            },
        });
    }
    /**
     * 更新指定订单的信息 (状态、支付方式等，仅管理员/员工)
     * @param orderId 订单 ID
     * @param payload
     * @returns OrderOutput 订单信息更新成功
     * @throws ApiError
     */
    public static updateOrderDetails(
        orderId: number,
        payload: OrderUpdateInput,
    ): CancelablePromise<OrderOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/orders/{order_id}',
            path: {
                'order_id': orderId,
            },
            body: payload,
            errors: {
                400: `输入参数无效或状态转换无效`,
                401: `需要认证`,
                403: `需要管理员或员工权限`,
                404: `订单未找到`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 获取指定 ID 的订单详情 (管理员/员工或订单所有者)
     * @param orderId 订单 ID
     * @param includeItems 是否包含订单项详情
     * @returns OrderOutput 成功获取订单详情
     * @throws ApiError
     */
    public static getOrderDetail(
        orderId: number,
        includeItems: boolean = true,
    ): CancelablePromise<OrderOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/orders/{order_id}',
            path: {
                'order_id': orderId,
            },
            query: {
                'include_items': includeItems,
            },
            errors: {
                401: `需要认证`,
                403: `无权查看此订单`,
                404: `订单未找到`,
                500: `获取失败`,
            },
        });
    }
    /**
     * 取消一个待处理的订单 (管理员/员工或订单所有者)
     * @param orderId 订单 ID
     * @returns any 订单取消成功
     * @throws ApiError
     */
    public static cancelOrder(
        orderId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/orders/{order_id}/cancel',
            path: {
                'order_id': orderId,
            },
            errors: {
                401: `需要认证`,
                403: `无权取消此订单`,
                404: `订单未找到`,
                409: `订单状态无法取消`,
                500: `取消失败`,
            },
        });
    }
    /**
     * 删除订单 (管理员/员工或所有者可软删除, 仅管理员可硬删除)
     * @param orderId 订单 ID
     * @param permanent 是否永久删除 (true/false)，默认为软删除
     * @returns void
     * @throws ApiError
     */
    public static deleteOrder(
        orderId: number,
        permanent: boolean = false,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/orders/{order_id}/delete',
            path: {
                'order_id': orderId,
            },
            query: {
                'permanent': permanent,
            },
            errors: {
                401: `需要认证`,
                403: `无权删除此订单 (硬删除需要管理员)`,
                404: `订单未找到`,
                409: `无法删除，存在依赖或状态不允许`,
                500: `删除失败`,
            },
        });
    }
    /**
     * 更新指定订单项的数量
     * @param orderItemId 订单项 ID
     * @param orderId 订单 ID
     * @param payload
     * @returns any 订单项数量更新成功
     * @throws ApiError
     */
    public static updateOrderItemQuantity(
        orderItemId: number,
        orderId: number,
        payload: UpdateOrderItemQuantity,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/orders/{order_id}/item/{order_item_id}',
            path: {
                'order_item_id': orderItemId,
                'order_id': orderId,
            },
            body: payload,
            errors: {
                400: `参数错误`,
                401: `未授权`,
                403: `无权修改此订单项`,
                404: `订单或订单项未找到`,
                409: `库存不足或订单状态不允许修改`,
            },
        });
    }
}
