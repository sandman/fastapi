"""Add primary key to posts

Revision ID: 5c4cb2219753
Revises: a39f064c4473
Create Date: 2023-10-16 17:27:47.314830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c4cb2219753'
down_revision: Union[str, None] = 'a39f064c4473'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
