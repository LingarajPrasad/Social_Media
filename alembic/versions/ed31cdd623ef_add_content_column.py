"""add content column

Revision ID: ed31cdd623ef
Revises: 77ab4c8200f7
Create Date: 2023-02-16 02:55:22.109458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed31cdd623ef'
down_revision = '77ab4c8200f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
