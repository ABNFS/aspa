from typing import Optional

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
        currency_db: Optional[Currency] = None
        if not currency:
            raise Exception("Dados Inválidos")
        elif currency.id:
            currency_db = CurrencyRepository.get_by_id(db, currency.id)
        return CurrencyRepository.save(db, currency.to_database(currency_db))

    @staticmethod
    def delete(db: Session, id: int) -> bool:
        return CurrencyRepository.delete(db, id)
