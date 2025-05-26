# -*- coding: utf-8 -*-
"""
@File       : test_users.py
@Date       : 2025-03-01
@Desc       :


"""


def test_register_success(client):
    user_data = {"account": "newuser", "password": "newpassword",
                 "role": "USER"}
    response = client.post("/api/v1/users/register", json=user_data)
    response_json = response.get_json()
    assert response.status_code == 201
    assert response_json["status"] == "success"
    assert response_json["message"] == "User created successfully"
    assert "data" in response_json
    assert "user_id" in response_json["data"]
    assert response_json["data"]["account"] == "newuser"


def test_register_duplicate_account(client, app, test_user):
    """测试注册失败：重复的用户名"""
    payload = {
        "account": "testuser",  # 与 test_user 一致
        "password": "password",  # 与 test_user 的密码一致
        "role": "USER"
    }
    response = client.post("/api/v1/users/register", json=payload)
    response_json = response.get_json()
    assert response.status_code == 409
    assert response_json["status"] == "fail"
    assert "Account already exists" in response_json["message"]


def test_register_missing_fields(client,test_user):
    """测试注册失败：缺少密码"""
    payload = {
        "account": "missingpassword"
        # 缺少 password
    }
    response = client.post("/api/v1/users/register", json=payload)
    assert response.status_code == 400
    assert "Input payload validation failed" in response.get_json()["message"]


def test_register_invalid_role(client):
    """测试注册失败：非法角色"""
    payload = {
        "account": "invalidrole",
        "password": "password",
        "role": "INVALID_ROLE"
    }
    response = client.post("/api/v1/users/register", json=payload)
    assert response.status_code == 400
    assert "Input payload validation failed" in response.get_json()["message"]


