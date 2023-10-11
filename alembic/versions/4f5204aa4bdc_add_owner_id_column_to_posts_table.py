"""Add owner_id column to posts table

Revision ID: 4f5204aa4bdc
Revises: abd785d62596
Create Date: 2023-10-11 12:09:46.574483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f5204aa4bdc"
down_revision: Union[str, None] = "abd785d62596"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
    pass
