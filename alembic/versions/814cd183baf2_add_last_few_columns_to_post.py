"""add last few columns to post

Revision ID: 814cd183baf2
Revises: 6801409dc93d
Create Date: 2025-09-03 23:16:43.117558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '814cd183baf2'
down_revision: Union[str, Sequence[str], None] = '6801409dc93d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('post',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post','published')
    op.drop_column('post','created_at')
    pass
