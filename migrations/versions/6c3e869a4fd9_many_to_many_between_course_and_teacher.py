"""many to many between course and teacher

Revision ID: 6c3e869a4fd9
Revises: ae3e895e09bf
Create Date: 2022-05-13 14:45:38.481103

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6c3e869a4fd9'
down_revision = 'ae3e895e09bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_teacher',
                    sa.Column('teacher_id', sa.Integer(), nullable=False),
                    sa.Column('course_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
                    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
                    sa.PrimaryKeyConstraint('teacher_id', 'course_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course_teacher')
    # ### end Alembic commands ###