"""Initial migration

Revision ID: 55eac7e08882
Revises: 189931546c10
Create Date: 2024-09-19 08:23:59.228579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55eac7e08882'
down_revision: Union[str, None] = '189931546c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mentors', 'feedbacks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mentors', sa.Column('feedbacks', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###