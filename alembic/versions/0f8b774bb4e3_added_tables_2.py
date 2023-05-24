"""added tables 2

Revision ID: 0f8b774bb4e3
Revises: 680ebd27daac
Create Date: 2023-05-23 13:04:37.943210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f8b774bb4e3'
down_revision = '680ebd27daac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('code_expiration_time', sa.DateTime(), nullable=True))
    op.drop_column('user', 'cede_expiration_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('cede_expiration_time', sa.DATETIME(), nullable=True))
    op.drop_column('user', 'code_expiration_time')
    # ### end Alembic commands ###