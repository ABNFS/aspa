from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Dinheiro(Base):
    __tablename__ = "moeda"

    id = Column(BIGINT, primary_key=True)
    nome = Column(VARCHAR(200), nullable=False)
    sigla = Column(VARCHAR(5), nullable=False)
    padrao = Column(BOOLEAN, default=False)
    excluido = Column(BOOLEAN, default=False)

    def __repr__(self) -> str:
        return f'nome: ${self.nome}, sigla: ${self.sigla}'
