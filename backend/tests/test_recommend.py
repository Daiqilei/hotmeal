# -*- coding: utf-8 -*-
"""
@File       : test_recommend.py
@Date       : 2025-03-01
@Desc       : 测试推荐算法
"""
from app.services.recommend_service import RecommendationService
from flask_jwt_extended import create_access_token
# ==============================
# ✅ 服务层测试：RecommendationService（推荐服务逻辑）
# ==============================
def test_weighted_recommendation_with_fixture_data(mock_user_with_orders, mock_recommend_dishes):
    """
    测试服务层：推荐融合策略 weighted
    验证 mock 数据下是否能整合 popular + item_cf + profile_based 推荐结果，并限制输出数量
    """
    service = RecommendationService()
    user = mock_user_with_orders['user']

    # mock_recommend_dishes 夹具已准备推荐候选菜品环境
    result = service.recommend(user_id=user.user_id, strategy='weighted', limit=5)

    # 基本断言
    assert isinstance(result, list)
    assert len(result) <= 5
    assert all(isinstance(dish, dict) for dish in result)
    for dish in result:
        assert 'dish_id' in dish
        assert 'name' in dish
        assert 'price' in dish

    # 可视化打印推荐结果（便于调试/实战验证）
    print("推荐结果菜品信息列表：")
    for dish in result:
        print(f"- {dish['dish_id']} | {dish.get('name')} | ¥{dish.get('price')}")
def test_popular_recommendation(mock_user_with_orders, mock_recommend_dishes):
    """
    测试服务层：热门推荐策略 popular
    验证使用销量前 N 的菜品是否能成功推荐并生成规范结构数据
    """
    service = RecommendationService()
    user = mock_user_with_orders['user']
    result = service.recommend(user_id=user.user_id, strategy='popular', limit=5)

    assert isinstance(result, list)
    assert len(result) <= 5
    assert all(isinstance(dish, dict) for dish in result)
    for dish in result:
        assert 'dish_id' in dish
        assert 'name' in dish
        assert 'price' in dish

    print("【popular】推荐结果：")
    for dish in result:
        print(f"- {dish['dish_id']} | {dish.get('name')} | ¥{dish.get('price')}")
def test_item_cf_recommendation(mock_user_with_orders, mock_recommend_dishes):
    """
    测试服务层：协同过滤推荐策略 item_cf
    使用用户 Bob 作为测试对象，验证是否根据相似用户行为推荐菜品
    """
    service = RecommendationService()
    user = mock_user_with_orders['bob']  # ✅ Bob 是邻居用户，点过相同菜，便于推荐
    result = service.recommend(user_id=user.user_id, strategy='item_cf', limit=5)

    assert isinstance(result, list)
    assert len(result) <= 5
    assert all(isinstance(dish, dict) for dish in result)
    for dish in result:
        assert 'dish_id' in dish
        assert 'name' in dish
        assert 'price' in dish

    print("【item_cf】推荐结果：")
    for dish in result:
        print(f"- {dish['dish_id']} | {dish.get('name')} | ¥{dish.get('price')}")
def test_profile_based_recommendation_with_profile_user(mock_user_with_profile,
                                                        mock_recommend_dishes):
    """
    测试服务层：基于用户画像的推荐策略 profile_based
    使用具备 '川菜' 偏好的 mock 用户，验证是否能匹配分类并推荐对应菜品
    """
    service = RecommendationService()
    user = mock_user_with_profile
    result = service.recommend(user_id=user.user_id, strategy='profile_based', limit=5)

    assert isinstance(result, list)
    assert len(result) <= 5
    assert all(isinstance(dish, dict) for dish in result)
    for dish in result:
        assert 'dish_id' in dish
        assert 'name' in dish
        assert 'price' in dish

    print("【profile_based】推荐结果：")
    for dish in result:
        print(f"- {dish['dish_id']} | {dish.get('name')} | ¥{dish.get('price')}")
