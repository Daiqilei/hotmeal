# -*- coding: utf-8 -*-
"""
@File       : test_chat.py
@Date       : 2025-03-01
@Desc       : This is the initialization file of the tests directory.
"""

# 确保以下接口已在 chat_routes.py 中定义并在主入口注册到 Flask app：
# 1. POST /api/v1/chats/ask
# 2. GET /api/v1/chats/history/<user_id>
# 3. POST /api/v1/chats/<chat_id>/process

def test_ask_question(client, user_header):
    response = client.post("/api/v1/chats/ask", json={
        "user_id": 1,
        "question": "推荐一下今天的特色菜"
    }, headers=user_header)
    assert response.status_code == 201
    assert "chat_id" in response.json["data"]

def test_get_user_chat_history(client, user_header):
    response = client.get("/api/v1/chats/history/1", headers=user_header)
    assert response.status_code == 200
    assert isinstance(response.json["data"]["items"], list)

def test_get_chat_answer(client, admin_header):
    # 创建新的 chat 提问
    create_resp = client.post("/api/v1/chats/ask", json={
        "question": "帮我推荐一下今晚的晚餐"
    }, headers=admin_header)
    assert create_resp.status_code == 201
    chat_id = create_resp.json["data"]["chat_id"]

    # 立即发起处理请求
    response = client.post(f"/api/v1/chats/{chat_id}/process", headers=admin_header)
    assert response.status_code in (200, 202)

# 新增的测试用例

def test_empty_question(client, user_header):
    """
    测试空问题输入，检查接口是否返回错误信息
    """
    response = client.post("/api/v1/chats/ask", json={
        "user_id": 1,
        "question": ""
    }, headers=user_header)
    # 这里假设接口对于空问题会返回 400 错误
    assert response.status_code == 400
    assert "error" in response.json

def test_invalid_payload(client, user_header):
    """
    测试传入不完整的 payload，例如缺少 question 字段
    """
    response = client.post("/api/v1/chats/ask", json={
        "user_id": 1
    }, headers=user_header)
    # 这里假设接口会返回 400 错误，提示缺少字段
    assert response.status_code == 400
    assert "error" in response.json

def test_long_question(client, user_header):
    """
    测试长文本输入，检查模型能否稳定返回结果，并验证返回数据结构
    """
    long_question = "请详细描述一下今天的菜品特点和推荐理由。" * 50  # 构造一个较长的输入
    response = client.post("/api/v1/chats/ask", json={
        "user_id": 1,
        "question": long_question
    }, headers=user_header)
    # 假设长问题依然可以成功生成响应
    assert response.status_code == 201
    data = response.json["data"]
    assert "chat_id" in data
    # 可进一步检查返回文本是否为字符串
    assert isinstance(data.get("answer", ""), str)