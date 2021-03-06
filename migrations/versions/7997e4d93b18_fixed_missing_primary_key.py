"""fixed missing primary key

Revision ID: 7997e4d93b18
Revises: 28afb6ca9aac
Create Date: 2021-09-16 01:44:57.314907

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7997e4d93b18'
down_revision = '28afb6ca9aac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('real_power_readings',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('device_name', sa.String(length=255), nullable=False),
    sa.Column('power', sa.Float(), nullable=True),
    sa.Column('power_generator', sa.Boolean(), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('date_time', 'device_name'),
    sa.UniqueConstraint('date_time', 'device_name')
    )
    op.create_table('real_site_readings',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('power', sa.Float(), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('date_time')
    )
    #op.drop_index('date_time', table_name='real_power_generation')
    op.drop_table('real_power_generation')
    op.drop_table('real_site_reading')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('real_site_reading',
    sa.Column('date_time', mysql.DATETIME(), nullable=False),
    sa.Column('temperature', mysql.FLOAT(), nullable=True),
    sa.Column('power', mysql.FLOAT(), nullable=True),
    sa.Column('create_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('date_time'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('real_power_generation',
    sa.Column('date_time', mysql.DATETIME(), nullable=False),
    sa.Column('power', mysql.FLOAT(), nullable=True),
    sa.Column('device_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('create_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('power_generator', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('date_time'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    #op.create_index('date_time', 'real_power_generation', ['date_time', 'device_name'], unique=False)
    op.drop_table('real_site_readings')
    op.drop_table('real_power_readings')
    # ### end Alembic commands ###
