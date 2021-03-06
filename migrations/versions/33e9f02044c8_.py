"""empty message

Revision ID: 33e9f02044c8
Revises: 8675f6b8a342
Create Date: 2021-06-13 11:41:49.650558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33e9f02044c8'
down_revision = '8675f6b8a342'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'timestamp')
    # ### end Alembic commands ###
