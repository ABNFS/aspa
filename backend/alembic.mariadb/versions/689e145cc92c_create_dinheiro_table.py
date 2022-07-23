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
        "tipo_partida_dobrada",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('nome', sa.VARCHAR(20), nullable=False),
        sa.Column('sigla', sa.CHAR(1), nullable=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        tipo_partida,
        [
            {"id": 1, "nome": 'Débito', "sigla": 'D'},
            {"id": 2, "nome": 'Crédito', "sigla": 'C'}
        ]
    )

    tipo_conta = op.create_table(
        "tipo_conta",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('nome', sa.VARCHAR(26), nullable=False),
        sa.Column('sigla', sa.CHAR(3), nullable=False),
        sa.Column('tipo_saldo', sa.BIGINT, sa.ForeignKey("tipo_partida_dobrada.id"), nullable=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        tipo_conta,
        [
            {"id": 3, "nome": 'Patrimônio', "sigla": 'PL', "tipo_saldo": 2},
            {"id": 4, "nome": 'Ativo', "sigla": 'ATV', "tipo_saldo": 1},
            {"id": 5, "nome": 'Exegível', "sigla": 'EXE', "tipo_saldo": 2},
            {"id": 6, "nome": 'Receitas', "sigla": 'REC', "tipo_saldo": 2},
            {"id": 7, "nome": 'Despesas', "sigla": 'DES', "tipo_saldo": 1},
            {"id": 8, "nome": 'Conta Retificadora Ativo', "sigla": 'CRA', "tipo_saldo": 2},
            {"id": 9, "nome": 'Conta Retificadora Passivo', "sigla": 'CRP', "tipo_saldo": 1}
        ]
    )

    moeda = op.create_table(
        "moeda",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('nome', sa.VARCHAR(200), nullable=False),
        sa.Column('sigla', sa.VARCHAR(5), nullable=False),
        sa.Column('padrao', sa.BOOLEAN, default=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        moeda,
        [
            {"id": 10, "nome": 'Real', "sigla": 'R$', "padrao": True}
        ]
    )

    op.create_table(
        "cambio",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('moeda_padrao', sa.BIGINT, sa.ForeignKey("moeda.id"), default=10),
        sa.Column('moeda_comprada', sa.BIGINT, sa.ForeignKey("moeda.id"), nullable=False),
        sa.Column('data', sa.DATE, nullable=False),
        sa.Column('taxa', sa.BIGINT, nullable=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )

    conta = op.create_table(
        "conta",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('codigo', sa.VARCHAR(20), nullable=False),
        sa.Column('nome', sa.VARCHAR(200), nullable=False),
        sa.Column('saldo', sa.BIGINT, nullable=False, default=0),
        sa.Column('sigla', sa.VARCHAR(5), nullable=True, default=None),
        sa.Column('moeda', sa.BIGINT, sa.ForeignKey("moeda.id"), nullable=False, default=10),
        sa.Column('tipo_conta', sa.BIGINT, sa.ForeignKey("tipo_conta.id"), nullable=False),
        sa.Column('pai', sa.BIGINT, sa.ForeignKey("conta.id"), nullable=True, default=None),
        sa.Column('pode_movimentar', sa.BOOLEAN, nullable=False, default=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        conta,
        [
            {"id": 11, "codigo": '1.0.0.0', "nome": 'Ativo', "saldo": 0, "sigla": 'ATV', "moeda": 10,
             "tipo_conta": 4, "pai": None, "pode_movimentar": False},
            {"id": 12, "codigo": '2.0.0.0', "nome": 'Passivo Exegível', "saldo": 0, "sigla": 'EXE', "moeda": 10,
             "tipo_conta": 5, "pai": None, "pode_movimentar": False},
            {"id": 13, "codigo": '3.0.0.0', "nome": 'Patrimônio Líquido', "saldo": 0, "sigla": 'PL', "moeda": 10,
             "tipo_conta": 3,"pai": None, "pode_movimentar": False},
            {"id": 14, "codigo": '4.0.0.0', "nome": 'Pagamentos', "saldo": 0, "sigla": 'PGMTO', "moeda": 10,
             "tipo_conta": 7,"pai": None, "pode_movimentar": False},
            {"id": 15, "codigo": '5.0.0.0', "nome": 'Recebimentos', "saldo": 0, "sigla": 'REC', "moeda": 10,
             "tipo_conta": 6,"pai": None, "pode_movimentar": False},
            {"id": 172, "codigo": '6.0.0.0', "nome": 'Ajustes Ativos', "saldo": 0, "sigla": 'AA', "moeda": 10,
             "tipo_conta": 8,"pai": None, "pode_movimentar": False},
            {"id": 173, "codigo": '7.0.0.0', "nome": 'Ajustes Passivos', "saldo": 0, "sigla": 'AP', "moeda": 10,
             "tipo_conta": 9,"pai": None, "pode_movimentar": False}
        ]
    )
    
    op.bulk_insert(
        conta,
        [
            {"id": 16, "codigo": '1.1.0.0', "nome": 'Financeiro', "tipo_conta": 4, "pai": 11},
            {"id": 17, "codigo": '1.2.0.0', "nome": 'Bens', "tipo_conta": 4, "pai": 11},
            {"id": 18, "codigo": '1.3.0.0', "nome": 'Recebíveis', "tipo_conta": 4, "pai": 11},

            {"id": 20, "codigo": '1.1.2.0', "nome": 'Contas à vista', "tipo_conta": 4, "pai": 16},
            {"id": 38, "codigo": '1.1.3.0', "nome": 'Investimenos à vista', "tipo_conta": 4, "pai": 16},

            {"id": 21, "codigo": '1.2.1.0', "nome": 'Móveis', "tipo_conta": 4, "pai": 17},
            {"id": 22, "codigo": '1.2.2.0', "nome": 'Imóveis', "tipo_conta": 4, "pai": 17},
            {"id": 23, "codigo": '1.2.3.0', "nome": 'Intangíveis', "tipo_conta": 4, "pai": 17},

            {"id": 24, "codigo": '1.3.1.0', "nome": 'Salário', "tipo_conta": 4, "pai": 18},
            {"id": 25, "codigo": '1.3.2.0', "nome": 'Férias', "tipo_conta": 4, "pai": 18},
            {"id": 26, "codigo": '1.3.3.0', "nome": 'Décimo-terceiro', "tipo_conta": 4, "pai": 18},
        ]
    )
    op.bulk_insert(
        conta,
        [

            {"id": 19, "codigo": '1.1.1.0', "nome": 'Dinheiro em espécie', "tipo_conta": 4, "pai": 16,
             "pode_movimentar": True},
            {"id": 27, "codigo": '1.3.4.0', "nome": 'Diária', "tipo_conta": 4, "pai": 18,
             "pode_movimentar": True},
            {"id": 28, "codigo": '1.3.5.0', "nome": 'Honorário', "tipo_conta": 4, "pai": 18,
             "pode_movimentar": True},
            {"id": 29, "codigo": '1.3.6.0', "nome": 'Serviços Prestado', "tipo_conta": 4, "pai": 18,
             "pode_movimentar": True},

            {"id": 30, "codigo": '1.1.2.1', "nome": 'Banco do Brasil', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 31, "codigo": '1.1.2.2', "nome": 'Nubank', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 32, "codigo": '1.1.2.3', "nome": 'Caixa', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 33, "codigo": '1.1.2.4', "nome": 'Santander', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 34, "codigo": '1.1.2.5', "nome": 'Mercado Pago', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 35, "codigo": '1.1.2.6', "nome": 'Bradesco', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 36, "codigo": '1.1.2.7', "nome": 'Inter', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},
            {"id": 37, "codigo": '1.1.2.8', "nome": 'C6', "tipo_conta": 4, "pai": 20,
             "pode_movimentar": True},

            {"id": 39, "codigo": '1.2.1.1', "nome": 'Notebook', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},
            {"id": 40, "codigo": '1.2.1.2', "nome": 'Carro', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},
            {"id": 41, "codigo": '1.2.1.3', "nome": 'Moto', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},
            {"id": 42, "codigo": '1.2.1.4', "nome": 'Celular', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},
            {"id": 43, "codigo": '1.2.1.5', "nome": 'Tablet', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},
            {"id": 44, "codigo": '1.2.1.6', "nome": 'Desktop', "tipo_conta": 4, "pai": 21,
             "pode_movimentar": True},

            {"id": 45, "codigo": '1.2.2.1', "nome": 'Lote', "tipo_conta": 4, "pai": 22, "pode_movimentar": True},
            {"id": 46, "codigo": '1.2.2.2', "nome": 'Casa', "tipo_conta": 4, "pai": 22, "pode_movimentar": True},

            {"id": 47, "codigo": '1.2.3.1', "nome": 'Participação em empresas', "tipo_conta": 4, "pai": 23,
             "pode_movimentar": True},

            {"id": 48, "codigo": '1.1.3.1', "nome": 'Ações', "tipo_conta": 4, "pai": 48,
             "pode_movimentar": True},
            {"id": 49, "codigo": '1.1.3.2', "nome": 'Fundos Investimento', "tipo_conta": 4, "pai": 48,
             "pode_movimentar": True},

            {"id": 50, "codigo": '1.3.1.1', "nome": 'TRE', "tipo_conta": 4, "pai": 24, "pode_movimentar": True},
            {"id": 51, "codigo": '1.3.1.2', "nome": 'Unitins', "tipo_conta": 4, "pai": 24,
             "pode_movimentar": True},
            {"id": 52, "codigo": '1.3.1.3', "nome": 'Unest', "tipo_conta": 4, "pai": 24, "pode_movimentar": True},

            {"id": 53, "codigo": '1.3.2.1', "nome": 'TRE', "tipo_conta": 4, "pai": 25, "pode_movimentar": True},
            {"id": 54, "codigo": '1.3.2.2', "nome": 'Unitins', "tipo_conta": 4, "pai": 25,
             "pode_movimentar": True},
            {"id": 55, "codigo": '1.3.2.3', "nome": 'Unest', "tipo_conta": 4, "pai": 25, "pode_movimentar": True},

            {"id": 56, "codigo": '1.3.3.1', "nome": 'TRE', "tipo_conta": 4, "pai": 26, "pode_movimentar": True},
            {"id": 57, "codigo": '1.3.3.2', "nome": 'Unitins', "tipo_conta": 4, "pai": 26,
             "pode_movimentar": True},
            {"id": 58, "codigo": '1.3.3.3', "nome": 'Unest', "tipo_conta": 4, "pai": 26, "pode_movimentar": True},
        ]
    )

    op.bulk_insert(
        conta,
        [
            {"id": 59, "codigo": '2.1.0.0', "nome": 'Financeiro', "tipo_conta": 5, "pai": 12},
            {"id": 60, "codigo": '2.2.0.0', "nome": 'Contas Serviço Público', "tipo_conta": 5, "pai": 12},
            {"id": 61, "codigo": '2.3.0.0', "nome": 'Impostos', "tipo_conta": 5, "pai": 12},
            {"id": 62, "codigo": '2.4.0.0', "nome": 'Dívidas', "tipo_conta": 5, "pai": 12},

            {"id": 63, "codigo": '2.1.1.0', "nome": 'Bancos', "tipo_conta": 5, "pai": 59},
            {"id": 64, "codigo": '2.1.2.0', "nome": 'Cartões de Crédito', "tipo_conta": 5, "pai": 59},
            {"id": 65, "codigo": '2.1.3.0', "nome": 'Empréstimos', "tipo_conta": 5, "pai": 59},
            {"id": 66, "codigo": '2.1.4.0', "nome": 'Cheque Especial', "tipo_conta": 5, "pai": 59},
        ]
    )

    op.bulk_insert(
        conta,
        [
            {"id": 67, "codigo": '2.2.1.0', "nome": 'Água', "tipo_conta": 5, "pai": 60, "pode_movimentar": True},
            {"id": 68, "codigo": '2.2.2.0', "nome": 'Energia', "tipo_conta": 5, "pai": 60, "pode_movimentar": True},
            {"id": 69, "codigo": '2.2.3.0', "nome": 'Gás', "tipo_conta": 5, "pai": 60, "pode_movimentar": True},

            {"id": 70, "codigo": '2.3.1.0', "nome": 'Imposto de Renda', "tipo_conta": 5, "pai": 61,
             "pode_movimentar": True},
            {"id": 71, "codigo": '2.3.2.0', "nome": 'IOF', "tipo_conta": 5, "pai": 61, "pode_movimentar": True},

            {"id": 72, "codigo": '2.3.1.0', "nome": 'Não negociadas', "tipo_conta": 5, "pai": 62,
             "pode_movimentar": True},
            {"id": 73, "codigo": '2.3.2.0', "nome": 'Negociadas', "tipo_conta": 5, "pai": 62, "pode_movimentar": True},
            {"id": 74, "codigo": '2.3.3.0', "nome": 'Sem juros', "tipo_conta": 5, "pai": 62, "pode_movimentar": True},

            {"id": 75, "codigo": '2.1.1.1', "nome": 'Taxas', "tipo_conta": 5, "pai": 63, "pode_movimentar": True},
            {"id": 76, "codigo": '2.1.1.2', "nome": 'Serviços', "tipo_conta": 5, "pai": 63, "pode_movimentar": True},
            {"id": 77, "codigo": '2.1.1.3', "nome": 'Título Capitalização', "tipo_conta": 5, "pai": 63,
             "pode_movimentar": True},
            {"id": 78, "codigo": '2.1.1.4', "nome": 'Previdência', "tipo_conta": 5, "pai": 63, "pode_movimentar": True},

            {"id": 79, "codigo": '2.1.2.1', "nome": 'Nubank', "tipo_conta": 5, "pai": 64, "pode_movimentar": True},
            {"id": 80, "codigo": '2.1.2.2', "nome": 'Mercado Pago', "tipo_conta": 5, "pai": 64,
             "pode_movimentar": True},
            {"id": 81, "codigo": '2.1.2.3', "nome": 'Santander', "tipo_conta": 5, "pai": 64, "pode_movimentar": True},

            {"id": 82, "codigo": '2.1.3.1', "nome": 'Nubank', "tipo_conta": 5, "pai": 65, "pode_movimentar": True},
            {"id": 83, "codigo": '2.1.3.2', "nome": 'Santander', "tipo_conta": 5, "pai": 65, "pode_movimentar": True},
            {"id": 84, "codigo": '2.1.3.3', "nome": 'Mercado Pago', "tipo_conta": 5, "pai": 65,
             "pode_movimentar": True},
            {"id": 85, "codigo": '2.1.3.4', "nome": 'Bradesco', "tipo_conta": 5, "pai": 65, "pode_movimentar": True},
            {"id": 86, "codigo": '2.1.3.5', "nome": 'Financimaneto Carro', "tipo_conta": 5, "pai": 65,
             "pode_movimentar": True},
            {"id": 87, "codigo": '2.1.3.6', "nome": 'Financimaneto Energia Solar', "tipo_conta": 5, "pai": 65,
             "pode_movimentar": True},
            {"id": 88, "codigo": '2.1.3.7', "nome": 'Consignado', "tipo_conta": 5, "pai": 65, "pode_movimentar": True},

            {"id": 89, "codigo": '2.1.4.1', "nome": 'Caixa', "tipo_conta": 5, "pai": 67, "pode_movimentar": True},

            {"id": 90, "codigo": '3.1.0.0', "nome": 'Resultado', "tipo_conta": 3, "pai": 13, "pode_movimentar": True}
        ]
    )

    op.bulk_insert(
        conta,
        [
            {"id": 91, "codigo": '4.1.0.0', "nome": 'Pagamento', "tipo_conta": 7, "pai": 14},
            {"id": 92, "codigo": '5.1.0.0', "nome": 'Recebimento', "tipo_conta": 6, "pai": 15},

            {"id": 93, "codigo": '4.1.1.0', "nome": 'Casa', "tipo_conta": 7, "pai": 91},
            {"id": 94, "codigo": '4.1.2.0', "nome": 'Locomoção', "tipo_conta": 7, "pai": 91},
            {"id": 95, "codigo": '4.1.4.0', "nome": 'Compras', "tipo_conta": 7, "pai": 91},
            {"id": 96, "codigo": '4.1.5.0', "nome": 'Diversão e Bem estar', "tipo_conta": 7, "pai": 91},
            {"id": 98, "codigo": '4.1.6.0', "nome": 'Estudo', "tipo_conta": 7, "pai": 91},
            {"id": 99, "codigo": '4.1.7.0', "nome": 'Roupa e beleza', "tipo_conta": 7, "pai": 91},
            {"id": 100, "codigo": '4.1.8.0', "nome": 'Animais de estimação', "tipo_conta": 7, "pai": 91},
            {"id": 101, "codigo": '4.1.9.0', "nome": 'Doação', "tipo_conta": 7, "pai": 91},
            {"id": 144, "codigo": '4.1.10.0', "nome": 'Softwares', "tipo_conta": 7, "pai": 91},
            {"id": 115, "codigo": '4.1.11.0', "nome": 'Alimentação', "tipo_conta": 7, "pai": 91},
            {"id": 131, "codigo": '4.1.12.0', "nome": 'Bens', "tipo_conta": 7, "pai": 91},
            {"id": 160, "codigo": '4.1.13.0', "nome": 'Financeiro', "tipo_conta": 7, "pai": 91},

            {"id": 166, "codigo": '5.1.1.0', "nome": 'Salários', "tipo_conta": 6, "pai": 92},
            {"id": 167, "codigo": '5.1.2.0', "nome": 'Honorários', "tipo_conta": 6, "pai": 92},
            {"id": 168, "codigo": '5.1.3.0', "nome": 'Serviços', "tipo_conta": 6, "pai": 92},
            {"id": 169, "codigo": '5.1.4.0', "nome": 'Vendas', "tipo_conta": 6, "pai": 92},
            {"id": 170, "codigo": '5.1.5.0', "nome": 'Rendimentos Financeiros', "tipo_conta": 6, "pai": 92},
            {"id": 171, "codigo": '5.1.6.0', "nome": 'Lucros', "tipo_conta": 6, "pai": 92}
        ]
    )

    op.bulk_insert(
        conta,
        [
            {"id": 102, "codigo": '4.1.1.1', "nome": 'Aluguel', "tipo_conta": 7, "pai": 93, "pode_movimentar": True},
            {"id": 103, "codigo": '4.1.1.2', "nome": 'Diárias', "tipo_conta": 7, "pai": 93, "pode_movimentar": True},
            {"id": 104, "codigo": '4.1.1.3', "nome": 'Manutenção Casa', "tipo_conta": 7, "pai": 93,
             "pode_movimentar": True},
            {"id": 105, "codigo": '4.1.1.4', "nome": 'Segurança Casa', "tipo_conta": 7, "pai": 93,
             "pode_movimentar": True},

            {"id": 106, "codigo": '4.1.2.1', "nome": 'Gasolina', "tipo_conta": 7, "pai": 94, "pode_movimentar": True},
            {"id": 107, "codigo": '4.1.2.2', "nome": 'Passagens', "tipo_conta": 7, "pai": 94, "pode_movimentar": True},
            {"id": 108, "codigo": '4.1.2.3', "nome": 'Diárias Hotel', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 109, "codigo": '4.1.2.4', "nome": 'Aluguel Carro', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 110, "codigo": '4.1.2.5', "nome": 'Manutenção veículo', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 111, "codigo": '4.1.2.6', "nome": 'Seguro Veículo', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 112, "codigo": '4.1.2.7', "nome": 'Seguro Viagem', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 113, "codigo": '4.1.2.8', "nome": 'Taxi/Aplicativo', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},
            {"id": 114, "codigo": '4.1.2.9', "nome": 'Entregador/Aplicativo', "tipo_conta": 7, "pai": 94,
             "pode_movimentar": True},

            {"id": 116, "codigo": '4.1.11.1', "nome": 'Restaurante', "tipo_conta": 7, "pai": 115,
             "pode_movimentar": True},
            {"id": 117, "codigo": '4.1.11.2', "nome": 'Entrega', "tipo_conta": 7, "pai": 115,
             "pode_movimentar": True},
            {"id": 118, "codigo": '4.1.11.3', "nome": 'Encomenda', "tipo_conta": 7, "pai": 115,
             "pode_movimentar": True},
            {"id": 119, "codigo": '4.1.11.4', "nome": 'Lanche', "tipo_conta": 7, "pai": 115,
             "pode_movimentar": True},
            {"id": 120, "codigo": '4.1.11.5', "nome": 'Doces', "tipo_conta": 7, "pai": 115,
             "pode_movimentar": True},

            {"id": 179, "codigo": '4.1.4.1', "nome": 'Mercadinho', "tipo_conta": 7, "pai": 95, "pode_movimentar": True},
            {"id": 180, "codigo": '4.1.4.2', "nome": 'Farmácia', "tipo_conta": 7, "pai": 95, "pode_movimentar": True},
            {"id": 181, "codigo": '4.1.4.3', "nome": 'Atacarejo', "tipo_conta": 7, "pai": 95, "pode_movimentar": True},
            {"id": 182, "codigo": '4.1.4.4', "nome": 'Livraria', "tipo_conta": 7, "pai": 95, "pode_movimentar": True},
            {"id": 183, "codigo": '4.1.4.5', "nome": 'Bazar', "tipo_conta": 7, "pai": 95, "pode_movimentar": True},
            {"id": 184, "codigo": '4.1.4.6', "nome": 'Supermercado', "tipo_conta": 7, "pai": 95,
             "pode_movimentar": True},

            {"id": 121, "codigo": '4.1.5.1', "nome": 'Cachaçada', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 122, "codigo": '4.1.5.2', "nome": 'Cinema', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 123, "codigo": '4.1.5.3', "nome": 'Stream', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 124, "codigo": '4.1.5.4', "nome": 'Livros e Gibis', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 125, "codigo": '4.1.5.5', "nome": 'Acampamento', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 126, "codigo": '4.1.5.6', "nome": 'Clube', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 136, "codigo": '4.1.5.7', "nome": 'RPG', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},
            {"id": 150, "codigo": '4.1.5.8', "nome": 'Jogos', "tipo_conta": 7, "pai": 96,
             "pode_movimentar": True},

            {"id": 127, "codigo": '4.1.6.1', "nome": 'Escola/Faculdade', "tipo_conta": 7, "pai": 98,
             "pode_movimentar": True},
            {"id": 128, "codigo": '4.1.6.2', "nome": 'Cursos', "tipo_conta": 7, "pai": 98,
             "pode_movimentar": True},
            {"id": 129, "codigo": '4.1.6.3', "nome": 'Livros Didáticos', "tipo_conta": 7, "pai": 98,
             "pode_movimentar": True},
            {"id": 130, "codigo": '4.1.6.4', "nome": 'Material de Escritório', "tipo_conta": 7, "pai": 98,
             "pode_movimentar": True},

            {"id": 132, "codigo": '4.1.7.1', "nome": 'Roupas', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},
            {"id": 133, "codigo": '4.1.7.2', "nome": 'Calçados', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},
            {"id": 134, "codigo": '4.1.7.3', "nome": 'Lingerie', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},
            {"id": 135, "codigo": '4.1.7.4', "nome": 'Fantasia', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},
            {"id": 137, "codigo": '4.1.7.5', "nome": 'Corte Cabelo', "tipo_conta": 7, "pai": 99,
             "pode_movimentar": True},
            {"id": 138, "codigo": '4.1.7.6', "nome": 'Manicure', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},
            {"id": 139, "codigo": '4.1.7.7', "nome": 'Depilação', "tipo_conta": 7, "pai": 99, "pode_movimentar": True},

            {"id": 140, "codigo": '4.1.8.1', "nome": 'Ração', "tipo_conta": 7, "pai": 100, "pode_movimentar": True},
            {"id": 141, "codigo": '4.1.8.2', "nome": 'Veterinário', "tipo_conta": 7, "pai": 100,
             "pode_movimentar": True},
            {"id": 142, "codigo": '4.1.8.3', "nome": 'Salão', "tipo_conta": 7, "pai": 100, "pode_movimentar": True},
            {"id": 143, "codigo": '4.1.8.4', "nome": 'Assessórios', "tipo_conta": 7, "pai": 100,
             "pode_movimentar": True},

            {"id": 145, "codigo": '4.1.9.1', "nome": 'Animais', "tipo_conta": 7, "pai": 101, "pode_movimentar": True},
            {"id": 146, "codigo": '4.1.9.2', "nome": 'Artistas', "tipo_conta": 7, "pai": 101, "pode_movimentar": True},
            {"id": 147, "codigo": '4.1.9.3', "nome": 'Cientístas', "tipo_conta": 7, "pai": 101,
             "pode_movimentar": True},
            {"id": 148, "codigo": '4.1.9.4', "nome": 'Crianças', "tipo_conta": 7, "pai": 101, "pode_movimentar": True},
            {"id": 149, "codigo": '4.1.9.5', "nome": 'Pessoas na Rua', "tipo_conta": 7, "pai": 101,
             "pode_movimentar": True},

            {"id": 151, "codigo": '4.1.10.1', "nome": 'Cloud Armazenamento', "tipo_conta": 7, "pai": 144,
             "pode_movimentar": True},
            {"id": 152, "codigo": '4.1.10.2', "nome": 'Servidores', "tipo_conta": 7, "pai": 144,
             "pode_movimentar": True},
            {"id": 153, "codigo": '4.1.10.3', "nome": 'Desenvolvimento', "tipo_conta": 7, "pai": 144,
             "pode_movimentar": True},
            {"id": 154, "codigo": '4.1.10.4', "nome": 'Arte', "tipo_conta": 7, "pai": 144, "pode_movimentar": True},
            {"id": 155, "codigo": '4.1.10.5', "nome": 'Segurança', "tipo_conta": 7, "pai": 144,
             "pode_movimentar": True},

            {"id": 156, "codigo": '4.1.12.1', "nome": 'Móveis', "tipo_conta": 7, "pai": 131, "pode_movimentar": True},
            {"id": 157, "codigo": '4.1.12.2', "nome": 'Veículos', "tipo_conta": 7, "pai": 131, "pode_movimentar": True},
            {"id": 158, "codigo": '4.1.12.3', "nome": 'Eletrônicos', "tipo_conta": 7, "pai": 131,
             "pode_movimentar": True},
            {"id": 159, "codigo": '4.1.12.4', "nome": 'Imóveis', "tipo_conta": 7, "pai": 131, "pode_movimentar": True},

            {"id": 161, "codigo": '4.1.13.1', "nome": 'Previdência Privada', "tipo_conta": 7, "pai": 160,
             "pode_movimentar": True},
            {"id": 162, "codigo": '4.1.13.2', "nome": 'Fundos de Ação', "tipo_conta": 7, "pai": 160,
             "pode_movimentar": True},
            {"id": 163, "codigo": '4.1.13.3', "nome": 'Juros', "tipo_conta": 7, "pai": 160, "pode_movimentar": True},
            {"id": 164, "codigo": '4.1.13.4', "nome": 'Empréstimos', "tipo_conta": 7, "pai": 160,
             "pode_movimentar": True},
            {"id": 165, "codigo": '4.1.13.5', "nome": 'Dívidas', "tipo_conta": 7, "pai": 160, "pode_movimentar": True},

            {"id": 174, "codigo": '6.1.0.0', "nome": 'Saldo Inicial', "tipo_conta": 8, "pai": 172,
             "pode_movimentar": True},
            {"id": 175, "codigo": '6.2.0.0', "nome": 'Extorno', "tipo_conta": 8, "pai": 172, "pode_movimentar": True},
            {"id": 176, "codigo": '6.3.0.0', "nome": 'Depreciação', "tipo_conta": 8, "pai": 172,
             "pode_movimentar": True},

            {"id": 177, "codigo": '7.1.0.0', "nome": 'Saldo Inicial', "tipo_conta": 9, "pai": 173,
             "pode_movimentar": True},
            {"id": 178, "codigo": '7.2.0.0', "nome": 'Extorno', "tipo_conta": 9, "pai": 173, "pode_movimentar": True},

        ]
    )
    op.create_table(
        "movimento",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('anotacao', sa.VARCHAR(200), nullable=False),
        sa.Column('data', sa.DATE, nullable=False),
        sa.Column('valor', sa.BIGINT, nullable=False),
        sa.Column('contaDebito', sa.BIGINT, sa.ForeignKey("conta.id"), nullable=False),
        sa.Column('contaCredito', sa.BIGINT, sa.ForeignKey("conta.id"), nullable=False),
        sa.Column('excluido', sa.BOOLEAN, default=False)
    )


def downgrade() -> None:
    op.drop_table("movimento")
    op.drop_table("conta")
    op.drop_table("cambio")
    op.drop_table("moeda")
    op.drop_table("tipo_conta")
    op.drop_table("tipo_partida_dobrada")
