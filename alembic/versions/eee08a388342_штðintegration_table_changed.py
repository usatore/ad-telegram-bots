"""штÐintegration table changed

Revision ID: eee08a388342
Revises: eeeff7cb3640
Create Date: 2025-04-29 13:50:41.918406

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'eee08a388342'
down_revision: Union[str, None] = 'eeeff7cb3640'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogger_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blogger_id', sa.Integer(), nullable=False),
    sa.Column('money_amount', sa.Integer(), nullable=False),
    sa.Column('transaction_type', sa.Boolean(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['blogger_id'], ['blogger.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('money_amount', sa.Integer(), nullable=False),
    sa.Column('transaction_type', sa.Boolean(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('blogger_payment')
    op.drop_table('company_payment')
    op.add_column('integration', sa.Column('materials', sa.JSON(), nullable=True))
    op.add_column('integration', sa.Column('done', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('integration', 'done')
    op.drop_column('integration', 'materials')
    op.create_table('company_payment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('money_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('approved', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='company_payment_company_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='company_payment_pkey')
    )
    op.create_table('blogger_payment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('blogger_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('money_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('approved', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['blogger_id'], ['blogger.id'], name='blogger_payment_blogger_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='blogger_payment_pkey')
    )
    op.drop_table('company_transaction')
    op.drop_table('blogger_transaction')
    # ### end Alembic commands ###
