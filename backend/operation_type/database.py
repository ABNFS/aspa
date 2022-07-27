from sqlalchemy import Column, VARCHAR,CHAR
from sqlalchemy.orm import relationship

from Database import Base, Mix

class OperationType(Base, Mix):
    __tablename__ = 'operation_type'

    name = Column(VARCHAR(20), nullable=False, unique=True)
    alias = Column(CHAR(1), nullable=False, unique=True)

    accounts_type = relationship("AccountType", back_populates="my_operation")
