# -*- coding: utf-8 -*-
"""
@File       : test_dining_area.py
@Date       : 2025-03-01 
@Desc       : Test cases for the Dining Area API endpoints.


"""

import logging  # 添加日志
import uuid  # 用于生成唯一名称
from http import HTTPStatus
import pytest

# 导入模型枚举
from app.models.enums import DiningAreaState, AreaType
from app.models import DiningArea


logger = logging.getLogger("test")  # 使用测试 logger


# --- 测试用例 ---

def test_create_dining_area_success(client, admin_header):
    """Test creating a dining area successfully as admin."""
    unique_name = f"包间_{uuid.uuid4().hex[:8]}"  # 使用 UUID 生成唯一名称
    payload = {
        "area_name": unique_name,
        "max_capacity": 8,
        "area_type": AreaType.PRIVATE.name  # 使用枚举名称
    }
    response = client.post("/api/v1/dining-areas/", json=payload,
                           headers=admin_header)  # 使用新路径 POST /api/v1/dining-areas/

    logger.debug(f"Create response status: {response.status_code}, json: {response.json}")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["status"] == "success"
    assert response.json["error_code"] == 0
    # assert response.json["message"] == "用餐区域创建成功" # 可以断言消息，但数据更重要

    data = response.json["data"]
    assert data["area_name"] == unique_name
    assert data["max_capacity"] == 8
    assert data["area_type"] == AreaType.PRIVATE.name
    assert data["state"] == DiningAreaState.FREE.name  # 默认应为 FREE
    assert data["area_id"] is not None
    assert data["usage_count"] == 0
    assert data["assigned_user_id"] is None


def test_create_dining_area_duplicate_name(client, admin_header, sample_dining_area):
    """Test creating a dining area with a duplicate name."""
    payload = {
        "area_name": sample_dining_area.area_name,  # 使用已存在的名称
        "max_capacity": 4,
        "area_type": AreaType.TABLE.name
    }
    response = client.post("/api/v1/dining-areas/", json=payload, headers=admin_header)

    logger.debug(f"Duplicate name response status: {response.status_code}, json: {response.json}")
    assert response.status_code == HTTPStatus.BAD_REQUEST  # 或 CONFLICT (取决于服务层实现)
    assert response.json["status"] == "fail"
    # assert response.json["error_code"] == ErrorCode.HTTP_CONFLICT.value # 假设服务层抛 BusinessError(..., CONFLICT)
    assert "Dining area name already exists." in response.json["message"]


def test_create_dining_area_invalid_data(client, admin_header):
    """Test creating a dining area with invalid data."""
    payloads = [
        {"area_name": "Test", "max_capacity": 10, "area_type": "INVALID_TYPE"},  # area_type 无效
        {"area_name": "", "max_capacity": 10, "area_type": "TABLE"},  # area_name 为空
    ]
    for payload in payloads:
        response = client.post("/api/v1/dining-areas/", json=payload, headers=admin_header)
        logger.debug(f"Invalid data payload: {payload}, response: {response.data}")
        assert response.status_code == HTTPStatus.BAD_REQUEST

        if response.is_json:
            json_data = response.get_json()
            # 判断 status 字段是否存在
            if "status" in json_data:
                assert json_data["status"] == "fail"
            else:
                # fallback：只要包含 message 或 errors，就认为是失败响应
                assert "message" in json_data or "errors" in json_data
        else:
            logger.error(f"响应不是 JSON 格式: {response.data}")
            pytest.fail("接口返回非 JSON 响应")


def test_create_dining_area_unauthorized(client):
    """Test creating a dining area without authentication."""
    payload = {"area_name": "Unauthorized Area", "max_capacity": 2, "area_type": "BAR"}
    response = client.post("/api/v1/dining-areas/", json=payload)  # 不带 header
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_dining_area_forbidden(client, user_header):  # 使用普通用户 token
    """Test creating a dining area with insufficient permissions."""
    payload = {"area_name": "Forbidden Area", "max_capacity": 2, "area_type": "BAR"}
    response = client.post("/api/v1/dining-areas/", json=payload, headers=user_header)  # 使用普通用户 header
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_list_dining_areas(client, admin_header,
                           sample_dining_area):  # 添加 sample_dining_area 确保至少有一条数据
    """Test listing all dining areas as admin."""
    response = client.get("/api/v1/dining-areas/", headers=admin_header)  # 使用新路径 GET /api/v1/dining-areas/

    assert response.status_code == HTTPStatus.OK
    assert response.json["status"] == "success"
    assert isinstance(response.json["data"], list)
    # 可以进一步断言列表不为空，或包含 sample_dining_area 的数据
    assert len(response.json["data"]) > 0
    found = any(item['area_id'] == sample_dining_area.area_id for item in response.json["data"])
    assert found, "Sample dining area not found in list"


