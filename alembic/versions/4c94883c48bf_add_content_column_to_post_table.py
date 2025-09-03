"""add content column to post table

Revision ID: 4c94883c48bf
Revises: 56c38c0c282b
Create Date: 2025-09-03 22:54:11.383388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c94883c48bf'
down_revision: Union[str, Sequence[str], None] = '56c38c0c282b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post','content')
    pass
