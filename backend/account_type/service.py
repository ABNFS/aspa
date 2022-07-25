from typing import Optional
from sqlalchemy.orm import Session

from .data import AccountTypeData
from .repository import AccountTypeRepository
from .database import AccountType


class AccountTypeService:

    @staticmethod
    def save(db: Session, accout_type: AccountTypeData) -> AccountType:
        return AccountTypeRepository.save(db, accout_type.to_database())

    @staticmethod
    def search(db: Session, name: Optional[str]) -> list[AccountType]:
        if name:
            return AccountTypeRepository.search_by_name(db, name)
        return AccountTypeRepository.get_all(db)
