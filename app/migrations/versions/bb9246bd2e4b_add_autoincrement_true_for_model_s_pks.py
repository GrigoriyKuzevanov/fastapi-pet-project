"""add autoincrement True for model's pks

Revision ID: bb9246bd2e4b
Revises: e159d0e74d6f
Create Date: 2024-08-07 10:15:48.297868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb9246bd2e4b'
down_revision: Union[str, None] = 'e159d0e74d6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
