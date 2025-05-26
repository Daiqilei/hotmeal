# -*- coding: utf-8 -*-
"""
@File       : test_auth.py
@Date       : 2025-03-01
@Desc       : 测试用户登录和权限验证


"""


def test_login_success(client,test_user):
    """
    测试登录成功：使用正确的用户名和密码，期望返回200并包含token字段
    """
    payload = {
        "account": "testuser",
        "password": "password"
    }

    response = client.post("/api/v1/users/login", json=payload)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    json_data = response.get_json()
    assert "data" in json_data
    json_data = json_data["data"]
    assert "token" in json_data, "Token not found in response data"


def test_login_failure(client):
    """
    测试登录失败：使用错误的用户名或密码，期望返回 401 状态码
    """
    payload = {
        "account": "wronguser",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"
    json_data = response.get_json(force=True)
    assert isinstance(json_data, dict), f"Invalid JSON response: {json_data}"
    assert "message" in json_data or "error" in json_data, f"No error or message in response: {json_data}"
    assert json_data.get("message", json_data.get("error")) == "User not found"


def test_login_wrong_password(client,test_user):
    """
    测试登录失败：用户名正确但密码错误，应返回401
    """
    payload = {"account": "testuser", "password": "wrongpassword"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"
    json_data = response.get_json(force=True)
    assert isinstance(json_data, dict), f"Invalid JSON response: {json_data}"
    assert "message" in json_data or "error" in json_data, f"No error or message in response: {json_data}"
    assert json_data.get("message", json_data.get("error")) == "Invalid password"


def test_login_missing_account(client):
    """
    测试登录失败：缺少用户名字段，应返回400或422
    """
    payload = {"password": "password"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code in (400, 422)


def test_require_roles_success(client,admin_user):
    """
    测试权限验证成功：模拟一个具有管理员权限的用户访问需要admin权限的接口
    注意：这里假设你有一个 '/api/v1/admin/admin' 路由，用于测试权限验证，并返回 "Access granted"
    """
    login_resp = client.post("/api/v1/users/login", json={"account": "admin", "password": "admin123"})
    assert login_resp.status_code == 200, f"Admin login failed, got {login_resp.status_code}"
    token = login_resp.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/admin/admin", headers=headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    body, code = response.get_json(), response.status_code
    assert isinstance(body, dict), "Response should be a dict"
    assert code == 200
    assert body.get("status") == "success"
    assert body.get("error_code") == 0
    assert body.get("data") == "Access granted"
    assert body.get("message") == "Operation succeeded"


def test_require_roles_failure(client,test_user):
    """
    测试权限验证失败：模拟一个普通用户访问需要管理员权限的接口，应返回 403 状态码
    """
    login_resp = client.post("/api/v1/users/login", json={"account": "testuser", "password": "password"})
    assert login_resp.status_code == 200, f"User login failed, got {login_resp.status_code}"
    token = login_resp.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/admin/admin", headers=headers)
    assert response.status_code == 403, f"Expected 403 but got {response.status_code}"
    json_data = response.get_json()
    assert "message" in json_data or "error" in json_data, "No error or message in response"
    assert json_data.get("message", json_data.get("error")) == "Permission denied"


def test_invalid_token(client):
    """
    测试权限验证失败：使用非法Token访问应返回401
    """
    headers = {"Authorization": "Bearer invalid.token.value"}
    response = client.get("/api/v1/admin/admin", headers=headers)
    assert response.status_code in (401, 422)