def test_login_success(client, test_user):
    """测试登录成功"""
    payload = {"account": "testuser", "password": "password"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.get_json()["data"]


def test_login_fail_user_not_found(client):
    """测试登录失败：用户不存在"""
    payload = {"account": "nonexistentuser", "password": "password"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 401
    assert "User not found" in response.get_json()["message"]


def test_login_fail_wrong_password(client, test_user):
    """测试登录失败：密码错误"""
    payload = {"account": "testuser", "password": "wrongpassword"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 401
    assert "Invalid password" in response.get_json()["message"]


def test_login_missing_fields(client):
    """测试登录失败：缺少必要字段"""
    payload = {"account": "missingpassword"}
    response = client.post("/api/v1/users/login", json=payload)
    assert response.status_code == 400
    assert "Input payload validation failed" in response.get_json()["message"]


def test_get_profile_with_valid_token(client, user_header, test_user):
    """测试获取个人资料：携带有效用户 token"""
    print(f"Test User Username (before request): {test_user.username}")  # 添加这行
    response = client.get("/api/v1/users/profile", headers=user_header)
    assert response.status_code == 200
    user_data = response.get_json()
    print("Response User Data:", user_data)
    assert user_data["data"]["user_id"] == test_user.user_id
    assert user_data["data"]["username"] == "testuser"
    assert user_data["data"]["email"] is None
    assert user_data["data"]["role"] == "USER"


def test_get_profile_with_invalid_token(client, invalid_auth_header):
    """测试获取个人资料：携带无效 token (假设你在 conftest.py 中定义了 invalid_auth_header)"""
    response = client.get("/api/v1/users/profile", headers=invalid_auth_header)
    assert response.status_code == 422
    resp_json = response.get_json()
    assert "invalid" in resp_json.get("msg", "").lower() or "segment" in resp_json.get("msg", "").lower()


def test_update_profile_with_valid_token(client, user_header, test_user, app):
    """测试更新个人资料：携带有效用户 token"""
    payload = {
        "username": "updateduser",
        "email": "updated@example.com",
        "phone_number": "+1234567890"
    }
    response = client.put("/api/v1/users/profile", json=payload,
                          headers=user_header)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Profile updated successfully"

    with app.app_context():
        from app.models import User
        updated_user = User.query.get(test_user.user_id)  # 使用 user_id
        assert updated_user.username == "updateduser"
        assert updated_user.email == "updated@example.com"
        assert updated_user.phone_number == "+1234567890"


def test_update_profile_with_invalid_email(client, user_header):
    """测试更新个人资料：携带有效用户 token，但邮箱格式无效"""
    payload = {
        "email": "invalid-email"
    }
    response = client.put("/api/v1/users/profile", json=payload,
                          headers=user_header)
    assert response.status_code == 400
    assert "Invalid email format" in response.get_json()["message"]


def test_update_profile_without_token(client):
    """测试更新个人资料：未携带 token"""
    payload = {
        "username": "updateduser"
    }
    response = client.put("/api/v1/users/profile", json=payload)
    assert response.status_code == 401
    assert "authorization" in response.get_json().get("msg", "").lower()


def test_get_user_by_id_with_admin_token(client, admin_header, test_user):
    """测试管理员通过 ID 获取用户信息：携带有效管理员 token"""
    response = client.get(f"/api/v1/users/{test_user.user_id}", headers=admin_header)

    assert response.status_code == 200

    user_data = response.get_json()
    assert user_data["data"]["user_id"] == test_user.user_id
    assert user_data["data"]["account"] == "testuser"


def test_get_user_by_id_with_user_token_forbidden(client, user_header,
                                                  test_user):
    """测试普通用户通过 ID 获取用户信息：携带普通用户 token，应该被拒绝"""
    response = client.get(f"/api/v1/users/{test_user.user_id}", headers=user_header)
    assert response.status_code == 403
    assert "Permission denied" in response.get_json()["message"]


def test_get_user_by_id_with_admin_token_not_found(client, admin_header):
    """测试管理员通过 ID 获取用户信息：ID 不存在"""
    response = client.get("/api/v1/users/99999", headers=admin_header)
    assert response.status_code == 404
    assert "User not found" in response.get_json()["message"]


def test_list_users_with_admin_token(client, admin_header):
    """测试管理员列出所有用户：携带有效管理员 token"""
    response = client.get("/api/v1/users/list", headers=admin_header)
    assert response.status_code == 200
    user_list = response.get_json()["data"]
    assert isinstance(user_list, list)
    assert len(user_list) >= 2
    assert "user_id" in user_list[0]
    assert "account" in user_list[0]


def test_list_users_with_user_token_forbidden(client, user_header):
    """测试普通用户列出所有用户：携带普通用户 token，应该被拒绝"""
    response = client.get("/api/v1/users/list", headers=user_header)
    assert response.status_code == 403
    assert "Permission denied" in response.get_json()["message"]


def test_list_users_without_token(client):
    """测试列出所有用户：未携带 token"""
    response = client.get("/api/v1/users/list")
    assert response.status_code == 401
    assert "authorization" in response.get_json().get("msg", "").lower()


def test_delete_user_with_admin_token(client, admin_header, test_user):
    """测试管理员删除用户：携带有效管理员 token"""
    response = client.delete(f"/api/v1/users/{test_user.user_id}", headers=admin_header)
    assert response.status_code == 204

    # 尝试获取被删除的用户，应该返回 404
    response_get = client.get(f"/api/v1/users/{test_user.user_id}",
                              headers=admin_header)
    assert response_get.status_code == 404


def test_delete_user_with_user_token_forbidden(client, user_header, test_user):
    """测试普通用户删除用户：携带普通用户 token，应该被拒绝"""
    response = client.delete(f"/api/v1/users/{test_user.user_id}", headers=user_header)
    assert response.status_code == 403
    assert "Permission denied" in response.get_json()["message"]


def test_delete_user_with_admin_token_not_found(client, admin_header):
    """测试管理员删除用户：ID 不存在"""
    response = client.delete("/api/v1/users/99999", headers=admin_header)
    assert response.status_code == 404
    assert "User not found" in response.get_json()["message"]
