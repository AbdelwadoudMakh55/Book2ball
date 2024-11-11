"""Add city attribute to PitchOwner

Revision ID: 95eb6d46aa8d
Revises: bdd2006ecfb1
Create Date: 2024-11-11 09:51:26.934915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95eb6d46aa8d'
down_revision: Union[str, None] = 'bdd2006ecfb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
