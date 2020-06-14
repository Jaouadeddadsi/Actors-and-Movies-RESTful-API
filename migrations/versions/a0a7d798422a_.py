"""empty message

Revision ID: a0a7d798422a
Revises:
Create Date: 2020-06-14 15:34:39.480344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0a7d798422a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=False),
                    sa.Column('gender', sa.String(length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_actors_name'), 'actors', ['name'], unique=False)
    op.create_table('movies',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('release_date', sa.Date(), nullable=False),
                    sa.Column('actor_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_table('movies')
    op.drop_index(op.f('ix_actors_name'), table_name='actors')
    op.drop_table('actors')
    # ### end Alembic commands ###
