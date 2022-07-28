"""create tables

Revision ID: 689e145cc92c
Revises: 
Create Date: 2022-07-22 22:12:39.823403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689e145cc92c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "operation_type",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('name', sa.VARCHAR(20), nullable=False, unique=True),
        sa.Column('alias', sa.CHAR(1), nullable=False, unique=True),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "account_type",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('name', sa.VARCHAR(26), nullable=False, unique=True),
        sa.Column('alias', sa.CHAR(3), nullable=False, unique=True),
        sa.Column('operation', sa.BIGINT, sa.ForeignKey("operation_type.id"), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "currency",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('name', sa.VARCHAR(200), nullable=False, unique=True),
        sa.Column('alias', sa.VARCHAR(5), nullable=False, unique=True),
        sa.Column('default', sa.BOOLEAN, default=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "exchange",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('currency_default', sa.BIGINT, sa.ForeignKey("currency.id"), default=1),
        sa.Column('currency_buy', sa.BIGINT, sa.ForeignKey("currency.id"), nullable=False),
        sa.Column('datetime', sa.DATETIME, nullable=False),
        sa.Column('rate', sa.BIGINT, nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "account",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement='auto'),
        sa.Column('code', sa.VARCHAR(20), nullable=False, unique=True),
        sa.Column('name', sa.VARCHAR(200), nullable=False),
        sa.Column('balance', sa.BIGINT, nullable=False, default=0),
        sa.Column('alias', sa.VARCHAR(5), nullable=True, default=None, unique=True),
        sa.Column('currency', sa.BIGINT, sa.ForeignKey("currency.id"), nullable=False, default=1),
        sa.Column('account_type', sa.BIGINT, sa.ForeignKey("account_type.id"), nullable=False),
        sa.Column('parent', sa.BIGINT, sa.ForeignKey("account.id"), nullable=True, default=None),
        sa.Column('operate', sa.BOOLEAN, nullable=False, default=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )
    op.create_index('code_account', 'account', ['code'])

    op.create_table(
        "tag",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('name', sa.VARCHAR(200), nullable=False, unique=True),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )
    op.create_index('name_tag', 'tag', ['name'])

    op.create_table(
        "record",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement="auto"),
        sa.Column('anotation', sa.VARCHAR(200), nullable=False),
        sa.Column('date', sa.DATE, nullable=False),
        sa.Column('amount', sa.BIGINT, nullable=False),
        sa.Column('account_debit', sa.BIGINT, sa.ForeignKey("account.id"), nullable=False),
        sa.Column('account_credit', sa.BIGINT, sa.ForeignKey("account.id"), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "tag_record",
        sa.Column('tag', sa.BIGINT, sa.ForeignKey("tag.id"), primary_key=True),
        sa.Column('record', sa.BIGINT, sa.ForeignKey("record.id"), primary_key=True),
    )

    op.create_index('id_tag', 'tag_record', ['tag'])

def downgrade() -> None:
    op.drop_table("tag_record")
    op.drop_table("record")
    op.drop_table("tag")
    op.drop_table("account")
    op.drop_table("exchange")
    op.drop_table("currency")
    op.drop_table("account_type")
    op.drop_table("operation_type")
