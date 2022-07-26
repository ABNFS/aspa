from sqlalchemy.orm import Session

from .database import AccountType

from Repository import GenericsRepository


class AccountTypeRepository:

    @staticmethod
    def save(db: Session, account_type: AccountType) -> AccountType:
        return GenericsRepository.save(db, account_type)

    @staticmethod
    def get_all(db: Session) -> list[AccountType]:
        return GenericsRepository.get_all(db, AccountType)

    @staticmethod
    def search_by_name(db: Session, name: str) -> list[AccountType]:
        return GenericsRepository.search_by_name(db, AccountType, name)

    @staticmethod
    def get_by_id(db: Session, id: int) -> AccountType:
        return GenericsRepository.get_by_id(db, AccountType, id)

    @staticmethod
    def delete(db: Session, id: int) -> bool:
        return GenericsRepository.delete(db, AccountType, id)
