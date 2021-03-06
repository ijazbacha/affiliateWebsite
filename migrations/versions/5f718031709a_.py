"""empty message

Revision ID: 5f718031709a
Revises: 33e9f02044c8
Create Date: 2021-06-13 11:44:21.294955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f718031709a'
down_revision = '33e9f02044c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('owner', sa.Column('last_message_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('owner', 'last_message_read_time')
    # ### end Alembic commands ###
