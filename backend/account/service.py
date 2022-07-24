from .repository import AccountRepository


class AcconutService:

    @staticmethod
    def search(name: str = ""):
        return AccountRepository.search_by_name(name) if name else AccountRepository.get_all()