"""empty message

Revision ID: a3d5fc43255d
Revises: 9918ff66ac46
Create Date: 2022-04-26 14:08:40.599297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3d5fc43255d'
down_revision = '9918ff66ac46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Favourites', 'temp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Favourites', sa.Column('temp', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
