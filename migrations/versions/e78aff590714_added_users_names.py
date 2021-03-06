"""added users names

Revision ID: e78aff590714
Revises: 86b999c87738
Create Date: 2021-03-13 20:51:16.825716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78aff590714'
down_revision = '86b999c87738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('surname', sa.String(length=128), nullable=True))
    op.drop_index('ix_user_username', table_name='user')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=64), nullable=True))
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.drop_column('user', 'surname')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
