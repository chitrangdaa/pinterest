"""empty message

Revision ID: 6d2bc59d2974
Revises: f917619c0cf2
Create Date: 2022-06-22 11:27:15.022193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d2bc59d2974'
down_revision = 'f917619c0cf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pinboard', sa.Column('pin_board_name', sa.String(length=80), nullable=False))
    op.drop_column('pinboard', 'board_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pinboard', sa.Column('board_name', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.drop_column('pinboard', 'pin_board_name')
    # ### end Alembic commands ###
