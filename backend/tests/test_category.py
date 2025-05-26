# -*- coding: utf-8 -*-
"""
@File       : test_category.py
@Date       : 2025-03-01
@Desc       : 测试分类管理相关的 API 路由（基于 pytest）


"""
from uuid import uuid4


def test_create_category(client, admin_header):
    """测试创建分类"""
    category_data = {
        "name": f"新建分类_{uuid4().hex}",
        "description": "测试分类",
        "img_url": "",
    }
    response = client.post('/api/v1/categories/', json=category_data, headers=admin_header)
    print("请求数据:", category_data)
    print("响应状态码:", response.status_code)
    print("响应 JSON:", response.json)
    assert response.status_code == 201
    assert response.json.get("data", {}).get("name") == category_data["name"]


def test_get_categories(client, admin_header, preset_categories):
    """测试获取所有分类"""
    assert preset_categories, "No preset categories available for test"

    response = client.get('/api/v1/categories/', headers=admin_header)
    assert response.status_code == 200
    # 返回数据格式应该是一个列表，列表中每项为分类信息
    data = response.json.get("data", [])
    assert isinstance(data, list)
    # 至少存在一条分类记录（测试环境）
    assert len(data) >= 1
    # 可选：检查某个已知分类是否存在
    names = [item.get("name") for item in data if
             isinstance(item, dict)]
    assert any(name for name in names)


def test_get_category(client, admin_header, preset_categories):
    """测试根据 ID 获取单个分类"""
    category_id = preset_categories[0].category_id
    response = client.get(f'/api/v1/categories/{category_id}', headers=admin_header)
    assert response.status_code == 200

    data = response.json.get("data", {})

    expected = preset_categories[0]
    assert data.get("name") == expected.name
    assert data.get("description") == expected.description


def test_update_category(client, admin_header, preset_categories):
    """测试更新单个分类"""
    assert preset_categories, "No preset categories available for test"

    category_id = preset_categories[0].category_id
    updated_data = {
        "name": f"更新分类_{uuid4().hex}",
        "description": "更新后的描述"
    }
    response = client.put(f'/api/v1/categories/{category_id}', json=updated_data,
                          headers=admin_header)

    assert response.status_code == 200
    # 检查更新后返回的数据，如果数据在 data 子对象中返回
    data = response.json.get("data", {})
    # 假设接口中更新后的分类名称存储在字段 name
    assert data.get("name") == updated_data["name"]
    # 更新后的描述也应正确返回
    if "description" in data:
        assert data.get("description") == "更新后的描述"


def test_delete_category(client, app, admin_header, preset_categories):
    """测试删除单个分类"""
    # 创建一个随机名称的分类用于删除测试，确保每次测试使用独立数据
    new_category_data = {
        "name": f"删除分类_{uuid4().hex}",
        "description": "用于删除测试的分类",
        "img_url": "",
    }
    create_response = client.post('/api/v1/categories/', json=new_category_data,
                                  headers=admin_header)
    print("请求数据:", new_category_data)
    print("响应状态码:", create_response.status_code)
    print("响应 JSON:", create_response.json)
    assert create_response.status_code == 201
    category_to_delete = create_response.json.get("data", {})
    category_id = category_to_delete.get("category_id")
    response = client.delete(f'/api/v1/categories/{category_id}', headers=admin_header)
    assert response.status_code == 204

    # assert response.json.get("message") == "Successfully deleted category"

    # 调用接口验证分类是否已被删除
    response_check = client.get(f'/api/v1/categories/{category_id}', headers=admin_header)
    assert response_check.status_code == 404
    assert response_check.json.get("message") == "Category not found"
