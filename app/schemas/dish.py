"""
Schemas for dish.
"""

from decimal import Decimal

from .base import BaseScheme, BaseSchemeAdd


class DishScheme(BaseScheme):
    """
    Dish schema to response.
    """
    submenu_id: int
    price: Decimal


class DishSchemeAdd(BaseSchemeAdd):
    """
    Schema for dish creation & modification
    """
    price: Decimal
