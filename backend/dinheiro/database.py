from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Dinheiro(Base):
    __tablename__ = "moeda"

    id = Column(BIGINT, primary_key=True)
    nome = Column(VARCHAR(200), nullable=False)
    sigla = Column(VARCHAR(5), nullable=False)
    cambio = Column("taxa_cambio", BIGINT, nullable=False)

    def __repr__(self) -> str:
        return f'{"id": ${self.id},"nome": \'${self.nome}\', "sigla": \'${self.sigla}\', "cambio": ${self.cambio / 100} }'
