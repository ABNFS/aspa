from .database import Conta
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class ContaRepository:

    @staticmethod
    def busca_por_nome(nome) -> list[Conta]:
        result: list[Conta] = []
        query = select(Conta).where(Conta.nome.ilike(f'%{nome}%')).where(Conta.excluido == False)
        with Session(database_engine) as session:
            for conta in session.scalars(query):
                result.append(conta)
        return result

    @staticmethod
    def busca_todos() -> list[Conta]:
        result: list[Conta] = []
        query = select(Conta).where(Conta.excluido == False)
        with Session(database_engine) as session:
            for conta in session.scalars(query):
                result.append(conta)
        return result
