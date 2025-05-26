# -*- coding: utf-8 -*-
"""
@File       : test_integration.py
@Date       : 2025-03-01
@Desc       :


"""


def test_full_order_flow(client):
    # Step 1: 创建分类
    client.post("/api/v1/category/add", json={"area_name": "热菜"})

    # Step 2: 创建菜品（假设你有 dish 接口）
    client.post("/api/v1/dish/add", json={
        "area_name": "宫保鸡丁",
        "price": 25.0,
        "category_id": 1,
        "description": "经典川菜",
        "image_url": "",
        "state": 1
    })

    # Step 3: 下订单
    response = client.post("/api/v1/order/create", json={
        "user_id": 1,
        "items": [{"dish_id": 1, "quantity": 2}]
    })
    assert response.status_code == 200
    assert "order_id" in response.json["data"]

    # Step 4: 查询订单列表
    response = client.get("/api/v1/order/user/1")
    assert response.status_code == 200
    assert isinstance(response.json["data"], list)


def test_recommendation_after_order(client):
    # 假设用户下过单后，推荐系统应生效
    response = client.get("/api/v1/recommend/user/1")
    assert response.status_code == 200
    assert isinstance(response.json["data"], list)
