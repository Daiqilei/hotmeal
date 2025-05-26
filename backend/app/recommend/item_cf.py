# -*- coding: utf-8 -*-
"""
@File       : item_cf.py
@Date       : 2025-03-01 (Refactored: 2025-03-01)
@Description:
@Project    : HotMeal - Personalized Meal Ordering System Based on Recommendation Algorithms

"""

import logging
import numpy as np
from sqlalchemy import text

from app.utils.db import db
from app.recommend.time_decay import TimeDecayHelper

logger = logging.getLogger(__name__)


class ItemCFRecommender:
    """基于菜品相似度为的协同过滤推荐器"""

    @staticmethod
    def get_user_ordered_dishes(user_id) -> set:
        """获取指定用户购买过的所有不重复的菜品 ID 集合"""
        logger.debug(f"查询用户 {user_id} 购买过的菜品...")
        try:
            # --- 修正 SQL 查询：从 order_items 获取 dish_id ---
            query = text("""
                SELECT DISTINCT oi.dish_id
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.user_id = :user_id
            """)
            # 使用 db.session.execute
            result = db.session.execute(query, {"user_id": user_id}).fetchall()
            # 将结果转换为 set
            ordered_dishes = {row[0] for row in result}  # 假设返回的是元组 (dish_id,)
            logger.debug(f"用户 {user_id} 购买过的菜品 ID 集合: {ordered_dishes}")
            return ordered_dishes
        except Exception as e:
            logger.error(f"查询用户 {user_id} 购买记录时出错: {e}", exc_info=True)
            return set()  # 出错时返回空集合

    @staticmethod
    def compute_dish_similarity():
        """基于共同购买行为计算菜品相似度矩阵"""
        logger.info("开始计算菜品相似度矩阵...")
        try:
            # --- 修正 SQL 查询：从 order_items 获取 user_id 和 dish_id ---
            # 假设 orders 表有 order_id, user_id
            # 假设 order_items 表有 order_id, dish_id
            query = text("""
                SELECT o.user_id, oi.dish_id
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
            """)
            # 使用 db.session.execute
            results = db.session.execute(query).fetchall()
            logger.info(f"从数据库获取了 {len(results)} 条用户-菜品购买记录。")

        except Exception as e:
            logger.error(f"计算相似度时查询数据库出错: {e}", exc_info=True)
            return {}  # 查询失败则返回空字典

        user_dish_matrix = {}
        # 使用列名访问结果 (如果 fetchall 返回的是 Row 对象)
        # 假设返回的是元组 (user_id, dish_id)
        for row in results:
            user_id, dish_id = row
            user_dish_matrix.setdefault(user_id, set()).add(dish_id)

        if not user_dish_matrix:
            logger.warning("没有有效的用户购买数据来计算相似度。")
            return {}

        dish_similarity = {}
        # 获取所有涉及的菜品 ID
        dishes = list(set(dish for dishes in user_dish_matrix.values() for dish in dishes))
        logger.info(f"共涉及 {len(dishes)} 个不同的菜品进行相似度计算。")

        # 使用更高效的方式构建购买了特定菜品的用户集合
        dish_user_matrix = {}
        for user, user_dishes in user_dish_matrix.items():
            for dish in user_dishes:
                dish_user_matrix.setdefault(dish, set()).add(user)

        # 计算相似度
        for i, dish_a in enumerate(dishes):
            for j in range(i + 1, len(dishes)):
                dish_b = dishes[j]

                users_a = dish_user_matrix.get(dish_a, set())
                users_b = dish_user_matrix.get(dish_b, set())

                intersection = len(users_a & users_b)
                len_a = len(users_a)
                len_b = len(users_b)

                if intersection > 0 and len_a > 0 and len_b > 0:
                    # 使用 Jaccard 相似度或余弦相似度，这里保持原来的余弦相似度计算方式
                    similarity = intersection / np.sqrt(len_a * len_b)
                else:
                    similarity = 0.0

                if similarity > 0:  # 只存储有相似度的项
                    dish_similarity.setdefault(dish_a, {})[dish_b] = similarity
                    dish_similarity.setdefault(dish_b, {})[dish_a] = similarity

        logger.info("菜品相似度矩阵计算完成。")
        return dish_similarity

    def recommend_by_item_similarity(self, user_id, limit=10):
        """
        注意：这里返回的是
        根据用户购买历史和物品相似度进行推荐
        """
        logger.info(f"开始为用户 {user_id} 生成协同过滤推荐...")
        user_dishes = self.get_user_ordered_dishes(user_id)  # 调用修正后的方法获取用户购买过的菜品

        if not user_dishes:
            logger.info(f"用户 {user_id} 没有购买记录，无法进行协同过滤推荐。")
            return []

        logger.info(f"用户 {user_id} 购买过的菜品: {user_dishes}")
        dish_similarity = self.compute_dish_similarity()  # 计算或获取相似度矩阵
        if not dish_similarity:
            logger.warning("无法获取菜品相似度矩阵，推荐失败。")
            return []

        dish_scores = {}

        # 遍历用户购买过的每个菜品
        for purchased_dish in user_dishes:
            # 获取与该菜品相似的其他菜品及其相似度分数
            for related_dish, similarity_score in dish_similarity.get(purchased_dish, {}).items():
                # 如果相似的菜品用户没买过
                if related_dish not in user_dishes:
                    # TODO: 考虑菜品的热门度或其他因素进行分数加权
                    # score = similarity_score * popularity_factor(related_dish)
                    # 累加相似度分数
                    dish_scores[related_dish] = dish_scores.get(related_dish, 0) + similarity_score

        # 按分数降序排序，取前 N 个
        # 使用 items() 并指定 lambda 函数的参数名，更清晰
        recommended_dishes = sorted(dish_scores.items(), key=lambda item: item[1], reverse=True)[
                             :limit]

        logger.info(f"为用户 {user_id} 生成了 {len(recommended_dishes)} 条推荐。")

        if not recommended_dishes:
            return {}

        # 构造返回值为字典：{dish_id: score}
        return {dish_id: round(score, 4) for dish_id, score in recommended_dishes}

    @staticmethod
    def get_user_ordered_dishes_with_time(user_id) -> dict:
        """
        获取用户购买过的菜品及其对应的首次购买时间。

        返回结构：
        {
            dish_id1: datetime,
            dish_id2: datetime,
            ...
        }
        """
        logger.debug(f"查询用户 {user_id} 的菜品购买时间记录...")
        try:
            query = text("""
                SELECT oi.dish_id, MIN(o.created_at) AS first_purchase_time
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.user_id = :user_id
                GROUP BY oi.dish_id
            """)
            results = db.session.execute(query, {"user_id": user_id}).fetchall()
            dish_time_map = {row[0]: row[1] for row in results}
            logger.debug(f"用户 {user_id} 菜品购买时间记录: {dish_time_map}")
            return dish_time_map
        except Exception as e:
            logger.error(f"查询用户 {user_id} 购买时间时出错: {e}", exc_info=True)
            return {}

    def recommend_by_item_similarity_with_time_decay(self, user_id, limit=10):
        """
        使用时间衰减因子对菜品推荐进行加权优化。
        结合用户的购买行为时间及菜品相似度，为用户推荐近期更相关的菜品。
        """
        logger.info(f"[时间衰减] 为用户 {user_id} 生成推荐...")
        user_dishes = self.get_user_ordered_dishes(user_id)
        if not user_dishes:
            logger.info(f"用户 {user_id} 无购买记录，跳过推荐。")
            return {}

        dish_similarity = self.compute_dish_similarity()
        if not dish_similarity:
            logger.warning("菜品相似度矩阵为空，跳过推荐。")
            return {}

        user_dish_time_map = self.get_user_ordered_dishes_with_time(user_id)
        if not user_dish_time_map:
            logger.warning(f"用户 {user_id} 无有效购买时间数据，跳过推荐。")
            return {}

        t_first = min(user_dish_time_map.values())
        t_last = max(user_dish_time_map.values())
        dish_scores = {}

        for purchased_dish in user_dishes:
            purchase_time = user_dish_time_map.get(purchased_dish)
            if not purchase_time:
                continue
            time_weight = TimeDecayHelper.compute_exponential_decay(
                t_event=purchase_time,
                t_first=t_first,
                t_last=t_last,
                contribution=1.0
            )
            for related_dish, similarity_score in dish_similarity.get(purchased_dish, {}).items():
                if related_dish not in user_dishes:
                    dish_scores[related_dish] = dish_scores.get(related_dish,
                                                                0) + similarity_score * time_weight

        recommended_dishes = sorted(dish_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        logger.info(f"[时间衰减] 为用户 {user_id} 推荐了 {len(recommended_dishes)} 道菜品。")

        return {dish_id: round(score, 4) for dish_id, score in recommended_dishes}
