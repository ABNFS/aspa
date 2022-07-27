from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from Database import Base, Mix

from account_type.database import AccountType
from currency.database import Currency


class Account(Mix, Base):

    code = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(200), nullable=False)
    balance = Column(BIGINT, nullable=True, default=0)
    alias = Column(VARCHAR(5), nullable=True, default=None)
    currency = Column(BIGINT, ForeignKey(Currency.id), nullable=True, default=1)
    account_type = Column(BIGINT, ForeignKey(AccountType.id), nullable=False)
    operate = Column(BOOLEAN, nullable=False, default=False)

    @declared_attr
    def parent(cls):
        return Column(BIGINT, ForeignKey(cls.id), nullable=True, default=None)

    @declared_attr
    def children(cls):
        return relationship(cls)

    my_account_type = relationship("AccountType", back_populates="accounts")
    my_currency = relationship("Currency", back_populates="accounts")
    # records = relationship('Record', back_populates="my_accounts")
