from .database import Currency
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class CurrencyRepository:

    @staticmethod
    def find_by_name(name) -> list[Currency]:
        result: list[Currency] = []
        query = select(Currency).where(Currency.name.ilike(f'%{name}%')).where(Currency.deleted == False)
        with Session(database_engine) as session:
            for currency in session.scalars(query):
                result.append(currency)
        return result

    @staticmethod
    def get_all() -> list[Currency]:
        result: list[Currency] = []
        query = select(Currency).where(Currency.deleted == False)
        with Session(database_engine) as session:
            for currency in session.scalars(query):
                result.append(currency)
        return result
