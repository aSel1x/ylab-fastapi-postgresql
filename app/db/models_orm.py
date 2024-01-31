from typing import Optional
from decimal import Decimal

from sqlmodel import SQLModel, Field, String, Relationship
from pydantic import field_serializer


class MenusORM(SQLModel, table=True):
    __tablename__ = "menus"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(String)
    description: str = Field(String)
    submenus: list['SubmenusORM'] = Relationship(back_populates="menu")

    @field_serializer("id")
    def serialize_id(self, _id: str | int, _info):
        return str(_id)


class SubmenusORM(SQLModel, table=True):
    __tablename__ = "submenus"
    id: int = Field(default=None, primary_key=True)
    menu_id: Optional[int] = Field(default=None, foreign_key="menus.id")
    title: str = Field(String)
    description: str = Field(String)
    menu: Optional[MenusORM] = Relationship(back_populates="submenus")
    dishes: list['DishesORM'] = Relationship(back_populates="submenu")

    @field_serializer("id")
    def serialize_id(self, _id: str | int, _info):
        return str(_id)


class DishesORM(SQLModel, table=True):
    __tablename__ = "dishes"
    id: int = Field(default=None, primary_key=True)
    submenu_id: Optional[int] = Field(default=None, foreign_key="submenus.id")
    title: str = Field(String)
    description: str = Field(String)
    price: Decimal = Field(String)
    submenu: Optional[SubmenusORM] = Relationship(back_populates="dishes")

    @field_serializer("id")
    def serialize_id(self, _id: str | int, _info):
        return str(_id)
