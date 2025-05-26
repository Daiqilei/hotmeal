# -*- coding: utf-8 -*-
"""
@File       : dish_routes.py
@Date       : 2025-03-01 (Refactored: 2025-03-01)
@Desc       : 菜品相关的 API 端点。


"""

import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required  # 导入需要的功能
from flask_restx import Namespace, Resource, fields

# 导入重构后的服务层模块
from app.services import dish_service
# 导入装饰器和响应工具
from app.utils.decorators import require_roles, log_request, timing
from app.utils.response import success, created, no_content, bad_request  # 导入需要的响应函数

# 导入需要的错误码和异常 (供参考)

logger = logging.getLogger(__name__)

# --- Namespace 定义 ---
# 路径使用复数形式 'dishes'
dish_ns = Namespace('dishes', description='菜品管理操作', path='/dishes')

# --- 输入/输出模型 (用于 Swagger 文档) ---

# 创建菜品时的输入模型
dish_create_model = dish_ns.model('DishCreateInput', {
    'name': fields.String(required=True, description='菜品名称', min_length=1, max_length=50,
                          example='宫保鸡丁'),
    'price': fields.String(required=True, description='价格 (格式如 "19.99")', example='25.00'),
    # 使用 Price 类型或 String
    'stock': fields.Integer(required=True, description='库存数量 (非负整数)', min=0, example=100),
    'category_id': fields.Integer(required=True, description='所属分类 ID', example=1),
    'image_url': fields.String(description='图片链接 (URL)',
                               example='http://example.com/image.jpg'),
    'sales': fields.Integer(description='初始销量 (非负整数)', min=0, default=0, example=0),
    'rating': fields.Float(description='初始评分 (0.0-5.0)', min=0.0, max=5.0, default=0.0,
                           example=4.5),
    'description': fields.String(description='菜品描述', max_length=255,
                                 example='经典川菜，味道鲜美'),
    'is_available': fields.Boolean(description='是否上架', default=True, example=True),
    'tag_names': fields.List(fields.String, description='标签名称列表', example=['辣', '新品'])
})

# 更新菜品时的输入模型 (所有字段可选)
dish_update_model = dish_ns.model('DishUpdateInput', {
    'name': fields.String(description='新菜品名称', min_length=1, max_length=50,
                          example='新宫保鸡丁'),
    'price': fields.String(description='新价格 (格式如 "19.99")', example='28.50'),
    'stock': fields.Integer(description='新库存数量 (非负整数)', min=0, example=50),
    'category_id': fields.Integer(description='新所属分类 ID', example=2),
    'image_url': fields.String(description='新图片链接 (URL)',
                               example='http://example.com/new_image.jpg'),
    'sales': fields.Integer(description='新销量 (非负整数)', min=0, example=10),
    'rating': fields.Float(description='新评分 (0.0-5.0)', min=0.0, max=5.0, example=4.8),
    'description': fields.String(description='新菜品描述', max_length=255,
                                 example='改良版经典川菜'),
    'is_available': fields.Boolean(description='新上架状态', example=False),
    'tag_names': fields.List(fields.String, description='新标签名称列表', example=['微辣', '推荐'])
})

# 菜品信息的输出模型 (与 serialize_dish 对应)
dish_output_model = dish_ns.model('DishOutput', {
    'dish_id': fields.Integer(description='菜品 ID'),
    'name': fields.String(description='菜品名称'),
    # 输出时通常是字符串或浮点数
    'price': fields.String(description='价格'),  # 或者 fields.Float
    'stock': fields.Integer(description='库存数量'),
    'image_url': fields.String(description='图片链接'),
    'sales': fields.Integer(description='销量'),
    'rating': fields.Float(description='评分'),
    'description': fields.String(description='描述'),
    'category_id': fields.Integer(description='分类 ID'),
    'category_name': fields.String(description='分类名称'),  # 从 serialize_dish 添加
    'is_available': fields.Boolean(description='是否上架'),
    'created_at': fields.DateTime(description='创建时间 (ISO 格式)'),
    'updated_at': fields.DateTime(description='更新时间 (ISO 格式)'),
    # 'deleted_at': fields.DateTime(description='删除时间 (ISO 格式)', readonly=True, nullable=True) # 如果有软删除
})


