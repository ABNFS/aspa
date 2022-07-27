from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from Database import Base, Mix
from operation_type.database import OperationType


class AccountType(Base, Mix):
    __tablename__ = 'account_type'

    name = Column(VARCHAR(26), nullable=False, unique=True)
    alias = Column(VARCHAR(3), nullable=False, unique=True)
    operation = Column(ForeignKey(OperationType.id), nullable=False)

    my_operation = relationship("OperationType", back_populates="accounts_type")
    accounts = relationship("Account", back_populates="my_account_type")
