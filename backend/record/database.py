from sqlalchemy import Column, BIGINT, DATE, BOOLEAN, VARCHAR, ForeignKey

from account.database import Account

from Database import Base


class Record(Base):

    __tablename__ = 'record'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    anotation = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    amount = Column(BIGINT, nullable=False)
    account_debit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    account_credit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    deleted = Column(BOOLEAN, default=False, nullable=True)
    tags = []