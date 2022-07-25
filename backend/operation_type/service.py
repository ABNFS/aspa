from sqlalchemy.orm import Session

from .repository import OperationTypeRepository
from .data import OperationTypeData
from .database import OperationType


class OperationTypeService:

    @staticmethod
    def new(db: Session, operation_type: OperationTypeData) -> OperationType:
        return OperationTypeRepository.save(db, operation_type.to_database())

    @staticmethod
    def search(db: Session, name:str):
        if name:
            return OperationTypeRepository.search_by_name(db, name)
        return OperationTypeRepository.get_all(db)
