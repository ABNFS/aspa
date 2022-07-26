from typing import Optional
from sqlalchemy.orm import Session

from .data import AccountTypeData
from .repository import AccountTypeRepository
from .database import AccountType


class AccountTypeService:

    @staticmethod
    def save(db: Session, account_type: AccountTypeData) -> AccountType:
        account_type_db: AccountType
        account_type_db = account_type.to_database(
            _db=AccountTypeRepository.get_by_id(db, account_type.id) if account_type.id else None)
        if not account_type_db:
            raise Exception("Account Type for update not found!")
        return AccountTypeRepository.save(db, account_type_db)

    @staticmethod
    def search(db: Session, name: Optional[str]) -> list[AccountType]:
        if name:
            return AccountTypeRepository.search_by_name(db, name)
        return AccountTypeRepository.get_all(db)

    @staticmethod
    def delete(db: Session, id: int) -> bool:
        return AccountTypeRepository.delete(db, id)

    @staticmethod
    def get(db: Session, id:int) -> AccountType:
        return AccountTypeRepository.get_by_id(db, id)