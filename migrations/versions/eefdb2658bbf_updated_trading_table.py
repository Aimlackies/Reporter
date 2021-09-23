"""updated trading table

Revision ID: eefdb2658bbf
Revises: 9d29fab6fa31
Create Date: 2021-09-23 10:39:07.028528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eefdb2658bbf'
down_revision = '9d29fab6fa31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trading', sa.Column('Datetime', sa.DateTime(), nullable=False))
    op.drop_index('date_time', table_name='trading')
    op.create_unique_constraint(None, 'trading', ['Datetime', 'Period'])
    op.drop_column('trading', 'date_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trading', sa.Column('date_time', mysql.DATETIME(), nullable=False))
    op.drop_constraint(None, 'trading', type_='unique')
    op.create_index('date_time', 'trading', ['date_time', 'Period'], unique=False)
    op.drop_column('trading', 'Datetime')
    # ### end Alembic commands ###
