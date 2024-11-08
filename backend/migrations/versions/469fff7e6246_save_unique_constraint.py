"""Save unique constraint

Revision ID: 469fff7e6246
Revises: 8874d1eda33a
Create Date: 2024-11-04 18:52:55.563935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '469fff7e6246'
down_revision = '8874d1eda33a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_save_user', ['user_id', 'content_type', 'content_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('saves', schema=None) as batch_op:
        batch_op.drop_constraint('unique_save_user', type_='unique')

    # ### end Alembic commands ###
