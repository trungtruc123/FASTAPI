"""add column to posts table

Revision ID: da2256a4caa2
Revises: c4302d84a25b
Create Date: 2023-03-05 00:36:28.755932

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'da2256a4caa2'
down_revision = 'c4302d84a25b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("context", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "context")
    pass
