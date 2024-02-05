"""
Submenu model.
"""

from typing import List

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Submenu(Base):
    menu_id: Mapped[int] = mapped_column(sa.Integer, ForeignKey(
        'menu.id', ondelete='CASCADE'), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    menu: Mapped['Menu'] = relationship(
        back_populates='submenus'
    )
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu',
        lazy='selectin',
        cascade='all, delete'
    )

    @property
    def dishes_count(self):
        return len(self.dishes)
