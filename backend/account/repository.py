from .database import Account
from startup import database_engine

from sqlalchemy import select
from sqlalchemy.orm import Session


class AccountRepository:

    @staticmethod
    def search_by_name(name) -> list[Account]:
        result: list[Account] = []
        query = select(Account).where(Account.name.ilike(f'%{name}%')).where(Account.deleted == False)
        with Session(database_engine) as session:
            for account in session.scalars(query):
                result.append(account)
        return result

    @staticmethod
    def get_all() -> list[Account]:
        result: list[Account] = []
        query = select(Account).where(Account.deleted == False)
        with Session(database_engine) as session:
            for account in session.scalars(query):
                result.append(account)
        return result
