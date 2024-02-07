"""
Schemas for submenu.
"""

from .base import BaseScheme, BaseSchemeAdd, BaseSchemeError


class SubmenuScheme(BaseScheme):
    """
    Submenu schema to response.
    """
    menu_id: int
    dishes_count: int


class SubmenuSchemeAdd(BaseSchemeAdd):
    """
    Schema for submenu creation & modification
    """


class SubmenuNotFound(BaseSchemeError):
    detail: str = 'submenu not found'