# --- 路由 ---

@dish_ns.route("/")  # 对应 /dishes/
class DishList(Resource):

    @dish_ns.doc('create_dish', security='jsonWebToken')
    @dish_ns.expect(dish_create_model, validate=True)  # 使用 expect 进行输入验证
    @dish_ns.response(HTTPStatus.CREATED, '菜品创建成功', dish_output_model)
    @dish_ns.response(HTTPStatus.BAD_REQUEST, '输入参数无效')
    @dish_ns.response(HTTPStatus.UNAUTHORIZED, '需要认证')
    @dish_ns.response(HTTPStatus.FORBIDDEN, '需要管理员权限')
    @dish_ns.response(HTTPStatus.CONFLICT, '菜品名称已存在')
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '创建失败')
    @jwt_required()  # 需要登录
    @require_roles(["admin"])  # 仅管理员可创建
    @log_request
    @timing
    # 移除了 @validate_json
    def post(self):
        """创建新菜品 (仅管理员)"""
        data = request.get_json()
        print("📥 Received JSON:", data)

        # sales 和 rating 字段由后端管理，前端不可传入
        new_dish_data = dish_service.create_dish(
            name=data.get("name"),
            price=data.get("price"),  # 服务层会处理 Decimal 转换和验证
            stock=data.get("stock"),
            category_id=data.get("category_id"),
            image_url=data.get("image_url"),
            sales=0,  # 销量由后端初始化为0，前端不可传入
            rating=0.0,  # 评分由后端初始化为0.0，前端不可传入
            description=data.get("description"),
            is_available=data.get("is_available", True),
            tag_names=data.get("tag_names")
        )

        # 服务层成功返回字典数据
        logger.info(
            f"管理员创建菜品: ID={new_dish_data.get('dish_id')}, Name='{new_dish_data.get('name')}'")
        return created(data=new_dish_data, message="菜品创建成功")

    @dish_ns.doc('list_available_dishes')
    @dish_ns.param('category_id', '按分类 ID 过滤 (可选)', type=int, location='args')  # 添加查询参数文档
    @dish_ns.response(HTTPStatus.OK, '成功获取可用菜品列表', [dish_output_model])  # 返回列表
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '获取列表失败')
    @log_request
    @timing
    def get(self):
        """获取所有可用的菜品列表 (公开访问)"""
        # 从查询参数获取 category_id
        category_id_str = request.args.get('category_id')
        category_id = None
        if category_id_str:
            try:
                category_id = int(category_id_str)
            except ValueError:
                return bad_request("category_id 参数必须是整数。")  # 基本类型验证

        # 调用服务层函数
        available_dishes_data = dish_service.get_available_dishes(category_id=category_id)
        print("🧪 服务层返回的可用菜品数据预览:", available_dishes_data[:3])  # 打印前 3 项快速确认结构
        logger.info(f"获取可用菜品列表: {len(available_dishes_data)} 个。"
                    f"{' Category ID: ' + str(category_id) if category_id else ''}")
        return success(message="成功获取可用菜品列表", data=available_dishes_data)


