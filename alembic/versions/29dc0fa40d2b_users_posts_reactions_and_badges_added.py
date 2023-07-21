"""Users, Posts, Reactions and Badges added

Revision ID: 29dc0fa40d2b
Revises: 
Create Date: 2023-07-19 19:21:25.696274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29dc0fa40d2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('post_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('in_reply_to_post_id', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(precision=32), nullable=True),
    sa.Column('longitude', sa.Float(precision=32), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('posts_reactions',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('reaction_id', sa.Integer(), nullable=False),
    sa.Column('reaction_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['reaction_id'], ['reactions.reaction_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'reaction_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts_reactions')
    op.drop_table('posts')
    # ### end Alembic commands ###