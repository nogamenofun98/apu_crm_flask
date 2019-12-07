"""empty message

Revision ID: 3eae94672bba
Revises: 
Create Date: 2019-12-07 10:29:19.251709

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3eae94672bba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('industry_area', sa.Column('industry_test', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('industry_area', 'industry_test')
    # ### end Alembic commands ###