# -*- coding: utf-8 -*-
"""
@File       : test_dish.py
@Date       : 2025-04-11
@Desc       : This is the test file for dish.py. Rewritten with clear structure and fixtures.

@Version    : 2.0.0
"""
from uuid import uuid4


def test_add_dish_success(client, admin_header, ensure_category):
    from uuid import uuid4
    payload = {
        "name": f"测试菜品_{uuid4().hex[:6]}",
        "price": "19.9",
        "stock": 100,
        "category_id": ensure_category.category_id,  # ✅ 用新分类,
        "description": "测试描述",
        "image_url": "https://example.com/image.jpg",
        "is_available": True
    }
    response = client.post("/api/v1/dishes/", json=payload, headers=admin_header)
    print("响应内容：", response.get_json())
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert "dish_id" in json_data["data"]


def test_add_dish_missing_fields(client, admin_header, ensure_category):
    payload = {
        "name": f"缺失测试菜_{uuid4().hex[:6]}",
        "price": "18.5",
        "stock": 20,
        "category_id": ensure_category.category_id
    }
    response = client.post("/api/v1/dishes/", json=payload, headers=admin_header)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert "dish_id" in json_data["data"]


def test_get_dish_list_success(client):
    response = client.get("/api/v1/dishes/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert isinstance(json_data["data"], list)


def test_get_dish_not_found(client):
    response = client.get("/api/v1/dishes/999999")
    assert response.status_code in (404, 200)
    json_data = response.get_json()
    assert json_data["status"] == "fail"
    assert "Dish not found" in json_data["message"]


def test_update_dish_success(client, admin_header, ensure_category):
    create_payload = {
        "name": "原始菜品",
        "price": "25.0",
        "stock": 30,
        "category_id": ensure_category.category_id,
        "description": "原始描述",
        "image_url": "https://example.com/img.jpg",
        "is_available": True
    }
    res = client.post("/api/v1/dishes/", json=create_payload, headers=admin_header)
    dish_id = res.get_json()["data"]["dish_id"]

    update_payload = {
        "name": "更新后的菜品",
        "price": "29.9",
        "stock": 20,
        "category_id": ensure_category.category_id,
        "description": "已更新",
        "image_url": "https://example.com/updated.jpg"
    }
    update_res = client.put(f"/api/v1/dishes/{dish_id}", json=update_payload, headers=admin_header)
    assert update_res.status_code == 200
    json_data = update_res.get_json()
    assert json_data["data"]["name"] == "更新后的菜品"


def test_delete_dish_success(client, admin_header, ensure_category):
    payload = {
        "name": f"待删除菜品_{uuid4().hex[:6]}",
        "price": "20.0",
        "stock": 10,
        "category_id": ensure_category.category_id,
        "description": "测试",
        "image_url": "https://example.com/delete.jpg",
        "is_available": True
    }
    res = client.post("/api/v1/dishes/", json=payload, headers=admin_header)
    dish_id = res.get_json()["data"]["dish_id"]

    del_res = client.delete(f"/api/v1/dishes/{dish_id}", headers=admin_header)
    assert del_res.status_code == 204


def test_delete_dish_not_found(client, admin_header):
    res = client.delete("/api/v1/dishes/999999", headers=admin_header)
    assert res.status_code in (404, 200)
    json_data = res.get_json()
    assert json_data.get("status") == "fail"
    assert "Dish not found" in json_data.get("message", "")
