from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN, ForeignKey
from sqlalchemy.orm import declarative_base

from currency.database import Currency
from account_type.database import AccountType

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id = Column(BIGINT, primary_key=True)
    code = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(200), nullable=False)
    balance = Column(BIGINT, nullable=True, default=0)
    alias = Column(VARCHAR(5), nullable=True, default=None)
    currency = Column(BIGINT, ForeignKey(Currency.id), nullable=True, default=1)
    account_type = Column(BIGINT, ForeignKey(AccountType.id), nullable=False)
    parent = Column(BIGINT, ForeignKey(id), nullable=True, default=None)
    operate = Column(BOOLEAN, nullable=False, default=False)
    deleted = Column(BOOLEAN, default=False)