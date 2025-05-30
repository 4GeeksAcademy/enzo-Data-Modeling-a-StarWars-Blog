"""empty message

Revision ID: b9b4290382e8
Revises: a5cffa318ac2
Create Date: 2025-05-28 01:42:37.069591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9b4290382e8'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.String(length=50), nullable=False),
    sa.Column('birth_year', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('climate', sa.String(length=100), nullable=False),
    sa.Column('population', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('subscription_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('subscription_date')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    op.drop_table('favorite_planet')
    op.drop_table('favorite_character')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###
