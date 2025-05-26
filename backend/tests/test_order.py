# -*- coding: utf-8 -*-
"""
@File       : test_order.py
@Date       : 2025-03-01
@Desc       : 订单接口测试
"""

from app.models.enums import OrderState
from app.utils.error_codes import ErrorCode


# add_order_success————————————————————————————————————————————————————————————

def test_add_order_success(client, admin_header, sample_dish,
                           sample_dining_area):
    payload = {
        "user_id": 1,
        "dish_list": [{"dish_id": sample_dish.dish_id, "quantity": 2}],
        "area_id": sample_dining_area.area_id
    }
    response = client.post("/api/v1/orders/", json=payload, headers=admin_header)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert "data" in json_data and "order_id" in json_data["data"]


def test_add_order_missing_fields(client, admin_header, sample_dish,
                                  sample_dining_area):
    payload = {"user_id": 1, "area_id": sample_dining_area.area_id}
    response = client.post("/api/v1/orders/", json=payload, headers=admin_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert "errors" in json_data
    assert "dish_list" in json_data["errors"]
    assert json_data["errors"][
               "dish_list"] == "'dish_list' is a required property"
    assert json_data["message"] == "Input payload validation failed"


def \
        test_add_order_empty_dish_list(client, admin_header, sample_dining_area):
    payload = {"user_id": 1, "area_id": sample_dining_area.area_id,
               "dish_list": []}
    response = client.post("/api/v1/orders/", json=payload, headers=admin_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.PARAM_INVALID.value


def test_add_order_invalid_dish_id(client, admin_header, sample_dining_area):
    payload = {"user_id": 1, "area_id": sample_dining_area.area_id,
               "dish_list": [{"dish_id": 99999, "quantity": 1}]}
    response = client.post("/api/v1/orders/", json=payload, headers=admin_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.DISH_NOT_FOUND.value


def test_add_order_exceed_stock(client, admin_header, sample_dish,
                                sample_dining_area):
    payload = {"user_id": 1, "area_id": sample_dining_area.area_id,
               "dish_list": [{"dish_id": sample_dish.dish_id, "quantity": 999}]}
    response = client.post("/api/v1/orders/", json=payload, headers=admin_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.INSUFFICIENT_STOCK.value


def test_list_orders_admin_success(client, admin_header):
    response = client.get("/api/v1/orders/", headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert "items" in json_data["data"]
    assert isinstance(json_data["data"]["items"], list)


def test_list_orders_user_forbidden(client, user_header):
    response = client.get("/api/v1/orders/", headers=user_header)

    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.FORBIDDEN.value


def test_get_order_by_id_admin_success(client, admin_header, create_test_order):
    order_id = create_test_order()
    # 在发送请求前获取 order 对象
    from app.models.order import Order
    order = Order.query.get(order_id)

    response = client.get(f"/api/v1/orders/{order_id}", headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert "data" in json_data and json_data["data"]["order_id"] == order_id


def test_get_order_by_id_not_found(client, admin_header):
    response = client.get("/api/v1/orders/99999", headers=admin_header)
    # print(response.get_json())  # 打印完整的 JSON 响应
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.ORDER_NOT_FOUND.value


def test_get_user_orders_success(client, user_header, create_test_order):
    create_test_order()
    response = client.get("/api/v1/orders/me", headers=user_header)
    print(f"Response status error_code: {response.status_code}")
    print(f"Response content type: {response.content_type}")
    print(f"Response data: {response.get_data(as_text=True)}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert isinstance(json_data["data"], list)
    assert len(json_data["data"]) >= 1


def test_get_user_orders_empty(client, user_header):
    response = client.get("/api/v1/orders/me", headers=user_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert isinstance(json_data["data"], list)
    assert len(json_data["data"]) == 0


# 更新系列测试


def test_update_order_admin_success(client, admin_header, create_test_order):
    order_id = create_test_order()
    payload = {"state": "PAID"}
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    assert json_data["data"]["state"] == "PAID"


def test_update_order_invalid_state(client, admin_header, create_test_order):
    order_id = create_test_order()
    payload = {"state": "INVALID"}
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=admin_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.PARAM_INVALID.value


def test_update_order_state_success(client, staff_header, create_test_order,
                                    app):
    order_id = create_test_order(state=OrderState.PENDING)
    payload = {"state": "PAID"}
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=staff_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value

    with app.app_context():
        from app.models import Order
        from app.utils.db import db
        updated_order = Order.query.get(order_id)
        db.session.refresh(updated_order)  # 刷新从当前会话获取的 order 对象
        db.session.commit()

    get_order_response = client.get(f"/api/v1/orders/{order_id}", headers=staff_header)
    assert get_order_response.get_json()["data"]["state"] == "PAID"


def test_update_order_state_invalid_transition(client, admin_header,
                                               create_test_order):
    # 创建一个订单并初始化状态为 PENDING
    order_id = create_test_order(state=OrderState.PENDING)

    # 尝试将订单状态更改为无效状态
    payload = {"state": "INVALID_STATE"}
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=admin_header)

    # 检查返回状态码是否是 400 (Bad Request)
    assert response.status_code == 400

    # 检查返回的错误码是否为 INVALID 状态转换的错误
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.PARAM_INVALID.value


def test_update_order_state_unauthorized(client, create_test_order, user_header,
                                         admin_header):
    order_id = create_test_order(state=OrderState.PENDING)
    payload = {"state": "PAID"}
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == 0

    # 尝试使用普通用户的 token 尝试更新订单状态
    response = client.put(f"/api/v1/orders/{order_id}", json=payload,
                          headers=user_header)
    assert response.status_code == 403
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.FORBIDDEN.value


def test_update_order_item_quantity_success(client, user_header,
                                            create_test_order, sample_dish):
    order_id = create_test_order(quantity=1)
    # 获取 order_item_id
    response = client.get(f"/api/v1/orders/{order_id}", headers=user_header)
    order_data = response.get_json()["data"]
    if order_data and order_data.get("order_items"):
        order_item_id = order_data["order_items"][0]["order_item_id"]
        payload = {"quantity": 3}
        print("订单ID:", order_id)
        print("订单项ID:", order_item_id)
        print("请求路径:", f"/api/v1/orders/{order_id}/item/{order_item_id}")
        print("请求数据:", payload)
        response_update = client.put(f"/api/v1/orders/{order_id}/item/{order_item_id}",
                                     json=payload, headers=user_header)
        print("响应状态码:", response_update.status_code)
        print("响应内容:", response_update.get_data(as_text=True))
        assert response_update.status_code == 200
        json_data_update = response_update.get_json()
        assert json_data_update["error_code"] == ErrorCode.SUCCESS.value
        updated_order_response = client.get(f"/api/v1/orders/{order_id}",
                                            headers=user_header)
        updated_order_data = updated_order_response.get_json()["data"]
        assert updated_order_data["order_items"][0]["quantity"] == 3


def test_update_order_item_quantity_invalid(client, user_header,
                                            create_test_order):
    order_id = create_test_order(quantity=1)
    # 获取 order_item_id
    response = client.get(f"/api/v1/orders/{order_id}", headers=user_header)
    order_data = response.get_json()["data"]
    if order_data and order_data.get("order_items"):
        order_item_id = order_data["order_items"][0]["order_item_id"]
        payload = {"quantity": 0}
        response_update = client.put(f"/api/v1/orders/{order_id}/item/{order_item_id}",
                                     json=payload, headers=user_header)
        print("响应状态码:", response_update.status_code)
        print("响应内容:", response_update.get_json())
        assert response_update.status_code == 400
        json_data_update = response_update.get_json()
        assert json_data_update["error_code"] == ErrorCode.PARAM_INVALID.value


def test_update_order_item_quantity_exceed_stock(client, user_header,
                                                 create_test_order,
                                                 sample_dish):
    order_id = create_test_order(quantity=1)
    # 获取 order_item_id
    response = client.get(f"/api/v1/orders/{order_id}", headers=user_header)
    order_data = response.get_json()["data"]
    if order_data and order_data.get("order_items"):
        order_item_id = order_data["order_items"][0]["order_item_id"]
        payload = {"quantity": 999}  # 超过默认的 sample_dish 库存 (100)
        response_update = client.put(f"/api/v1/orders/{order_id}/item/{order_item_id}",
                                     json=payload, headers=user_header)
        assert response_update.status_code == 400
        json_data_update = response_update.get_json()
        assert json_data_update[
                   "error_code"] == ErrorCode.INSUFFICIENT_STOCK.value


# FIXME
def test_cancel_order_success(client, user_header, create_test_order):
    import logging
    logger = logging.getLogger(__name__)
    order_id = create_test_order(state=OrderState.PENDING)
    logger.info(f"Order ID: {order_id}\n")
    response = client.put(f"/api/v1/orders/{order_id}/cancel", headers=user_header)
    logger.info(response.get_json())
    logger.info(response.data)
    logger.info(response.status_code)
    logger.info("日志测试\n")
    assert response.status_code == 200

    logger.info(response.data)
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value
    logger.info(json_data.get("data"))
    get_order_response = client.get(f"/api/v1/orders/{order_id}", headers=user_header)
    assert get_order_response.get_json()["data"]["state"] == "CANCELED"


def test_cancel_order_not_found(client, user_header):
    response = client.put("/api/v1/orders/99999/cancel", headers=user_header)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.ORDER_NOT_FOUND.value


def test_cancel_order_invalid_state(client, user_header, create_test_order):
    order_id = create_test_order(state=OrderState.PAID)  # 假设 PAID 状态不能取消
    response = client.put(f"/api/v1/orders/{order_id}/cancel", headers=user_header)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.ORDER_STATE_INVALID.value


def test_cancel_order_unauthorized(client, create_test_order, user_header,
                                   admin_header):
    order_id = create_test_order(state=OrderState.PENDING)
    # 使用管理员的 token 尝试取消普通用户的订单
    response = client.put(f"/api/v1/orders/{order_id}/cancel", headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value


# 删除系列测试———————————————————————————————————————————————————————————————————


def test_hard_delete_order_admin_success(client, admin_header,
                                         create_test_order):
    order_id = create_test_order()
    response = client.delete(f"/api/v1/orders/{order_id}/delete?permanent=true",
                             headers=admin_header)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.SUCCESS.value


def test_hard_delete_order_not_found(client, admin_header):
    print(client.application.url_map)  # 打印 URL 映射
    response = client.delete("/api/v1/orders/99999/delete?permanent=true", headers=admin_header)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["error_code"] == ErrorCode.ORDER_NOT_FOUND.value
