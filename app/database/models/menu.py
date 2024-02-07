"""
Menu model.
"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Menu(Base):
    title: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    submenus: Mapped[list['Submenu']] = relationship(
        back_populates='menu',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    @property
    def submenus_count(self):
        return len(self.submenus)

    @property
    def dishes_count(self):
        return sum(len(submenu.dishes) for submenu in self.submenus)
