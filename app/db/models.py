from decimal import Decimal
from typing import Optional, Tuple, Union

from pydantic import BaseModel, field_serializer


class DishModel(BaseModel):
    id: Union[int, str] = None
    submenu_id: Optional[int] = None
    title: str
    description: str
    price: Decimal

    @field_serializer("id")
    def serialize_message(self, _id: str | int, _info):
        return str(_id)

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.submenu_id,
            self.title,
            self.description,
            self.price
        )


class SubMenuModel(BaseModel):
    id: Union[int, str] = None
    menu_id: Optional[int] = None
    title: str
    description: str
    dishes_count: Optional[int] = 0

    @field_serializer("id")
    def serialize_message(self, _id: str | int, _info):
        return str(_id)

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.menu_id,
            self.title,
            self.description
        )


class MenuModel(BaseModel):
    id: Union[int, str] = None
    title: str
    description: str
    submenus_count: Optional[int] = 0
    dishes_count: Optional[int] = 0

    @field_serializer("id")
    def serialize_message(self, _id: str | int, _info):
        return str(_id)

    def to_tuple(self) -> Tuple:
        return (
            self.id,
            self.title,
            self.description
        )
