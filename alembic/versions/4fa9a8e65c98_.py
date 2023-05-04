"""empty message

Revision ID: 4fa9a8e65c98
Revises: 
Create Date: 2023-05-04 09:09:38.268998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fa9a8e65c98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hashtag_name'), 'hashtag', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('follower',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_follower_id'), 'follower', ['id'], unique=False)
    op.create_table('tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=280), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('bio', sa.String(length=256), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profile_id'), 'user_profile', ['id'], unique=False)
    op.create_table('tweet_hashtags',
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('hashtag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hashtag_id'], ['hashtag.id'], ),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ),
    sa.PrimaryKeyConstraint('tweet_id', 'hashtag_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet_hashtags')
    op.drop_index(op.f('ix_user_profile_id'), table_name='user_profile')
    op.drop_table('user_profile')
    op.drop_table('tweet')
    op.drop_index(op.f('ix_follower_id'), table_name='follower')
    op.drop_table('follower')
    op.drop_table('user')
    op.drop_index(op.f('ix_hashtag_name'), table_name='hashtag')
    op.drop_table('hashtag')
    # ### end Alembic commands ###
