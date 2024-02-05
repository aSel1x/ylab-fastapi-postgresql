"""
Schemas for menu.
"""

from .base import BaseScheme, BaseSchemeAdd


class MenuScheme(BaseScheme):
    """
    Menu schema to response.
    """
    submenus_count: int
    dishes_count: int


class MenuSchemeAdd(BaseSchemeAdd):
    """
    Schema for menu creation & modification
    """
