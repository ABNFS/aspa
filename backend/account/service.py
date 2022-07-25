from .repository import AccountRepository
from .data import AccountData
from .database import Account

from sqlalchemy.orm import Session


class AccountService:
    @staticmethod
    def search(db: Session, name: str = ""):
        return AccountRepository.search_by_name(db, name) if name else AccountRepository.get_all(db)

    @staticmethod
    def save(db: Session, account: AccountData) -> Account:
        return AccountRepository.save(db, account.to_database())
