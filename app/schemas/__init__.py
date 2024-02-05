"""
Pydantic schemas.
"""

from app.schemas.base import BaseScheme, BaseSchemeAdd
from app.schemas.menu import MenuScheme, MenuSchemeAdd
from app.schemas.submenu import SubmenuScheme, SubmenuSchemeAdd
from app.schemas.dish import DishScheme, DishSchemeAdd

__all__ = (
    'BaseScheme',
    'BaseSchemeAdd',
    'MenuScheme',
    'MenuSchemeAdd',
    'SubmenuScheme',
    'SubmenuSchemeAdd',
    'DishScheme',
    'DishSchemeAdd',
)
