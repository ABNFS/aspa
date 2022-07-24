from .database import Dinheiro
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class DinheiroRepository:

    def busca_por_nome(self, nome) -> list:
        result: list = []
        query = select(Dinheiro).where(Dinheiro.nome.like(nome))
        with Session(database_engine) as session:
            for dinheiro in session.scalars(query):
                result.append(dinheiro)
        return result
