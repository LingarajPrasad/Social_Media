"""Create posts Table

Revision ID: 77ab4c8200f7
Revises: 
Create Date: 2023-02-16 02:43:33.499830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77ab4c8200f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False,primary_key=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
