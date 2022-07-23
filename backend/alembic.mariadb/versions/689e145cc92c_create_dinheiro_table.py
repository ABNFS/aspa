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
    tipo_partida = op.create_table(
        "tipo_partidas_dobradas",
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('nome', sa.VARCHAR(20), nullable=False),
        sa.Column('sigla', sa.CHAR(1), nullable=False)
    )

    tipo_conta = op.create_table(
        "tipo_conta",
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('nome', sa.VARCHAR(26), nullable=False),
        sa.Column('sigla', sa.CHAR(3), nullable=False),
        sa.Column('tipo_saldo', sa.BIGINT, sa.ForeignKey("tipo_partidas_dobradas.id"), nullable=False),
    )

    op.create_table(
        "moeda",
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('nome', sa.VARCHAR(200), nullable=False),
        sa.Column('sigla', sa.VARCHAR(5), nullable=False),
        sa.Column('taxa_cambio', sa.BIGINT, nullable=False)
    )

    op.create_table(
        "conta",
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('codigo', sa.VARCHAR(20), nullable=False),
        sa.Column('nome', sa.VARCHAR(200), nullable=False),
        sa.Column('saldo', sa.BIGINT, nullable=False),
        sa.Column('sigla', sa.VARCHAR(5), nullable=False),
        sa.Column('moeda_id', sa.BIGINT, sa.ForeignKey("moeda.id"), nullable=False),
        sa.Column('tipo_conta', sa.BIGINT, sa.ForeignKey("tipo_conta.id"), nullable=False)
    )

    op.create_table(
        "movimento",
        sa.Column('id', sa.BIGINT, primary_key=True),
        sa.Column('anotacao', sa.VARCHAR(200), nullable=False),
        sa.Column('data', sa.TIMESTAMP, nullable=False),
        sa.Column('valor', sa.BIGINT, nullable=False),
        sa.Column('contaDebito', sa.BIGINT, sa.ForeignKey("conta.id"), nullable=False),
        sa.Column('contaCredito', sa.BIGINT, sa.ForeignKey("conta.id"), nullable=False)
    )

    op.bulk_insert(
        tipo_partida,
        [
            {"id": 1, "nome": 'Débito', "sigla": 'D'},
            {"id": 2, "nome": 'Crédito', "sigla": 'C'}
        ]
    )

    op.bulk_insert(
        tipo_conta,
        [
            {"id": 1, "nome": 'Patrimônio', "sigla": 'PL', "tipo_saldo": 2},
            {"id": 2, "nome": 'Ativo', "sigla": 'ATV', "tipo_saldo": 1},
            {"id": 3, "nome": 'Exegível', "sigla": 'EXE', "tipo_saldo": 2},
            {"id": 4, "nome": 'Receitas', "sigla": 'REC', "tipo_saldo": 2},
            {"id": 5, "nome": 'Despesas', "sigla": 'DES', "tipo_saldo": 1},
            {"id": 6, "nome": 'Conta Retificadora Ativo', "sigla": 'CRA', "tipo_saldo": 2},
            {"id": 7, "nome": 'Conta Retificadora Passivo', "sigla": 'CRP', "tipo_saldo": 1}
        ]
    )

def downgrade() -> None:
    op.drop_table("movimento")
    op.drop_table("conta")
    op.drop_table("moeda")
    op.drop_table("tipo_conta")
    op.drop_table("tipo_partidas_dobradas")
