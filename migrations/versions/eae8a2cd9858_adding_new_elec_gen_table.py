"""Adding new elec_gen table

Revision ID: eae8a2cd9858
Revises: a683af7ee05a
Create Date: 2021-07-22 14:36:30.812155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eae8a2cd9858'
down_revision = 'a683af7ee05a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('elec_gen',
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('electricity_gen', sa.Float(), nullable=True),
    sa.Column('device', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('date_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('elec_gen')
    # ### end Alembic commands ###
