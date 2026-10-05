"""add localized catalog fields

Revision ID: 0003
Revises: 0002
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("products", sa.Column("name_ar", sa.String(140), nullable=True))
    op.add_column("products", sa.Column("description_ar", sa.Text(), nullable=True))
    op.add_column("products", sa.Column("category_ar", sa.String(80), nullable=True))

def downgrade():
    op.drop_column("products", "category_ar")
    op.drop_column("products", "description_ar")
    op.drop_column("products", "name_ar")
