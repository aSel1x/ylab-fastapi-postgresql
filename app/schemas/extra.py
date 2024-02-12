"""Schemas for extra endpoint"""

from pydantic import BaseModel

from .dish import DishScheme
from .menu import MenuScheme
from .submenu import SubmenuScheme


class SubmenuPlus(SubmenuScheme):
    dishes: list[DishScheme]


class MenuPlus(MenuScheme):
    submenus: list[SubmenuPlus]


class ExtraScheme(BaseModel):
    menus: list[MenuPlus] | None
