from .database import Account
from Repository import GenericsRepository

from sqlalchemy.orm import Session


class AccountRepository:

    @staticmethod
    def search_by_name(db: Session, name: str = "") -> list[Account]:
        return GenericsRepository.search_by_str_fields(db, Account, {"name": name})

    @staticmethod
    def search_by_name_and_code(db: Session, name: str, code: str) -> list[Account]:
        return GenericsRepository.search_by_str_fields(db, Account, {"name": name, "code": code})

    @staticmethod
    def get_all(db: Session) -> list[Account]:
        return GenericsRepository.get_all(db, Account)

    @staticmethod
    def save(db: Session, account: Account) -> Account:
        return GenericsRepository.save(db, account)

    @staticmethod
    def get_by_id(db: Session, id: int) -> Account:
        return GenericsRepository.get_by_id(db, Account, id)

    @staticmethod
    def delete(db: Session, id: int) -> Account:
        return GenericsRepository.delete(db, Account, id)
