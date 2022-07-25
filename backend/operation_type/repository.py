from sqlalchemy.orm import Session

from Repository import GenericsRepository
from .database import OperationType

class OperationTypeRepository:

    @staticmethod
    def save(db: Session, operation_type: OperationType) -> OperationType:
        return GenericsRepository.save(db, operation_type)

    @staticmethod
    def search_by_name(db: Session, name: str):
        return GenericsRepository.search_by_name(db, OperationType, name)

    @staticmethod
    def get_all(db: Session):
        return GenericsRepository.get_all(db, OperationType)