"""empty message

Revision ID: 7f48c8301928
Revises: f8704cc7bb08
Create Date: 2021-08-13 10:49:48.366837

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7f48c8301928'
down_revision = 'f8704cc7bb08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actualload',
    sa.Column('Date, time', sa.DateTime(), nullable=False),
    sa.Column('Period', sa.Integer(), nullable=False),
    sa.Column('Volume Generated onsite', sa.Float(), nullable=True),
    sa.Column('Volume consumed onsite', sa.Float(), nullable=True),
    sa.Column('Imbalance volume', sa.Float(), nullable=True),
    sa.Column('Imbalance Price', sa.Float(), nullable=True),
    sa.Column('Net profit', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('Date, time'),
    sa.UniqueConstraint('Date, time')
    )
    op.create_table('predictedload',
    sa.Column('Date, time', sa.DateTime(), nullable=False),
    sa.Column('Period', sa.Integer(), nullable=False),
    sa.Column('Predicted grid load(MWh)', sa.Float(), nullable=False),
    sa.Column('Predicted market price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('Date, time'),
    sa.UniqueConstraint('Date, time')
    )
    op.create_unique_constraint(None, 'trading', ['Date, time'])
    op.drop_column('trading', 'Volume Generated onsite')
    op.drop_column('trading', 'Imbalance volume')
    op.drop_column('trading', 'Imbalance Price')
    op.drop_column('trading', 'Predicted grid load(MWh)')
    op.drop_column('trading', 'Volume consumed onsite')
    op.drop_column('trading', 'Net profit')
    op.drop_column('trading', 'Predicted market price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trading', sa.Column('Predicted market price', mysql.FLOAT(), nullable=False))
    op.add_column('trading', sa.Column('Net profit', mysql.FLOAT(), nullable=True))
    op.add_column('trading', sa.Column('Volume consumed onsite', mysql.FLOAT(), nullable=True))
    op.add_column('trading', sa.Column('Predicted grid load(MWh)', mysql.FLOAT(), nullable=False))
    op.add_column('trading', sa.Column('Imbalance Price', mysql.FLOAT(), nullable=True))
    op.add_column('trading', sa.Column('Imbalance volume', mysql.FLOAT(), nullable=True))
    op.add_column('trading', sa.Column('Volume Generated onsite', mysql.FLOAT(), nullable=True))
    op.drop_constraint(None, 'trading', type_='unique')
    op.drop_table('predictedload')
    op.drop_table('actualload')
    # ### end Alembic commands ###