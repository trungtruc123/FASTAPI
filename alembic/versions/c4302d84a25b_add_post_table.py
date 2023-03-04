"""add post table

Revision ID: c4302d84a25b
Revises: 
Create Date: 2023-03-05 00:32:31.157067

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c4302d84a25b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
