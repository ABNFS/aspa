from typing import Optional

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
        account_db: Optional[Account] = None
        if account.id:
            account_db = AccountRepository.get_by_id(db, account.id)
        account_db = account.to_database(account_db)
        return AccountRepository.save(db, account_db)

    @staticmethod
    def delete(db: Session, id: int) -> bool:
        return AccountRepository.delete(db, id)
