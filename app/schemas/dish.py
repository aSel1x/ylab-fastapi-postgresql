"""
Schemas for dish.
"""

from decimal import Decimal

from pydantic import field_validator

from .base import BaseScheme, BaseSchemeAdd, BaseSchemeError


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
    price: str

    @field_validator('price')
    @classmethod
    def convert_price_to_decimal(cls, v) -> Decimal:
        v = v.replace(',', '.')
        return Decimal(v).quantize(Decimal('0.00'))


class DishNotFound(BaseSchemeError):
    detail: str = 'dish not found'
