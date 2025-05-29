# -*- coding: utf-8 -*-
"""
@File       : conftest.py
@Date       : 2025-03-01 (Refactored: 2025-03-01)
@Description: Pytest 共享夹具文件。提供 Flask 测试客户端、应用上下文以及隔离测试所需的用户/令牌设置。
@Project    : HotMeal - Personalized Meal Ordering System Based on Recommendation Algorithms
"""

import pytest
import logging

from decimal import Decimal
from uuid import uuid4
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token

# 导入 Flask app 工厂函数和 db 实例
from app import create_app
# 导入所有需要创建或查询的模型
from app.models import User, Category, Dish, DiningArea, Order, OrderItem
from app.models.enums import UserRole, AreaType, OrderState
from app.utils.db import db


@pytest.fixture(scope="function")
def mock_recommend_dishes(db_session):
    """
    创建一批用于推荐系统测试的真实菜品数据，覆盖常见中餐分类和销量层级。
    共 15 道菜，涵盖川菜、粤菜、家常菜，适用于 itemCF、popular、profile 等推荐策略。
    """
    now = datetime.utcnow()

    test_data = [
        ("川菜", [
            ("宫保鸡丁", 120), ("水煮鱼", 90), ("辣子鸡", 60), ("麻婆豆腐", 55), ("回锅肉", 110)
        ]),
        ("粤菜", [
            ("清蒸鲈鱼", 80), ("粤式烧鸭", 100)
        ]),
        ("家常菜", [
            ("鱼香肉丝", 70), ("干煸四季豆", 50), ("酸辣土豆丝", 65), ("醋溜白菜", 45),
            ("虾仁炒蛋", 35), ("番茄炒蛋", 150)
        ]),
        ("淮扬菜", [
            ("红烧狮子头", 30)
        ])
    ]

    dishes = []
    chuancai_category = None
    for category_name, dish_list in test_data:
        if category_name == "川菜":
            category = Category(name="川菜")  # 不加 uuid，便于画像匹配
            chuancai_category = category
        else:
            category = Category(name=f"{category_name}_{uuid4().hex[:4]}")
        db_session.add(category)
        db_session.flush()

        for index, (dish_name, sales) in enumerate(dish_list):
            dish = Dish(
                name=f"{dish_name}",
                price=Decimal("18.0") + index,
                stock=100,
                category_id=category.category_id,
                description="推荐系统测试菜",
                image_url=f"http://example.com/img/{uuid4().hex[:6]}.jpg",
                is_available=True,
                sales=sales,
                rating=4.0 + (index % 2) * 0.3,
                created_at=now - timedelta(days=index * 2),
            )
            db_session.add(dish)
            dishes.append(dish)

    # 明确添加一个额外川菜用于推荐测试
    if chuancai_category is None:
        chuancai_category = Category(name="川菜")
        db_session.add(chuancai_category)
        db_session.flush()

    extra_dish = Dish(
        name="测试川菜推荐菜",
        price=Decimal("26.0"),
        stock=50,
        category_id=chuancai_category.category_id,
        description="专用于画像推荐测试",
        image_url="http://example.com/img/chuancai_test.jpg",
        is_available=True,
        sales=80,
        rating=4.5,
        created_at=now - timedelta(days=5)
    )
    db_session.add(extra_dish)
    dishes.append(extra_dish)

    db_session.commit()
    for d in dishes:
        db_session.refresh(d)

    return dishes


# ====================【ItemCF 推荐测试专用夹具】======================================================

