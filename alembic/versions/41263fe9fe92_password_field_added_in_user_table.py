"""password field added in User table

Revision ID: 41263fe9fe92
Revises: 29dc0fa40d2b
Create Date: 2023-07-19 19:46:06.539461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41263fe9fe92'
down_revision = '29dc0fa40d2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.drop_column('users', 'surname')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
