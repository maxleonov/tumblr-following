"""initial migration

Revision ID: 80d964f3edff
Revises:
Create Date: 2017-11-07 15:00:14.942921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80d964f3edff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('blog_name', sa.VARCHAR(), nullable=True),
    sa.Column('post_url', sa.VARCHAR(), nullable=True),
    sa.Column('reblogged_from_name', sa.VARCHAR(), nullable=True),
    sa.Column('reblogged_root_name', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('following',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('url', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('posts')
    op.drop_table('following')
