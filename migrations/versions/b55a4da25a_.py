"""empty message

Revision ID: b55a4da25a
Revises: 49a31a27858
Create Date: 2015-06-13 18:30:26.747589

"""

# revision identifiers, used by Alembic.
revision = 'b55a4da25a'
down_revision = '49a31a27858'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('claim',
    sa.Column('claim_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('page_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['page.page_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('claim_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('claim')
    ### end Alembic commands ###
