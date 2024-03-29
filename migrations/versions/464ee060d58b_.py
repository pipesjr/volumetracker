"""empty message

Revision ID: 464ee060d58b
Revises: 
Create Date: 2019-11-06 08:56:32.133834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464ee060d58b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meso', sa.Column('session_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_meso_session_id'), 'meso', ['session_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_meso_session_id'), table_name='meso')
    op.drop_column('meso', 'session_id')
    # ### end Alembic commands ###
