"""add user table

Revision ID: 3b3fe9d42de5
Revises: da2256a4caa2
Create Date: 2023-03-05 00:40:25.657562

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3b3fe9d42de5'
down_revision = 'da2256a4caa2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("create_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                              nullable=False),
                    sa.UniqueConstraint("email"),
                    sa.PrimaryKeyConstraint("id"))

    pass


def downgrade():
    op.drop_table("users")
    pass
