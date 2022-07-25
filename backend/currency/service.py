from .repository import CurrencyRepository
from .database import Currency
from .data import CurrencyData

from sqlalchemy.orm import Session


class CurrencyService:
    @staticmethod
    def search(db: Session, name: str = ""):
        return CurrencyRepository.search_by_name(db, name) if name else CurrencyRepository.get_all(db)

    @staticmethod
    def save(db: Session, currency: CurrencyData) -> Currency:
        if "id" not in currency:
            raise Exception("It is imposible save a new object, please use new")
        return CurrencyRepository.save(db, currency.to_database())

    @staticmethod
    def new(db: Session, currency: CurrencyData) -> Currency:
        return CurrencyRepository.save(db, currency.to_database())

