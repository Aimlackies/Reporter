"""merging two heads

Revision ID: 21d138d4483a
Revises: 24e169623a73, 7997e4d93b18
Create Date: 2021-09-19 16:28:08.781806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21d138d4483a'
down_revision = ('24e169623a73', '7997e4d93b18')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
