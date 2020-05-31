"""create tesco_reviews table

Revision ID: 15f65bdb25f6
Revises: b7faac7d1491
Create Date: 2020-05-30 02:36:12.849967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f65bdb25f6'
down_revision = 'b7faac7d1491'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tesco_reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('review_title', sa.String(length=255)),
        sa.Column('stars_count', sa.Integer),
        sa.Column('author', sa.String(length=255)),
        sa.Column('date', sa.String(length=255)),
        sa.Column('review_text', sa.Text),
        sa.Column('parent_url', sa.String(length=255))
    )


def downgrade():
    op.drop_table('tesco_reviews')
