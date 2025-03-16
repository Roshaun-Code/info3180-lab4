"""empty message

Revision ID: 8faf5da7bea4
Revises: 24f9fcaa8987
Create Date: 2025-03-15 19:48:32.509660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8faf5da7bea4'
down_revision = '24f9fcaa8987'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
