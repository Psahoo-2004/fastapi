"""add foreign=key to post table

Revision ID: 6801409dc93d
Revises: 53a697fcfa6d
Create Date: 2025-09-03 23:10:45.145201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6801409dc93d'
down_revision: Union[str, Sequence[str], None] = '53a697fcfa6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post',sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table='post',referent_table='user',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk',table_name='post')
    op.drop_column('post','owner_id')
    pass