@pytest.fixture(scope="function")
def mock_user_with_orders(db_session, mock_recommend_dishes):
    """
    创建一个用户和他的历史订单行为，用于测试 ItemCF 协同过滤推荐。
    默认点过 mock_recommend_dishes 中销量前 3 的菜品。
    """
    from app.models.order import Order
    from app.models.order_item import OrderItem
    from app.models.enums import OrderState

    # 创建用户
    test_user = User(
        account=f"user_cf_{uuid4().hex[:6]}",
        username="协同用户",
        role=UserRole.USER
    )
    test_user.set_password("test123")
    db_session.add(test_user)
    db_session.flush()

    # 获取销量前 3 的菜品
    sorted_dishes = sorted(mock_recommend_dishes, key=lambda d: d.sales, reverse=True)[:3]
    orders = []
    for dish in sorted_dishes:
        order = Order(
            user_id=test_user.user_id,
            price=dish.price,
            state=OrderState.COMPLETED
        )
        db_session.add(order)
        db_session.flush()

        item = OrderItem(
            order_id=order.order_id,
            dish_id=dish.dish_id,
            quantity=1,
            unit_price=dish.price
        )
        db_session.add(item)
        orders.append(order)

    # 创建两个额外用户，用于 item_cf 协同过滤构造邻居关系
    alice = User(account=f"alice_{uuid4().hex[:6]}", username="Alice", role=UserRole.USER)
    bob = User(account=f"bob_{uuid4().hex[:6]}", username="Bob", role=UserRole.USER)
    alice.set_password("alice123")
    bob.set_password("bob123")
    db_session.add_all([alice, bob])
    db_session.flush()

    # Alice 点过与 test_user 相同的 2 个菜（作为邻居）
    for dish in sorted_dishes[:2]:
        order = Order(user_id=alice.user_id, price=dish.price, state=OrderState.COMPLETED)
        db_session.add(order)
        db_session.flush()
        item = OrderItem(order_id=order.order_id, dish_id=dish.dish_id, quantity=1, unit_price=dish.price)
        db_session.add(item)

    # Bob 点过前两个菜 + 另外两个不同的菜，便于推荐
    extra_dishes = mock_recommend_dishes[3:5]
    for dish in sorted_dishes[:2] + extra_dishes:
        order = Order(user_id=bob.user_id, price=dish.price, state=OrderState.COMPLETED)
        db_session.add(order)
        db_session.flush()
        item = OrderItem(order_id=order.order_id, dish_id=dish.dish_id, quantity=1, unit_price=dish.price)
        db_session.add(item)

    db_session.commit()
    return {
        "user": test_user,
        "dishes": sorted_dishes,
        "orders": orders,
        "alice": alice,
        "bob": bob
    }


# ====================【Profile-Based 推荐测试专用夹具】======================================================

@pytest.fixture(scope="function")
def mock_user_with_profile(db_session):
    """
    创建一个设定偏好为 '川菜' 的测试用户，用于 profile-based 推荐算法测试。
    """
    test_user = User(
        account=f"user_profile_{uuid4().hex[:6]}",
        username="画像用户",
        role=UserRole.USER,
        favorite_cuisine="川菜"
    )
    test_user.set_password("test123")
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    return test_user


def get_or_create_user(session, **kwargs):
    """
    get_or_create_user 是一个辅助函数，用于在测试中创建或获取用户。
    它接受一个 session 对象，以及一组可选参数，用于创建或查找用户。
    如果用户已存在，则返回该用户对象；否则，创建新用户并返回。
    """
    account = kwargs.get("account")
    instance = session.query(User).filter_by(account=account).first()
    if instance:
        return instance
    instance = User(**kwargs)
    session.add(instance)
    return instance


# 配置日志（测试期间可以简化或重定向）
# logging.basicConfig(level=logging.INFO) # 可以移到 pytest 配置或保持简单
logger = logging.getLogger("test")  # 使用专门的测试 logger 名称


