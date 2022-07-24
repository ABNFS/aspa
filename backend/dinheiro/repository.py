from .database import Dinheiro
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class DinheiroRepository:

    @staticmethod
    def busca_por_nome(nome) -> list[Dinheiro]:
        result: list[Dinheiro] = []
        query = select(Dinheiro).where(Dinheiro.nome.ilike(f'%{nome}%')).where(Dinheiro.excluido == False)
        with Session(database_engine) as session:
            for dinheiro in session.scalars(query):
                result.append(dinheiro)
        return result

    @staticmethod
    def busca_todos() -> list[Dinheiro]:
        result: list[Dinheiro] = []
        query = select(Dinheiro).where(Dinheiro.excluido == False)
        with Session(database_engine) as session:
            for dinheiro in session.scalars(query):
                result.append(dinheiro)
        return result
