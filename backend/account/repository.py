from .database import Account
from Repository import GenericsRepository

from sqlalchemy.orm import Session


class AccountRepository:

    @staticmethod
    def search_by_name(db: Session, name: str = "") -> list[Account]:
        return GenericsRepository.search_by_name(db, Account, name)

    @staticmethod
    def get_all(db: Session) -> list[Account]:
        return GenericsRepository.get_all(db, Account)

    @staticmethod
    def save(db: Session, account: Account) -> Account:
        return GenericsRepository.save(db, account)