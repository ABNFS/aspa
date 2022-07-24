from .database import Dinheiro
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class DinheiroRepository:

    @staticmethod
    async def busca_por_nome(nome) -> list[Dinheiro]:
        result: list[Dinheiro] = []
        query = select(Dinheiro).where(Dinheiro.nome.like(nome))
        with Session(database_engine) as session:
            for dinheiro in session.scalars(query):
                result.append(dinheiro)
        return result

    @staticmethod
    async def busca_todos() -> list[Dinheiro]:
        result: list[Dinheiro] = []
        query = select(Dinheiro).where(not Dinheiro.excluido)
        with Session(database_engine) as session:
            for dinheiro in session.scalars(query):
                result.append(dinheiro)
        return result
