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

    op_type = op.create_table(
        "operation_type",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('name', sa.VARCHAR(20), nullable=False),
        sa.Column('alias', sa.CHAR(1), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        op_type,
        [
            {"id": 1, "name": 'Débito', "alias": 'D'},
            {"id": 2, "name": 'Crédito', "alias": 'C'}
        ]
    )

    account_type = op.create_table(
        "account_type",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('name', sa.VARCHAR(26), nullable=False),
        sa.Column('alias', sa.CHAR(3), nullable=False),
        sa.Column('operation', sa.BIGINT, sa.ForeignKey("operation_type.id"), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        account_type,
        [
            {"id": 3, "name": 'Patrimônio', "alias": 'PL', "operation": 2},
            {"id": 4, "name": 'Ativo', "alias": 'ATV', "operation": 1},
            {"id": 5, "name": 'Exegível', "alias": 'EXE', "operation": 2},
            {"id": 6, "name": 'Receitas', "alias": 'REC', "operation": 2},
            {"id": 7, "name": 'Despesas', "alias": 'DES', "operation": 1},
            {"id": 8, "name": 'Conta Retificadora Ativo', "alias": 'CRA', "operation": 2},
            {"id": 9, "name": 'Conta Retificadora Passivo', "alias": 'CRP', "operation": 1}
        ]
    )

    currency = op.create_table(
        "currency",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('name', sa.VARCHAR(200), nullable=False),
        sa.Column('alias', sa.VARCHAR(5), nullable=False),
        sa.Column('default', sa.BOOLEAN, default=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        currency,
        [
            {"id": 10, "name": 'Real', "alias": 'R$', "default": True}
        ]
    )

    op.create_table(
        "exchange",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('currency_default', sa.BIGINT, sa.ForeignKey("currency.id"), default=10),
        sa.Column('currency_buy', sa.BIGINT, sa.ForeignKey("currency.id"), nullable=False),
        sa.Column('date', sa.DATE, nullable=False),
        sa.Column('rate', sa.BIGINT, nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    account = op.create_table(
        "account",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('code', sa.VARCHAR(20), nullable=False),
        sa.Column('name', sa.VARCHAR(200), nullable=False),
        sa.Column('balance', sa.BIGINT, nullable=False, default=0),
        sa.Column('alias', sa.VARCHAR(5), nullable=True, default=None),
        sa.Column('currency', sa.BIGINT, sa.ForeignKey("currency.id"), nullable=False, default=10),
        sa.Column('account_type', sa.BIGINT, sa.ForeignKey("account_type.id"), nullable=False),
        sa.Column('parent', sa.BIGINT, sa.ForeignKey("account.id"), nullable=True, default=None),
        sa.Column('operate', sa.BOOLEAN, nullable=False, default=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.bulk_insert(
        account,
        [
            {"id": 11, "code": '1.0.0.0', "name": 'Ativo', "balance": 0, "alias": 'ATV', "currency": 10,
             "account_type": 4, "parent": None, "operate": False},
            {"id": 12, "code": '2.0.0.0', "name": 'Passivo Exegível', "balance": 0, "alias": 'EXE', "currency": 10,
             "account_type": 5, "parent": None, "operate": False},
            {"id": 13, "code": '3.0.0.0', "name": 'Patrimônio Líquido', "balance": 0, "alias": 'PL', "currency": 10,
             "account_type": 3,"parent": None, "operate": False},
            {"id": 14, "code": '4.0.0.0', "name": 'Pagamentos', "balance": 0, "alias": 'PGMTO', "currency": 10,
             "account_type": 7,"parent": None, "operate": False},
            {"id": 15, "code": '5.0.0.0', "name": 'Recebimentos', "balance": 0, "alias": 'REC', "currency": 10,
             "account_type": 6,"parent": None, "operate": False},
            {"id": 172, "code": '6.0.0.0', "name": 'Ajustes Ativos', "balance": 0, "alias": 'AA', "currency": 10,
             "account_type": 8,"parent": None, "operate": False},
            {"id": 173, "code": '7.0.0.0', "name": 'Ajustes Passivos', "balance": 0, "alias": 'AP', "currency": 10,
             "account_type": 9,"parent": None, "operate": False}
        ]
    )
    
    op.bulk_insert(
        account,
        [
            {"id": 16, "code": '1.1.0.0', "name": 'Financeiro', "account_type": 4, "parent": 11},
            {"id": 17, "code": '1.2.0.0', "name": 'Bens', "account_type": 4, "parent": 11},
            {"id": 18, "code": '1.3.0.0', "name": 'Recebíveis', "account_type": 4, "parent": 11},

            {"id": 20, "code": '1.1.2.0', "name": 'accounts à vista', "account_type": 4, "parent": 16},
            {"id": 38, "code": '1.1.3.0', "name": 'Investimenos à vista', "account_type": 4, "parent": 16},

            {"id": 21, "code": '1.2.1.0', "name": 'Móveis', "account_type": 4, "parent": 17},
            {"id": 22, "code": '1.2.2.0', "name": 'Imóveis', "account_type": 4, "parent": 17},
            {"id": 23, "code": '1.2.3.0', "name": 'Intangíveis', "account_type": 4, "parent": 17},

            {"id": 24, "code": '1.3.1.0', "name": 'Salário', "account_type": 4, "parent": 18},
            {"id": 25, "code": '1.3.2.0', "name": 'Férias', "account_type": 4, "parent": 18},
            {"id": 26, "code": '1.3.3.0', "name": 'Décimo-terceiro', "account_type": 4, "parent": 18},
        ]
    )
    op.bulk_insert(
        account,
        [

            {"id": 19, "code": '1.1.1.0', "name": 'Dinheiro em espécie', "account_type": 4, "parent": 16,
             "operate": True},
            {"id": 27, "code": '1.3.4.0', "name": 'Diária', "account_type": 4, "parent": 18,
             "operate": True},
            {"id": 28, "code": '1.3.5.0', "name": 'Honorário', "account_type": 4, "parent": 18,
             "operate": True},
            {"id": 29, "code": '1.3.6.0', "name": 'Serviços Prestado', "account_type": 4, "parent": 18,
             "operate": True},

            {"id": 30, "code": '1.1.2.1', "name": 'Banco do Brasil', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 31, "code": '1.1.2.2', "name": 'Nubank', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 32, "code": '1.1.2.3', "name": 'Caixa', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 33, "code": '1.1.2.4', "name": 'Santander', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 34, "code": '1.1.2.5', "name": 'Mercado Pago', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 35, "code": '1.1.2.6', "name": 'Bradesco', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 36, "code": '1.1.2.7', "name": 'Inter', "account_type": 4, "parent": 20,
             "operate": True},
            {"id": 37, "code": '1.1.2.8', "name": 'C6', "account_type": 4, "parent": 20,
             "operate": True},

            {"id": 39, "code": '1.2.1.1', "name": 'Notebook', "account_type": 4, "parent": 21,
             "operate": True},
            {"id": 40, "code": '1.2.1.2', "name": 'Carro', "account_type": 4, "parent": 21,
             "operate": True},
            {"id": 41, "code": '1.2.1.3', "name": 'Moto', "account_type": 4, "parent": 21,
             "operate": True},
            {"id": 42, "code": '1.2.1.4', "name": 'Celular', "account_type": 4, "parent": 21,
             "operate": True},
            {"id": 43, "code": '1.2.1.5', "name": 'Tablet', "account_type": 4, "parent": 21,
             "operate": True},
            {"id": 44, "code": '1.2.1.6', "name": 'Desktop', "account_type": 4, "parent": 21,
             "operate": True},

            {"id": 45, "code": '1.2.2.1', "name": 'Lote', "account_type": 4, "parent": 22, "operate": True},
            {"id": 46, "code": '1.2.2.2', "name": 'Casa', "account_type": 4, "parent": 22, "operate": True},

            {"id": 47, "code": '1.2.3.1', "name": 'Participação em empresas', "account_type": 4, "parent": 23,
             "operate": True},

            {"id": 48, "code": '1.1.3.1', "name": 'Ações', "account_type": 4, "parent": 48,
             "operate": True},
            {"id": 49, "code": '1.1.3.2', "name": 'Fundos Investimento', "account_type": 4, "parent": 48,
             "operate": True},

            {"id": 50, "code": '1.3.1.1', "name": 'TRE', "account_type": 4, "parent": 24, "operate": True},
            {"id": 51, "code": '1.3.1.2', "name": 'Unitins', "account_type": 4, "parent": 24,
             "operate": True},
            {"id": 52, "code": '1.3.1.3', "name": 'Unest', "account_type": 4, "parent": 24, "operate": True},

            {"id": 53, "code": '1.3.2.1', "name": 'TRE', "account_type": 4, "parent": 25, "operate": True},
            {"id": 54, "code": '1.3.2.2', "name": 'Unitins', "account_type": 4, "parent": 25,
             "operate": True},
            {"id": 55, "code": '1.3.2.3', "name": 'Unest', "account_type": 4, "parent": 25, "operate": True},

            {"id": 56, "code": '1.3.3.1', "name": 'TRE', "account_type": 4, "parent": 26, "operate": True},
            {"id": 57, "code": '1.3.3.2', "name": 'Unitins', "account_type": 4, "parent": 26,
             "operate": True},
            {"id": 58, "code": '1.3.3.3', "name": 'Unest', "account_type": 4, "parent": 26, "operate": True},
        ]
    )

    op.bulk_insert(
        account,
        [
            {"id": 59, "code": '2.1.0.0', "name": 'Financeiro', "account_type": 5, "parent": 12},
            {"id": 60, "code": '2.2.0.0', "name": 'accounts Serviço Público', "account_type": 5, "parent": 12},
            {"id": 61, "code": '2.3.0.0', "name": 'Impostos', "account_type": 5, "parent": 12},
            {"id": 62, "code": '2.4.0.0', "name": 'Dívidas', "account_type": 5, "parent": 12},

            {"id": 63, "code": '2.1.1.0', "name": 'Bancos', "account_type": 5, "parent": 59},
            {"id": 64, "code": '2.1.2.0', "name": 'Cartões de Crédito', "account_type": 5, "parent": 59},
            {"id": 65, "code": '2.1.3.0', "name": 'Empréstimos', "account_type": 5, "parent": 59},
            {"id": 66, "code": '2.1.4.0', "name": 'Cheque Especial', "account_type": 5, "parent": 59},
        ]
    )

    op.bulk_insert(
        account,
        [
            {"id": 67, "code": '2.2.1.0', "name": 'Água', "account_type": 5, "parent": 60, "operate": True},
            {"id": 68, "code": '2.2.2.0', "name": 'Energia', "account_type": 5, "parent": 60, "operate": True},
            {"id": 69, "code": '2.2.3.0', "name": 'Gás', "account_type": 5, "parent": 60, "operate": True},

            {"id": 70, "code": '2.3.1.0', "name": 'Imposto de Renda', "account_type": 5, "parent": 61,
             "operate": True},
            {"id": 71, "code": '2.3.2.0', "name": 'IOF', "account_type": 5, "parent": 61, "operate": True},

            {"id": 72, "code": '2.3.1.0', "name": 'Não negociadas', "account_type": 5, "parent": 62,
             "operate": True},
            {"id": 73, "code": '2.3.2.0', "name": 'Negociadas', "account_type": 5, "parent": 62, "operate": True},
            {"id": 74, "code": '2.3.3.0', "name": 'Sem juros', "account_type": 5, "parent": 62, "operate": True},

            {"id": 75, "code": '2.1.1.1', "name": 'rates', "account_type": 5, "parent": 63, "operate": True},
            {"id": 76, "code": '2.1.1.2', "name": 'Serviços', "account_type": 5, "parent": 63, "operate": True},
            {"id": 77, "code": '2.1.1.3', "name": 'Título Capitalização', "account_type": 5, "parent": 63,
             "operate": True},
            {"id": 78, "code": '2.1.1.4', "name": 'Previdência', "account_type": 5, "parent": 63, "operate": True},

            {"id": 79, "code": '2.1.2.1', "name": 'Nubank', "account_type": 5, "parent": 64, "operate": True},
            {"id": 80, "code": '2.1.2.2', "name": 'Mercado Pago', "account_type": 5, "parent": 64,
             "operate": True},
            {"id": 81, "code": '2.1.2.3', "name": 'Santander', "account_type": 5, "parent": 64, "operate": True},

            {"id": 82, "code": '2.1.3.1', "name": 'Nubank', "account_type": 5, "parent": 65, "operate": True},
            {"id": 83, "code": '2.1.3.2', "name": 'Santander', "account_type": 5, "parent": 65, "operate": True},
            {"id": 84, "code": '2.1.3.3', "name": 'Mercado Pago', "account_type": 5, "parent": 65,
             "operate": True},
            {"id": 85, "code": '2.1.3.4', "name": 'Bradesco', "account_type": 5, "parent": 65, "operate": True},
            {"id": 86, "code": '2.1.3.5', "name": 'Financimaneto Carro', "account_type": 5, "parent": 65,
             "operate": True},
            {"id": 87, "code": '2.1.3.6', "name": 'Financimaneto Energia Solar', "account_type": 5, "parent": 65,
             "operate": True},
            {"id": 88, "code": '2.1.3.7', "name": 'Consignado', "account_type": 5, "parent": 65, "operate": True},

            {"id": 89, "code": '2.1.4.1', "name": 'Caixa', "account_type": 5, "parent": 67, "operate": True},

            {"id": 90, "code": '3.1.0.0', "name": 'Resultado', "account_type": 3, "parent": 13, "operate": True}
        ]
    )

    op.bulk_insert(
        account,
        [
            {"id": 91, "code": '4.1.0.0', "name": 'Pagamento', "account_type": 7, "parent": 14},
            {"id": 92, "code": '5.1.0.0', "name": 'Recebimento', "account_type": 6, "parent": 15},

            {"id": 93, "code": '4.1.1.0', "name": 'Casa', "account_type": 7, "parent": 91},
            {"id": 94, "code": '4.1.2.0', "name": 'Locomoção', "account_type": 7, "parent": 91},
            {"id": 95, "code": '4.1.4.0', "name": 'Compras', "account_type": 7, "parent": 91},
            {"id": 96, "code": '4.1.5.0', "name": 'Diversão e Bem estar', "account_type": 7, "parent": 91},
            {"id": 98, "code": '4.1.6.0', "name": 'Estudo', "account_type": 7, "parent": 91},
            {"id": 99, "code": '4.1.7.0', "name": 'Roupa e beleza', "account_type": 7, "parent": 91},
            {"id": 100, "code": '4.1.8.0', "name": 'Animais de estimação', "account_type": 7, "parent": 91},
            {"id": 101, "code": '4.1.9.0', "name": 'Doação', "account_type": 7, "parent": 91},
            {"id": 144, "code": '4.1.10.0', "name": 'Softwares', "account_type": 7, "parent": 91},
            {"id": 115, "code": '4.1.11.0', "name": 'Alimentação', "account_type": 7, "parent": 91},
            {"id": 131, "code": '4.1.12.0', "name": 'Bens', "account_type": 7, "parent": 91},
            {"id": 160, "code": '4.1.13.0', "name": 'Financeiro', "account_type": 7, "parent": 91},

            {"id": 166, "code": '5.1.1.0', "name": 'Salários', "account_type": 6, "parent": 92},
            {"id": 167, "code": '5.1.2.0', "name": 'Honorários', "account_type": 6, "parent": 92},
            {"id": 168, "code": '5.1.3.0', "name": 'Serviços', "account_type": 6, "parent": 92},
            {"id": 169, "code": '5.1.4.0', "name": 'Vendas', "account_type": 6, "parent": 92},
            {"id": 170, "code": '5.1.5.0', "name": 'Rendimentos Financeiros', "account_type": 6, "parent": 92},
            {"id": 171, "code": '5.1.6.0', "name": 'Lucros', "account_type": 6, "parent": 92}
        ]
    )

    op.bulk_insert(
        account,
        [
            {"id": 102, "code": '4.1.1.1', "name": 'Aluguel', "account_type": 7, "parent": 93, "operate": True},
            {"id": 103, "code": '4.1.1.2', "name": 'Diárias', "account_type": 7, "parent": 93, "operate": True},
            {"id": 104, "code": '4.1.1.3', "name": 'Manutenção Casa', "account_type": 7, "parent": 93,
             "operate": True},
            {"id": 105, "code": '4.1.1.4', "name": 'Segurança Casa', "account_type": 7, "parent": 93,
             "operate": True},

            {"id": 106, "code": '4.1.2.1', "name": 'Gasolina', "account_type": 7, "parent": 94, "operate": True},
            {"id": 107, "code": '4.1.2.2', "name": 'Passagens', "account_type": 7, "parent": 94, "operate": True},
            {"id": 108, "code": '4.1.2.3', "name": 'Diárias Hotel', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 109, "code": '4.1.2.4', "name": 'Aluguel Carro', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 110, "code": '4.1.2.5', "name": 'Manutenção veículo', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 111, "code": '4.1.2.6', "name": 'Seguro Veículo', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 112, "code": '4.1.2.7', "name": 'Seguro Viagem', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 113, "code": '4.1.2.8', "name": 'Taxi/Aplicativo', "account_type": 7, "parent": 94,
             "operate": True},
            {"id": 114, "code": '4.1.2.9', "name": 'Entregador/Aplicativo', "account_type": 7, "parent": 94,
             "operate": True},

            {"id": 116, "code": '4.1.11.1', "name": 'Restaurante', "account_type": 7, "parent": 115,
             "operate": True},
            {"id": 117, "code": '4.1.11.2', "name": 'Entrega', "account_type": 7, "parent": 115,
             "operate": True},
            {"id": 118, "code": '4.1.11.3', "name": 'Encomenda', "account_type": 7, "parent": 115,
             "operate": True},
            {"id": 119, "code": '4.1.11.4', "name": 'Lanche', "account_type": 7, "parent": 115,
             "operate": True},
            {"id": 120, "code": '4.1.11.5', "name": 'Doces', "account_type": 7, "parent": 115,
             "operate": True},

            {"id": 179, "code": '4.1.4.1', "name": 'Mercadinho', "account_type": 7, "parent": 95, "operate": True},
            {"id": 180, "code": '4.1.4.2', "name": 'Farmácia', "account_type": 7, "parent": 95, "operate": True},
            {"id": 181, "code": '4.1.4.3', "name": 'Atacarejo', "account_type": 7, "parent": 95, "operate": True},
            {"id": 182, "code": '4.1.4.4', "name": 'Livraria', "account_type": 7, "parent": 95, "operate": True},
            {"id": 183, "code": '4.1.4.5', "name": 'Bazar', "account_type": 7, "parent": 95, "operate": True},
            {"id": 184, "code": '4.1.4.6', "name": 'Supermercado', "account_type": 7, "parent": 95,
             "operate": True},

            {"id": 121, "code": '4.1.5.1', "name": 'Cachaçada', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 122, "code": '4.1.5.2', "name": 'Cinema', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 123, "code": '4.1.5.3', "name": 'Stream', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 124, "code": '4.1.5.4', "name": 'Livros e Gibis', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 125, "code": '4.1.5.5', "name": 'Acampamento', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 126, "code": '4.1.5.6', "name": 'Clube', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 136, "code": '4.1.5.7', "name": 'RPG', "account_type": 7, "parent": 96,
             "operate": True},
            {"id": 150, "code": '4.1.5.8', "name": 'Jogos', "account_type": 7, "parent": 96,
             "operate": True},

            {"id": 127, "code": '4.1.6.1', "name": 'Escola/Faculdade', "account_type": 7, "parent": 98,
             "operate": True},
            {"id": 128, "code": '4.1.6.2', "name": 'Cursos', "account_type": 7, "parent": 98,
             "operate": True},
            {"id": 129, "code": '4.1.6.3', "name": 'Livros Didáticos', "account_type": 7, "parent": 98,
             "operate": True},
            {"id": 130, "code": '4.1.6.4', "name": 'Material de Escritório', "account_type": 7, "parent": 98,
             "operate": True},

            {"id": 132, "code": '4.1.7.1', "name": 'Roupas', "account_type": 7, "parent": 99, "operate": True},
            {"id": 133, "code": '4.1.7.2', "name": 'Calçados', "account_type": 7, "parent": 99, "operate": True},
            {"id": 134, "code": '4.1.7.3', "name": 'Lingerie', "account_type": 7, "parent": 99, "operate": True},
            {"id": 135, "code": '4.1.7.4', "name": 'Fantasia', "account_type": 7, "parent": 99, "operate": True},
            {"id": 137, "code": '4.1.7.5', "name": 'Corte Cabelo', "account_type": 7, "parent": 99,
             "operate": True},
            {"id": 138, "code": '4.1.7.6', "name": 'Manicure', "account_type": 7, "parent": 99, "operate": True},
            {"id": 139, "code": '4.1.7.7', "name": 'Depilação', "account_type": 7, "parent": 99, "operate": True},

            {"id": 140, "code": '4.1.8.1', "name": 'Ração', "account_type": 7, "parent": 100, "operate": True},
            {"id": 141, "code": '4.1.8.2', "name": 'Veterinário', "account_type": 7, "parent": 100,
             "operate": True},
            {"id": 142, "code": '4.1.8.3', "name": 'Salão', "account_type": 7, "parent": 100, "operate": True},
            {"id": 143, "code": '4.1.8.4', "name": 'Assessórios', "account_type": 7, "parent": 100,
             "operate": True},

            {"id": 145, "code": '4.1.9.1', "name": 'Animais', "account_type": 7, "parent": 101, "operate": True},
            {"id": 146, "code": '4.1.9.2', "name": 'Artistas', "account_type": 7, "parent": 101, "operate": True},
            {"id": 147, "code": '4.1.9.3', "name": 'Cientístas', "account_type": 7, "parent": 101,
             "operate": True},
            {"id": 148, "code": '4.1.9.4', "name": 'Crianças', "account_type": 7, "parent": 101, "operate": True},
            {"id": 149, "code": '4.1.9.5', "name": 'Pessoas na Rua', "account_type": 7, "parent": 101,
             "operate": True},

            {"id": 151, "code": '4.1.10.1', "name": 'Cloud Armazenamento', "account_type": 7, "parent": 144,
             "operate": True},
            {"id": 152, "code": '4.1.10.2', "name": 'Servidores', "account_type": 7, "parent": 144,
             "operate": True},
            {"id": 153, "code": '4.1.10.3', "name": 'Desenvolvimento', "account_type": 7, "parent": 144,
             "operate": True},
            {"id": 154, "code": '4.1.10.4', "name": 'Arte', "account_type": 7, "parent": 144, "operate": True},
            {"id": 155, "code": '4.1.10.5', "name": 'Segurança', "account_type": 7, "parent": 144,
             "operate": True},

            {"id": 156, "code": '4.1.12.1', "name": 'Móveis', "account_type": 7, "parent": 131, "operate": True},
            {"id": 157, "code": '4.1.12.2', "name": 'Veículos', "account_type": 7, "parent": 131, "operate": True},
            {"id": 158, "code": '4.1.12.3', "name": 'Eletrônicos', "account_type": 7, "parent": 131,
             "operate": True},
            {"id": 159, "code": '4.1.12.4', "name": 'Imóveis', "account_type": 7, "parent": 131, "operate": True},

            {"id": 161, "code": '4.1.13.1', "name": 'Previdência Privada', "account_type": 7, "parent": 160,
             "operate": True},
            {"id": 162, "code": '4.1.13.2', "name": 'Fundos de Ação', "account_type": 7, "parent": 160,
             "operate": True},
            {"id": 163, "code": '4.1.13.3', "name": 'Juros', "account_type": 7, "parent": 160, "operate": True},
            {"id": 164, "code": '4.1.13.4', "name": 'Empréstimos', "account_type": 7, "parent": 160,
             "operate": True},
            {"id": 165, "code": '4.1.13.5', "name": 'Dívidas', "account_type": 7, "parent": 160, "operate": True},

            {"id": 174, "code": '6.1.0.0', "name": 'balance Inicial', "account_type": 8, "parent": 172,
             "operate": True},
            {"id": 175, "code": '6.2.0.0', "name": 'Extorno', "account_type": 8, "parent": 172, "operate": True},
            {"id": 176, "code": '6.3.0.0', "name": 'Depreciação', "account_type": 8, "parent": 172,
             "operate": True},

            {"id": 177, "code": '7.1.0.0', "name": 'balance Inicial', "account_type": 9, "parent": 173,
             "operate": True},
            {"id": 178, "code": '7.2.0.0', "name": 'Extorno', "account_type": 9, "parent": 173, "operate": True},

        ]
    )

    op.create_table(
        "tag",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('name', sa.VARCHAR(200), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "record",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('anotation', sa.VARCHAR(200), nullable=False),
        sa.Column('date', sa.DATE, nullable=False),
        sa.Column('value', sa.BIGINT, nullable=False),
        sa.Column('accountDebit', sa.BIGINT, sa.ForeignKey("account.id"), nullable=False),
        sa.Column('accountCredit', sa.BIGINT, sa.ForeignKey("account.id"), nullable=False),
        sa.Column('deleted', sa.BOOLEAN, default=False)
    )

    op.create_table(
        "tag_record",
        sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=False),
        sa.Column('tag', sa.BIGINT, sa.ForeignKey("tag.id"), nullable=False),
        sa.Column('record', sa.BIGINT, sa.ForeignKey("record.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tag_record")
    op.drop_table("record")
    op.drop_table("tag")
    op.drop_table("account")
    op.drop_table("exchange")
    op.drop_table("currency")
    op.drop_table("account_type")
    op.drop_table("operation_type")
