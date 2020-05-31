"""create tesco_parser table

Revision ID: b7faac7d1491
Revises: 
Create Date: 2020-05-28 20:00:42.497910

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import LONGTEXT

# revision identifiers, used by Alembic.
revision = 'b7faac7d1491'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tesco_parser',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_url', sa.String(length=255)),
        sa.Column('product_id', sa.Integer),
        sa.Column('image_url', sa.String(length=255)),
        sa.Column('product_title', sa.String(length=255)),
        sa.Column('category', sa.String(length=255)),
        sa.Column('price', sa.String(length=255)),
        sa.Column('product_description', sa.Text),
        sa.Column('name_and_address', sa.String(length=255)),
        sa.Column('return_address', sa.Text),
        sa.Column('net_contents', sa.String(length=255)),
        sa.Column('review', LONGTEXT),
        sa.Column('usually_bought_next_products', sa.Text)
    )


def downgrade():
    op.drop_table('tesco_parser')
