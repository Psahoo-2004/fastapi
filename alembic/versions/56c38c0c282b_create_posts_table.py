"""create posts table

Revision ID: 56c38c0c282b
Revises: 
Create Date: 2025-09-03 22:42:26.722380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56c38c0c282b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("post",sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                          ,sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post')
    pass
