"""empty message

Revision ID: 2d8d8d71d885
Revises: 5f718031709a
Create Date: 2021-06-13 13:12:10.233672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d8d8d71d885'
down_revision = '5f718031709a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('owner', schema=None) as batch_op:
        batch_op.drop_column('last_notification_read_time')

    with op.batch_alter_table('subscriber', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriber', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    with op.batch_alter_table('owner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_notification_read_time', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###
