from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id = Column('id', BIGINT, primary_key=True, autoincrement=True)
    code = Column('code', VARCHAR(20), nullable=False)
    name = Column('name', VARCHAR(200), nullable=False)
    balance = Column('balance', BIGINT, nullable=False, default=0)
    alias = Column('alias', VARCHAR(5), nullable=True, default=None)
    currency = Column('currency', BIGINT, ForeignKey("currency.id"), nullable=False, default=10)
    account_type = Column('account_type', BIGINT, ForeignKey("account_type.id"), nullable=False)
    parent = Column('parent', BIGINT, ForeignKey("account.id"), nullable=True, default=None)
    operate = Column('operate', BOOLEAN, nullable=False, default=False)
    deleted = Column('deleted', BOOLEAN, default=False)
