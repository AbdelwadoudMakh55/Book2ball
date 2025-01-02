"""Add attributes

Revision ID: 2c869c91e327
Revises: 8dc9a1d17b66
Create Date: 2024-11-11 12:40:12.060240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c869c91e327'
down_revision: Union[str, None] = '8dc9a1d17b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