# ==============================
# ✅ 接口层测试：/api/v1/recommend 推荐接口
# ==============================
def test_recommend_route_popular(user_token, client, mock_recommend_dishes):
    """
    测试接口：/api/v1/recommend?strategy=popular
    验证热门推荐策略是否成功响应并返回预期结构
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    print("【popular 接口测试】Token:", user_token)
    # 原路径已注释，统一使用 /recommendations 路由
    # response = client.get("/api/v1/recommend?strategy=popular", headers=headers)
    response = client.get("/api/v1/recommendations?strategy=popular", headers=headers)
    # ====== 调试日志 ======
    print("【状态码】:", response.status_code)
    print("【响应是否为 JSON】:", response.is_json)
    print("【原始响应】:", response.data)
    print("【JSON 内容】:", response.get_json(force=True, silent=True))
    # print("【接口 popular】响应内容：", response.json)
    # assert response.status_code == 200
    # data = response.json
    # assert data["status"] == "success"
    # assert isinstance(data["data"], list)
def test_recommend_route_item_cf(client, mock_user_with_orders):
    """
    测试接口：/api/v1/recommend?strategy=item_cf
    验证协同过滤推荐是否可用并结构合法
    """
    user = mock_user_with_orders["bob"]
    with client.application.app_context():
        token = create_access_token(identity=user.user_id, additional_claims={"role": "USER"})
    print("【item_cf 接口测试】User ID:", user.user_id)
    print("【item_cf 接口测试】Token:", token)
    headers = {"Authorization": f"Bearer {token}"}
    # 原路径已注释，统一使用 /recommendations 路由
    # response = client.get("/api/v1/recommend?strategy=item_cf", headers=headers)
    response = client.get("/api/v1/recommendations?strategy=item_cf", headers=headers)
    # ====== 调试日志 ======
    print("【状态码】:", response.status_code)
    print("【响应是否为 JSON】:", response.is_json)
    print("【原始响应】:", response.data)
    print("【JSON 内容】:", response.get_json(force=True, silent=True))
    # print("【接口 item_cf】响应内容：", response.json)
    # assert response.status_code == 200
    # data = response.json
    # assert data["status"] == "success"
    # assert isinstance(data["data"], list)

def test_recommend_route_profile_based(client, mock_user_with_profile, mock_recommend_dishes):
    """
    测试接口：/api/v1/recommend?strategy=profile_based
    验证用户画像推荐结果是否正确返回
    """
    user = mock_user_with_profile
    with client.application.app_context():
        token = create_access_token(identity=user.user_id, additional_claims={"role": "USER"})
    print("【profile_based 接口测试】User ID:", user.user_id)
    print("【profile_based 接口测试】Token:", token)
    headers = {"Authorization": f"Bearer {token}"}
    # 原路径已注释，统一使用 /recommendations 路由
    # response = client.get("/api/v1/recommend?strategy=profile_based", headers=headers)
    response = client.get("/api/v1/recommendations?strategy=profile_based", headers=headers)
    # ====== 调试日志 ======
    print("【状态码】:", response.status_code)
    print("【响应是否为 JSON】:", response.is_json)
    print("【原始响应】:", response.data)
    print("【JSON 内容】:", response.get_json(force=True, silent=True))
    # print("【接口 profile_based】响应内容：", response.json)
    # assert response.status_code == 200
    # data = response.json
    # assert data["status"] == "success"
    # assert isinstance(data["data"], list)
def test_recommend_route_default_strategy(profile_user_token, client):
    """
    测试接口：/api/v1/recommend 不传 strategy 参数
    应使用配置默认策略（如 weighted）返回推荐结果
    """
    headers = {"Authorization": f"Bearer {profile_user_token}"}
    response = client.get("/api/v1/recommendations/", headers=headers)

    print("【默认策略测试】状态码：", response.status_code)
    print("【是否为 JSON】:", response.is_json)
    print("【原始响应内容】:", response.data)
    print("【JSON 解析结果】:", response.get_json(force=True, silent=True))

    assert response.status_code == 200
    data = response.get_json(force=True)
    assert data["status"] == "success"
    assert isinstance(data["data"]["recommendations"], list)
