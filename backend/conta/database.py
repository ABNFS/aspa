from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Conta(Base):
    __tablename__ = "conta"

    id = Column('id', BIGINT, primary_key=True, autoincrement=False)
    codigo = Column('codigo', VARCHAR(20), nullable=False)
    nome = Column('nome', VARCHAR(200), nullable=False)
    saldo = Column('saldo', BIGINT, nullable=False, default=0)
    sigla = Column('sigla', VARCHAR(5), nullable=True, default=None)
    moeda = Column('moeda', BIGINT, ForeignKey("moeda.id"), nullable=False, default=10)
    tipo_conta = Column('tipo_conta', BIGINT, ForeignKey("tipo_conta.id"), nullable=False)
    pai = Column('pai', BIGINT, ForeignKey("conta.id"), nullable=True, default=None)
    pode_movimentar = Column('pode_movimentar', BOOLEAN, nullable=False, default=False)
    excluido = Column('excluido', BOOLEAN, default=False)
