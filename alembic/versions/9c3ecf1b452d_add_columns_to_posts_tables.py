"""add columns to posts tables

Revision ID: 9c3ecf1b452d
Revises: 1d0f08796d04
Create Date: 2023-03-05 01:09:10.554694

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c3ecf1b452d'
down_revision = '1d0f08796d04'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("create_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                                     nullable=False), )

    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "create_at")
    pass
