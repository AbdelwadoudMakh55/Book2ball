"""Remove availability from Pitch, make start time unique

Revision ID: 3518127fdcd7
Revises: d0ba3e5521a9
Create Date: 2024-11-16 22:47:53.939121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = '3518127fdcd7'
down_revision: Union[str, None] = 'd0ba3e5521a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
