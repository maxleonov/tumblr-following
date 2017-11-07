"""Add following.user_name

Revision ID: f573f3b19b09
Revises: 80d964f3edff
Create Date: 2017-11-07 15:08:56.747877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f573f3b19b09'
down_revision = '80d964f3edff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('following', sa.Column('user_name', sa.VARCHAR()))


def downgrade():
    pass