# ====================【核心应用 & 数据库基础设施】=====================================================
@pytest.fixture(scope='session')  # 改为 session 作用域以提高效率
def app():
    """
    创建并配置一个用于测试的 Flask 应用实例。
    在整个测试会话期间只创建一次。
    """
    # 确保加载了环境变量，特别是测试数据库配置等（如果需要）
    # from dotenv import load_dotenv
    # load_dotenv() # 如果 TestConfig 不直接读取 os.getenv

    flask_app = create_app('testing')  # 使用 'testing' 配置

    # 配置更新（可以覆盖或补充 TestConfig）
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": False,  # 测试时通常关闭 DEBUG
        # 推荐使用内存数据库进行快速测试
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        # "SQLALCHEMY_DATABASE_URI": "sqlite:///test_temp.db", # 或者临时文件数据库
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": flask_app.config.get('SECRET_KEY', 'testing-secret-key'),
        "JWT_SECRET_KEY": flask_app.config.get('JWT_SECRET_KEY',
                                               flask_app.config.get
                                               ('SECRET_KEY', 'testing-secret-key')),
        "SQLALCHEMY_ECHO": False,  # 测试时通常关闭 SQL Echo
    })

    # 配置测试日志
    # handler = logging.StreamHandler() # 输出到控制台
    # handler.setLevel(logging.DEBUG) # 设置测试期间的日志级别
    # flask_app.logger.addHandler(handler)
    # flask_app.logger.setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)  # 减少 SQLAlchemy 日志噪音

    with flask_app.app_context():
        logger.info("Setting up database for test session...")
        db.create_all()  # 创建所有表

    yield flask_app  # 提供 app 实例给测试

    # 清理 (测试会话结束后)
    with flask_app.app_context():
        logger.info("Tearing down database after test session...")
        db.session.remove()  # 移除 session
        db.drop_all()  # 删除所有表

    # 如果使用的是文件数据库，在这里删除文件
    # if flask_app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///test_temp.db":
    #     if os.path.exists("test_temp.db"):
    #         os.remove("test_temp.db")


@pytest.fixture(scope='function')
def db_session(app):
    """
    提供一个数据库 session，并在测试函数结束后回滚事务，清理数据。
    """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        from sqlalchemy.orm import sessionmaker
        session_factory = sessionmaker(bind=connection)
        session = session_factory()

        try:
            yield session
        finally:
            transaction.rollback()
            connection.close()
            session.close()


@pytest.fixture(scope='function')
def client(app):
    """提供一个 Flask 测试客户端。"""
    return app.test_client()


# ====================【用户夹具】====================================================================

@pytest.fixture(scope='function')  # function 作用域确保每次测试用户都是干净创建的
def test_users(db_session):  # 依赖 db_session 夹具
    """创建一组标准的测试用户并返回用户对象字典。"""
    users = {}
    try:
        admin = get_or_create_user(db_session, account="admin", role=UserRole.ADMIN)
        admin.set_password("admin123")
        users['admin'] = admin

        staff = get_or_create_user(db_session, account="staff", role=UserRole.STAFF)
        staff.set_password("staff123")
        users['staff'] = staff

        user = get_or_create_user(db_session, account="testuser", username="testuser",
                                  role=UserRole.USER)
        user.set_password("password")
        users['user'] = user

        db_session.commit()  # 提交用户创建

        for user_obj in users.values():
            db_session.refresh(user_obj)
            logger.debug(
                f"Created test user: {user_obj.account} (ID: {user_obj.user_id}, Role: {user_obj.role.name})")

        return users
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to create test users: {e}", exc_info=True)
        pytest.fail(f"Failed to set up test users: {e}")


# 单独获取用户的夹具
@pytest.fixture(scope='function')
def admin_user(test_users):
    """
    admin 用户对象。
    """
    return test_users['admin']


@pytest.fixture(scope='function')
def staff_user(test_users):
    """
    staff 用户对象。
    """
    return test_users['staff']


@pytest.fixture(scope='function')
def test_user(test_users):
    return test_users['user']


# ====================【Token / Header 认证夹具】=====================================================


