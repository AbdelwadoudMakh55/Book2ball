"""Add images_url attribute to Pitch

Revision ID: 8dc9a1d17b66
Revises: 95eb6d46aa8d
Create Date: 2024-11-11 12:30:12.407624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dc9a1d17b66'
down_revision: Union[str, None] = '95eb6d46aa8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
