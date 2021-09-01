"""merging two heads

Revision ID: 34e14ce1bdb5
Revises: eae8a2cd9858, aa73e6cd5d62
Create Date: 2021-08-18 21:01:44.648032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34e14ce1bdb5'
down_revision = ('eae8a2cd9858', 'aa73e6cd5d62')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
