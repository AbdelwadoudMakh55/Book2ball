"""Change default for images_url

Revision ID: a2169ed7ad29
Revises: 2ba6f2fdc324
Create Date: 2024-11-16 13:45:00.402440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2169ed7ad29'
down_revision: Union[str, None] = '2ba6f2fdc324'
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
