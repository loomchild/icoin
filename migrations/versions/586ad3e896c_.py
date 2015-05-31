"""empty message

Revision ID: 586ad3e896c
Revises: None
Create Date: 2015-05-31 13:19:42.586550

"""

# revision identifiers, used by Alembic.
revision = '586ad3e896c'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page',
    sa.Column('page_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url', sa.String(length=4096), nullable=False),
    sa.Column('domain', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('page_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page')
    ### end Alembic commands ###