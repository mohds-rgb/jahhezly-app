"""add store location context

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("stores", sa.Column("city", sa.String(80), nullable=True))
    op.add_column("stores", sa.Column("district", sa.String(80), nullable=True))
    op.add_column("stores", sa.Column("branch_code", sa.String(32), nullable=True))

def downgrade():
    op.drop_column("stores", "branch_code")
    op.drop_column("stores", "district")
    op.drop_column("stores", "city")
