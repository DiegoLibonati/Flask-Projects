"""empty message

Revision ID: 99e1e06b4a05
Revises: cb4ca6d87091
Create Date: 2022-07-22 23:16:21.266062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99e1e06b4a05'
down_revision = 'cb4ca6d87091'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_banner', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile_banner')
    # ### end Alembic commands ###
