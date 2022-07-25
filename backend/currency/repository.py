from .database import Currency
from Repository import GenericsRepository

from sqlalchemy.orm import Session


class CurrencyRepository:

    @staticmethod
    def search_by_name(db: Session, name: str = "") -> list[Currency]:
        return GenericsRepository.search_by_name(db, Currency, name)

    @staticmethod
    def get_all(db: Session) -> list[Currency]:
        return GenericsRepository.get_all(db, Currency)

    @staticmethod
    def save(db: Session, currency: Currency):
        return GenericsRepository.save(db, currency)

