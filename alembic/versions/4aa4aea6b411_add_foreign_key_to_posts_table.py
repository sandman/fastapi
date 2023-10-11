"""Add foreign key to posts table

Revision ID: 4aa4aea6b411
Revises: 1d474f3abab4
Create Date: 2023-10-11 12:28:53.672026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4aa4aea6b411"
down_revision: Union[str, None] = "1d474f3abab4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts", type_="foreignkey")
    pass
