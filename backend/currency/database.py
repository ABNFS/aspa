from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"

    id = Column(BIGINT, primary_key=True, autoincement=True)
    name = Column(VARCHAR(200), nullable=False)
    alias = Column(VARCHAR(5), nullable=False)
    default = Column(BOOLEAN, default=False)
    deleted = Column(BOOLEAN, default=False)

    def __repr__(self) -> str:
        return f'nome: ${self.nome}, sigla: ${self.sigla}'
