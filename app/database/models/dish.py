"""
Dish model.
"""

from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Dish(Base):
    submenu_id: Mapped[int] = mapped_column(sa.Integer, ForeignKey(
        'submenu.id', ondelete='CASCADE'), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    price: Mapped[Decimal] = mapped_column(sa.Numeric(scale=2), unique=False, nullable=False)
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')