def _generate_test_token(user: User) -> str:
    """使用 Flask-JWT-Extended 生成测试令牌"""
    if not user or not user.user_id:
        raise ValueError("Invalid user object provided for token generation.")
    identity = str(user.user_id)
    additional_claims = {"role": user.role.value}
    # 注意：create_access_token 需要在 app 上下文中调用
    # 但如果夹具依赖 app，它会自动处理上下文
    token = create_access_token(identity=identity, additional_claims=additional_claims)
    logger.debug(f"Generated token for user {user.account}")
    return token


@pytest.fixture(scope='function')
def admin_token(app, admin_user):  # 需要 app 上下文
    """为 admin 用户生成 JWT 令牌。"""
    with app.app_context():  # 确保在 app 上下文中生成 token
        return _generate_test_token(admin_user)


@pytest.fixture(scope='function')
def staff_token(app, staff_user):
    """为 staff 用户生成 JWT 令牌。"""
    with app.app_context():
        return _generate_test_token(staff_user)


@pytest.fixture(scope='function')
def user_token(app, test_user):
    """为 testuser 用户生成 JWT 令牌。"""
    with app.app_context():
        return _generate_test_token(test_user)


# Header Fixtures
@pytest.fixture(scope='function')
def admin_header(admin_token):
    """为 admin 用户创建认证请求头。"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope='function')
def staff_header(staff_token):
    """为 staff 用户创建认证请求头。"""
    return {"Authorization": f"Bearer {staff_token}"}


@pytest.fixture(scope='function')
def user_header(user_token):
    """为 testuser 用户创建认证请求头。"""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture(scope='function')
def invalid_auth_header():
    """创建一个无效的认证请求头。"""
    return {"Authorization": "Bearer invalid-or-expired-token"}


# ====================【Profile 用户 Token 夹具】=====================================================

@pytest.fixture(scope='function')
def profile_user_token(app, mock_user_with_profile):
    """为画像用户生成 JWT 令牌，用于 profile_based 和默认策略测试。"""
    with app.app_context():
        return _generate_test_token(mock_user_with_profile)


# ====================【模型示例数据夹具】=============================================================


@pytest.fixture
def preset_categories(db_session):
    """生成两个随机分类用于测试，避免唯一键冲突"""
    name1 = f"测试分类_{uuid4().hex}"
    name2 = f"测试分类_{uuid4().hex}"
    category1 = Category(name=name1, description="第一个测试分类")
    category2 = Category(name=name2, description="第二个测试分类")
    db_session.add_all([category1, category2])
    db_session.commit()
    return [category1, category2]


@pytest.fixture(scope='function')
def ensure_category(db_session):
    """创建一个确保可用的分类对象，避免名称重复和事务冲突。"""
    try:
        name = f"测试分类_{uuid4().hex[:6]}"
        category = Category(name=name, description="用于 ensure_category 测试夹具")
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        logger.debug(f"Created ensure_category: {category.name} (ID: {category.category_id})")
        return category
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to create ensure_category: {e}", exc_info=True)
        pytest.fail(f"Failed to set up ensure_category: {e}")


@pytest.fixture(scope='function')
def sample_category(db_session):  # 依赖 db_session
    """创建一个示例分类并返回 Category 对象。"""
    try:
        name = f"测试分类_{uuid4().hex[:6]}"
        category = Category(name=name)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        logger.debug(f"Created sample category: {category.name} (ID: {category.category_id})")
        return category
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to create sample category: {e}", exc_info=True)
        pytest.fail(f"Failed to set up sample category: {e}")


@pytest.fixture(scope='function')
def sample_dish(db_session, sample_category):  # 依赖 db_session 和 sample_category
    """创建一个示例菜品并返回 Dish 对象。"""
    try:
        unique_name = f"测试菜品_{uuid4().hex[:6]}"
        dish = Dish(
            name=unique_name,
            price=Decimal("19.99"),
            stock=100,
            category_id=sample_category.category_id,
            description="这是一个测试菜品描述",
            image_url="http://example.com/sample_dish.jpg",
            is_available=True,
            rating=4.5
        )
        db_session.add(dish)
        db_session.commit()
        db_session.refresh(dish)
        logger.debug(f"Created sample dish: {dish.name} (ID: {dish.dish_id})")
        return dish
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to create sample dish: {e}", exc_info=True)
        pytest.fail(f"Failed to set up sample dish: {e}")


@pytest.fixture(scope='function')
def sample_dining_area(db_session):  # 依赖 db_session
    """创建一个示例用餐区域并返回 DiningArea 对象。"""
    try:
        area_name = f"测试区域_{uuid4().hex[:6]}"
        area = DiningArea(
            area_name=area_name,
            max_capacity=4,
            area_type=AreaType.TABLE
        )
        db_session.add(area)
        db_session.commit()
        db_session.refresh(area)
        logger.debug(f"Created sample dining area: {area.area_name} (ID: {area.area_id})")
        return area
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to create sample dining area: {e}", exc_info=True)
        pytest.fail(f"Failed to set up sample dining area: {e}")


# ====================【订单工厂夹具】=================================================================

@pytest.fixture(scope='function')
def create_test_order(db_session, test_user, sample_dish, sample_dining_area):  # 依赖多个夹具
    """
    提供一个工厂函数来创建测试订单。
    用法: order_id = create_test_order(quantity=2, state=OrderState.PAID)
    """
    created_orders = []  # 跟踪创建的订单 ID，以便清理（如果需要跨测试函数）

    def _factory(quantity=1, state=OrderState.PENDING) -> int:
        """创建订单和订单项的内部函数。"""
        try:
            # 确保依赖的对象有效
            if not all([test_user, sample_dish, sample_dining_area]):
                pytest.fail("Missing dependencies for create_test_order factory.")

            order = Order(
                user_id=test_user.user_id,
                area_id=sample_dining_area.area_id,
                state=state,
                price=Decimal(str(sample_dish.price)) * quantity  # 预计算价格
            )
            db_session.add(order)
            # 需要先 flush 获取 order.order_id
            db_session.flush()

            order_item = OrderItem(
                order_id=order.order_id,
                dish_id=sample_dish.dish_id,
                quantity=quantity,
                unit_price=sample_dish.price  # 使用 Decimal
            )
            db_session.add(order_item)
            db_session.commit()  # 提交订单和订单项
            db_session.refresh(order)  # 刷新订单以获取最终状态

            logger.debug(
                f"Created test order (ID: {order.order_id}) with {quantity}x '{sample_dish.name}'")
            created_orders.append(order.order_id)

            assert order.order_id is not None
            return order.order_id

        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to create test order in factory: {e}", exc_info=True)
            pytest.fail(f"Failed to create test order: {e}")

    yield _factory  # 提供工厂函数


@pytest.fixture(scope='function')
def recommendation_test_data(db_session, test_user):
    """为推荐测试准备一份完整的历史数据：分类 + 菜品 + 订单 + 订单项"""
    from app.models.enums import OrderState

    # 创建分类
    category = Category(
        name=f"推荐分类_{uuid4().hex[:6]}",
        description="推荐系统测试用分类"
    )
    db_session.add(category)
    db_session.flush()

    # 创建菜品
    dish = Dish(
        name=f"推荐菜品_{uuid4().hex[:6]}",
        price=Decimal("28.00"),
        stock=100,
        category_id=category.category_id,
        description="测试用推荐菜品",
        image_url="http://example.com/recommend_dish.jpg",
        is_available=True,
        rating=4.8
    )
    db_session.add(dish)
    db_session.flush()

    # 创建订单
    order = Order(
        user_id=test_user.user_id,
        state=OrderState.COMPLETED,
        price=dish.price
    )
    db_session.add(order)
    db_session.flush()

    # 创建订单项
    item = OrderItem(
        order_id=order.order_id,
        dish_id=dish.dish_id,
        quantity=1,
        unit_price=dish.price
    )
    db_session.add(item)
    db_session.commit()

    return {
        "category": category,
        "dish": dish,
        "order": order,
        "item": item
    }
