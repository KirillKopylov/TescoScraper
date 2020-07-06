"""create products table

Revision ID: d94758fe3799
Revises: 
Create Date: 2020-07-05 13:28:54.903709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, JSON, TEXT, DECIMAL, TIMESTAMP

# revision identifiers, used by Alembic.
revision = 'd94758fe3799'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', BIGINT(unsigned=True), primary_key=True),
        sa.Column('product_id', BIGINT(unsigned=True), index=True, unique=True, nullable=False),
        sa.Column('url', VARCHAR(768), nullable=False),
        sa.Column('image_url', VARCHAR(768)),
        sa.Column('title', VARCHAR(100), nullable=False),
        sa.Column('category', VARCHAR(100)),
        sa.Column('price', DECIMAL(10, 3, unsigned=True)),
        sa.Column('description', TEXT),
        sa.Column('name_and_address', TEXT),
        sa.Column('return_address', TEXT),
        sa.Column('net_contents', TEXT),
        sa.Column('reviews', JSON),
        sa.Column('usually_bought_next', JSON),
        sa.Column('created_at', TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP()')),
        sa.Column('updated_at', TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP()'))
    )


def downgrade():
    op.drop_table('products')
