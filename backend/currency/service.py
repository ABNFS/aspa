from .repository import CurrencyRepository
from .data import CurrencyData


class CurrencyService:
    @staticmethod
    def search(name):
        return CurrencyRepository.find_by_name(name) if name else CurrencyRepository.get_all()
