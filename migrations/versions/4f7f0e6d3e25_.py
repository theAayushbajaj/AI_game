"""empty message

Revision ID: 4f7f0e6d3e25
Revises: 5f78f7976bae
Create Date: 2019-03-03 11:44:49.231604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f7f0e6d3e25'
down_revision = '5f78f7976bae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_email', sa.String(length=100), nullable=False),
    sa.Column('child_email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parents')
    # ### end Alembic commands ###