def test_list_dining_areas_filtered(client, admin_header, sample_dining_area):
    """Test filtering dining areas by type and state."""
    # 按类型过滤
    response_type = client.get(f"/api/v1/dining-areas/?area_type={AreaType.TABLE.name}",
                               headers=admin_header)
    assert response_type.status_code == HTTPStatus.OK
    assert all(item['area_type'] == AreaType.TABLE.name for item in response_type.json["data"])

    # 按状态过滤 (假设 sample_dining_area 是 FREE)
    response_state = client.get(f"/api/v1/dining-areas/?state={DiningAreaState.FREE.name}",
                                headers=admin_header)
    assert response_state.status_code == HTTPStatus.OK
    assert all(item['state'] == DiningAreaState.FREE.name for item in response_state.json["data"])
    found = any(
        item['area_id'] == sample_dining_area.area_id for item in response_state.json["data"])
    assert found, "Sample dining area not found in filtered list"

    # 无效过滤参数
    response_invalid = client.get("/api/v1/dining-areas/?area_type=INVALID", headers=admin_header)
    assert response_invalid.status_code == HTTPStatus.BAD_REQUEST


def test_get_dining_area_detail(client, admin_header, sample_dining_area):
    """Test getting details of a specific dining area."""
    area_id = sample_dining_area.area_id
    response = client.get(f"/api/v1/dining-areas/{area_id}",
                          headers=admin_header)  # 使用新路径 GET /api/v1/dining-areas/{id}

    assert response.status_code == HTTPStatus.OK
    assert response.json["status"] == "success"
    data = response.json["data"]
    assert data["area_id"] == area_id
    assert data["area_name"] == sample_dining_area.area_name


