"""create usually_bought_next table

Revision ID: 87bc0051fcc2
Revises: 15f65bdb25f6
Create Date: 2020-05-30 03:02:17.538538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87bc0051fcc2'
down_revision = '15f65bdb25f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tesco_usually_bought_next',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_url', sa.String(length=255)),
        sa.Column('product_title', sa.String(length=255)),
        sa.Column('product_image_url', sa.String(length=255)),
        sa.Column('price', sa.String(length=255)),
        sa.Column('parent_url', sa.String(length=255))
    )


def downgrade():
    op.drop_table('tesco_usually_bought_next')
