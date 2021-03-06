"""empty message

Revision ID: 3348bd3ffb82
Revises: 7f48c8301928
Create Date: 2021-08-13 10:51:21.486929

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3348bd3ffb82'
down_revision = '7f48c8301928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actual_load',
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
    op.create_table('predicted_load',
    sa.Column('Date, time', sa.DateTime(), nullable=False),
    sa.Column('Period', sa.Integer(), nullable=False),
    sa.Column('Predicted grid load(MWh)', sa.Float(), nullable=False),
    sa.Column('Predicted market price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('Date, time'),
    sa.UniqueConstraint('Date, time')
    )
    op.drop_index('Date, time', table_name='actualload')
    op.drop_table('actualload')
    op.drop_index('Date, time', table_name='predictedload')
    op.drop_table('predictedload')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('predictedload',
    sa.Column('Date, time', mysql.DATETIME(), nullable=False),
    sa.Column('Period', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Predicted grid load(MWh)', mysql.FLOAT(), nullable=False),
    sa.Column('Predicted market price', mysql.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('Date, time'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('Date, time', 'predictedload', ['Date, time'], unique=True)
    op.create_table('actualload',
    sa.Column('Date, time', mysql.DATETIME(), nullable=False),
    sa.Column('Period', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Volume Generated onsite', mysql.FLOAT(), nullable=True),
    sa.Column('Volume consumed onsite', mysql.FLOAT(), nullable=True),
    sa.Column('Imbalance volume', mysql.FLOAT(), nullable=True),
    sa.Column('Imbalance Price', mysql.FLOAT(), nullable=True),
    sa.Column('Net profit', mysql.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('Date, time'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('Date, time', 'actualload', ['Date, time'], unique=True)
    op.drop_table('predicted_load')
    op.drop_table('actual_load')
    # ### end Alembic commands ###
