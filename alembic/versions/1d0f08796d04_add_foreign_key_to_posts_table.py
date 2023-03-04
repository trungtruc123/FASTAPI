"""add foreign key to posts table

Revision ID: 1d0f08796d04
Revises: 3b3fe9d42de5
Create Date: 2023-03-05 00:56:52.935103

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1d0f08796d04'
down_revision = '3b3fe9d42de5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk", source_table="posts", referent_table="users", local_cols=["owner_id"],
                          remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