@dish_ns.route("/<int:dish_id>")  # 对应 /dishes/{dish_id}
@dish_ns.param('dish_id', '菜品 ID')
class DishDetail(Resource):

    @dish_ns.doc('get_dish_detail')
    @dish_ns.response(HTTPStatus.OK, '成功获取菜品详情', dish_output_model)
    @dish_ns.response(HTTPStatus.NOT_FOUND, '菜品未找到')
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '获取详情失败')
    @log_request
    @timing
    def get(self, dish_id):
        """获取指定 ID 的菜品详情 (公开访问)"""
        # 服务层函数在未找到时抛出 NotFoundError
        dish_data = dish_service.get_dish_by_id(dish_id)

        logger.info(f"获取菜品详情: ID={dish_id}, Name='{dish_data.get('name')}'")
        return success(message="成功获取菜品详情", data=dish_data)

    @dish_ns.doc('update_dish', security='jsonWebToken')
    @dish_ns.expect(dish_update_model, validate=True)  # 使用 expect 进行输入验证
    @dish_ns.response(HTTPStatus.OK, '菜品更新成功', dish_output_model)
    @dish_ns.response(HTTPStatus.BAD_REQUEST, '输入参数无效')
    @dish_ns.response(HTTPStatus.UNAUTHORIZED, '需要认证')
    @dish_ns.response(HTTPStatus.FORBIDDEN, '需要管理员权限')
    @dish_ns.response(HTTPStatus.NOT_FOUND, '菜品未找到')
    @dish_ns.response(HTTPStatus.CONFLICT, '菜品名称已存在')
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '更新失败')
    @jwt_required()
    @require_roles(["admin"])  # 仅管理员可更新
    @log_request
    @timing
    # 移除了 @validate_json
    def put(self, dish_id):
        """更新指定 ID 的菜品信息 (仅管理员)"""
        update_data = request.get_json()
        if not update_data:  # 确保至少有内容提交
            return bad_request("请求体不能为空。")

        # 调用服务层函数，它会在失败时抛出异常
        updated_dish_data = dish_service.update_dish(dish_id=dish_id, update_data=update_data)

        logger.info(f"管理员更新菜品: ID={dish_id}")
        return success(message="菜品更新成功", data=updated_dish_data)

    @dish_ns.doc('delete_dish_permanently', security='jsonWebToken')
    @dish_ns.response(HTTPStatus.NO_CONTENT, '菜品永久删除成功')
    @dish_ns.response(HTTPStatus.UNAUTHORIZED, '需要认证')
    @dish_ns.response(HTTPStatus.FORBIDDEN, '需要管理员权限')
    @dish_ns.response(HTTPStatus.NOT_FOUND, '菜品未找到')
    @dish_ns.response(HTTPStatus.CONFLICT, '无法删除，存在关联数据')
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '删除失败')
    @jwt_required()
    @require_roles(["admin"])  # 仅管理员可永久删除
    @log_request
    @timing
    def delete(self, dish_id):
        """永久删除指定 ID 的菜品 (硬删除，仅管理员)"""
        # 服务层函数在失败时抛异常，成功时返回 True
        dish_service.delete_dish_permanently(dish_id)

        logger.info(f"管理员永久删除了菜品: ID={dish_id}")
        # 成功删除返回 204 No Content
        return no_content(message="菜品永久删除成功")


# --- 额外的管理接口：上架/下架 ---
@dish_ns.route("/<int:dish_id>/availability")
@dish_ns.param('dish_id', '菜品 ID')
class DishAvailability(Resource):

    @dish_ns.doc('set_dish_availability', security='jsonWebToken')
    @dish_ns.expect(dish_ns.model('SetAvailabilityInput', {  # 定义简单的输入模型
        'is_available': fields.Boolean(required=True, description='设置新的上架状态 (true/false)')
    }), validate=True)
    @dish_ns.response(HTTPStatus.OK, '菜品可用性设置成功')
    @dish_ns.response(HTTPStatus.BAD_REQUEST, '输入参数无效')
    @dish_ns.response(HTTPStatus.UNAUTHORIZED, '需要认证')
    @dish_ns.response(HTTPStatus.FORBIDDEN, '需要管理员权限')
    @dish_ns.response(HTTPStatus.NOT_FOUND, '菜品未找到')
    @dish_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, '设置失败')
    @jwt_required()
    @require_roles(["admin"])  # 仅管理员可操作
    @log_request
    @timing
    def put(self, dish_id):
        """设置菜品的上架或下架状态 (仅管理员)"""
        data = request.get_json()
        is_available = data.get('is_available')  # expect 已确保存在且为布尔值

        # 调用服务层函数
        dish_service.set_dish_availability(dish_id=dish_id, is_available=is_available)

        action = "上架" if is_available else "下架"
        logger.info(f"管理员将菜品 {dish_id} 设置为 {action} 状态。")
        return success(message=f"菜品已成功{action}")
