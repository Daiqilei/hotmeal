# -*- coding: utf-8 -*-
"""
File Name:     /app/models/__init__.py
Project:       hotmeal
Author:        taichilei
Created:       2025-04-23
Description:   models init
"""

from flask_sqlalchemy import SQLAlchemy

from .category import Category
from .dish import Dish
from .user import User
from .order import Order
from .dining_area import DiningArea
from .chat import Chat
from .order_item import OrderItem

db = SQLAlchemy()

__all__ = ["db", "Dish", "User", "Order", "DiningArea", "Category", "Chat", "OrderItem"]