def test_get_nonexistent_dining_area(client, admin_header):
    """Test getting details of a non-existent dining area."""
    nonexistent_id = 99999
    response = client.get(f"/api/v1/dining-areas/{nonexistent_id}", headers=admin_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_dining_area(client, admin_header, sample_dining_area):
    """Test updating a dining area successfully."""
    area_id = sample_dining_area.area_id
    unique_name = f"更新后的区域_{uuid.uuid4().hex[:8]}"
    payload = {
        "area_name": unique_name,
        "max_capacity": 15,
        "area_type": AreaType.PRIVATE.name
    }
    response = client.put(f"/api/v1/dining-areas/{area_id}", json=payload,
                          headers=admin_header)  # 使用新路径 PUT /api/v1/dining-areas/{id}

    logger.debug(f"Update response status: {response.status_code}, json: {response.json}")
    assert response.status_code == HTTPStatus.OK
    assert response.json["status"] == "success"
    data = response.json["data"]
    assert data["area_id"] == area_id
    assert data["area_name"] == unique_name
    assert data["max_capacity"] == 15
    assert data["area_type"] == AreaType.PRIVATE.name

    # 验证数据库中的值是否真的改变了 (可选，但更可靠)
    # get_res = client.get(f"/api/v1/dining-areas/{area_id}", headers=admin_header)
    # assert get_res.json["data"]["area_name"] == unique_name


def test_update_dining_area_name_conflict(client, admin_header, db_session):
    """Test updating a dining area name to an existing name."""
    # 创建两个区域
    area1 = DiningArea(area_name="区域A", max_capacity=2, area_type=AreaType.TABLE)
    area2 = DiningArea(area_name="区域B", max_capacity=4, area_type=AreaType.TABLE)
    db_session.add_all([area1, area2])
    db_session.commit()
    area1_id = area1.area_id
    area2_name = area2.area_name

    # 尝试将区域 A 的名称更新为区域 B 的名称
    payload = {"area_name": area2_name}
    response = client.put(f"/api/v1/dining-areas/{area1_id}", json=payload, headers=admin_header)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # 或者 CONFLICT (取决于服务层 BusinessError)
    assert response.json["status"] == "fail"
    assert "Dining area name already exists." in response.json["message"]


def test_update_nonexistent_dining_area(client, admin_header):
    """Test updating a non-existent dining area."""
    nonexistent_id = 99999
    payload = {"area_name": "不存在的更新"}
    response = client.put(f"/api/v1/dining-areas/{nonexistent_id}", json=payload, headers=admin_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_assign_and_release_dining_area(client, admin_header, db_session, test_user):
    """Test assigning and then releasing a dining area."""
    # 1. 创建一个空闲区域
    area = DiningArea(area_name=f"待分配区域_{uuid.uuid4().hex[:8]}", max_capacity=2,
                      area_type=AreaType.TABLE)
    db_session.add(area)
    db_session.commit()
    area_id = area.area_id

    # 2. 分配区域
    assign_payload = {"user_id": test_user.user_id}
    assign_res = client.post(f"/api/v1/dining-areas/{area_id}/assign", json=assign_payload,
                             headers=admin_header)  # 使用新路径 POST /api/v1/dining-areas/{id}/assign

    logger.debug(f"Assign response: {assign_res.json}")
    assert assign_res.status_code == HTTPStatus.OK
    assert assign_res.json["status"] == "success"
    assign_data = assign_res.json["data"]
    assert assign_data["area_id"] == area_id
    assert assign_data["state"] == DiningAreaState.OCCUPIED.name
    assert assign_data["assigned_user_id"] == test_user.user_id
    assert assign_data["usage_count"] == 1  # 使用次数增加
    assert assign_data["last_used"] is not None

    # 3. 尝试再次分配已被占用的区域 (应失败)
    assign_again_res = client.post(f"/api/v1/dining-areas/{area_id}/assign", json=assign_payload,
                                   headers=admin_header)
    assert assign_again_res.status_code == HTTPStatus.BAD_REQUEST  # 或 CONFLICT
    assert "Area is already occupied" in assign_again_res.json["message"]

    # 4. 释放区域
    release_res = client.post(f"/api/v1/dining-areas/{area_id}/release",
                              headers=admin_header)  # 使用新路径 POST /api/v1/dining-areas/{id}/release (不需要请求体)

    logger.debug(f"Release response: {release_res.json}")
    assert release_res.status_code == HTTPStatus.OK
    assert release_res.json["status"] == "success"
    release_data = release_res.json["data"]
    assert release_data["area_id"] == area_id
    assert release_data["state"] == DiningAreaState.FREE.name
    assert release_data["assigned_user_id"] is None
    # usage_count 和 last_used 在释放时是否更新取决于业务逻辑，当前服务层实现是不更新

    # 5. 尝试再次释放已经是空闲的区域 (应成功或返回当前状态)
    release_again_res = client.post(f"/api/v1/dining-areas/{area_id}/release", headers=admin_header)
    assert release_again_res.status_code == HTTPStatus.OK  # 服务层做了幂等处理
    assert release_again_res.json["data"]["state"] == DiningAreaState.FREE.name


def test_assign_area_to_nonexistent_user(client, admin_header, sample_dining_area):
    """Test assigning area to a non-existent user."""
    area_id = sample_dining_area.area_id
    nonexistent_user_id = 99999
    assign_payload = {"user_id": nonexistent_user_id}
    assign_res = client.post(f"/api/v1/dining-areas/{area_id}/assign", json=assign_payload,
                             headers=admin_header)
    assert assign_res.status_code == HTTPStatus.NOT_FOUND  # 服务层应抛 NotFoundError
    assert "User not found" in assign_res.json["message"]


def test_delete_dining_area_success(client, admin_header, db_session):
    """Test deleting a dining area successfully."""
    # 创建一个用于删除的区域
    area_to_delete = DiningArea(area_name=f"待删除区域_{uuid.uuid4().hex[:8]}", max_capacity=1,
                                area_type=AreaType.BAR)
    db_session.add(area_to_delete)
    db_session.commit()
    area_id = area_to_delete.area_id

    # 执行删除
    delete_res = client.delete(f"/api/v1/dining-areas/{area_id}",
                               headers=admin_header)  # 使用新路径 DELETE /api/v1/dining-areas/{id}
    assert delete_res.status_code == HTTPStatus.NO_CONTENT

    # 验证是否真的删除了
    get_res = client.get(f"/api/v1/dining-areas/{area_id}", headers=admin_header)
    assert get_res.status_code == HTTPStatus.NOT_FOUND


def test_delete_occupied_dining_area(client, admin_header, db_session, test_user):
    """Test deleting an occupied dining area (should fail)."""
    # 创建并分配一个区域
    area = DiningArea(area_name=f"占用待删除_{uuid.uuid4().hex[:8]}", max_capacity=2,
                      area_type=AreaType.TABLE)
    db_session.add(area)
    db_session.commit()
    area_id = area.area_id
    assign_payload = {"user_id": test_user.user_id}
    client.post(f"/api/v1/dining-areas/{area_id}/assign", json=assign_payload, headers=admin_header)  # 分配

    # 尝试删除
    delete_res = client.delete(f"/api/v1/dining-areas/{area_id}", headers=admin_header)
    assert delete_res.status_code == HTTPStatus.BAD_REQUEST  # 或 CONFLICT
    assert "Dining area is currently occupied and cannot be deleted." in delete_res.json["message"]


def test_delete_nonexistent_dining_area(client, admin_header):
    """Test deleting a non-existent dining area."""
    nonexistent_id = 99999
    delete_res = client.delete(f"/api/v1/dining-areas/{nonexistent_id}", headers=admin_header)  # 使用新路径
    assert delete_res.status_code == HTTPStatus.NOT_FOUND  # 服务层应抛 NotFoundError
