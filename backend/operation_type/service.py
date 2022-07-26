from typing import Optional

from sqlalchemy.orm import Session

from .repository import OperationTypeRepository
from .data import OperationTypeData
from .database import OperationType


class OperationTypeService:

    @staticmethod
    def save(db: Session, operation_type: OperationTypeData) -> OperationType:
        operation_db: Optional[OperationType] = None
        if operation_type.id:
            operation_db = OperationTypeRepository.get_by_id(db, operation_type.id)
        return OperationTypeRepository.save(db, operation_type.to_database(operation_db))

    @staticmethod
    def search(db: Session, name:str):
        if name:
            return OperationTypeRepository.search_by_name(db, name)
        return OperationTypeRepository.get_all(db)
