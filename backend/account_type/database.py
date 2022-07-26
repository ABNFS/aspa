from sqlalchemy import Column, BIGINT, VARCHAR, BOOLEAN, ForeignKey

from operation_type.database import OperationType

from Database import Base


class AccountType(Base):
    __tablename__ = 'account_type'
    id = Column(BIGINT, primary_key=True, autoincrement="auto")
    name = Column(VARCHAR(26), nullable=False, unique=True)
    alias = Column(VARCHAR(3), nullable=False, unique=True)
    operation = Column(ForeignKey(OperationType.id), nullable=False)
    deleted = Column(BOOLEAN, default=False)
