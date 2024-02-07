"""init

Revision ID: 8a18164e2eff
Revises:
Create Date: 2024-02-04 16:57:53.258138

"""
from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a18164e2eff'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_menu'))
                    )
    op.create_table('submenu',
                    sa.Column('menu_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], name=op.f(
                        'fk_submenu_menu_id_menu'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_submenu'))
                    )
    op.create_table('dish',
                    sa.Column('submenu_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('price', sa.Numeric(scale=2), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], name=op.f(
                        'fk_dish_submenu_id_submenu'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_dish'))
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###