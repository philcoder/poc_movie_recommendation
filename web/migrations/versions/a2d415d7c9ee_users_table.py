"""users table

Revision ID: a2d415d7c9ee
Revises: 8156df4de080
Create Date: 2019-05-20 17:54:28.167764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2d415d7c9ee'
down_revision = '8156df4de080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('username', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('userrole', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
