"""add label in subgroup

Revision ID: 951a6b738ad0
Revises: b04a73b00266
Create Date: 2022-06-11 02:36:37.081188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '951a6b738ad0'
down_revision = 'b04a73b00266'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subgroup', sa.Column('label', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subgroup', 'label')
    # ### end Alembic commands ###
