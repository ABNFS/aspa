from sqlalchemy import Column, BIGINT, DATE, BOOLEAN, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from account.database import Account

from Database import Base, Mix


class TagRecord(Base):
    __tablename__ = 'tag_record'
    record = ForeignKey(BIGINT, ForeignKey('Record.id'), primary_key=True)
    tag = ForeignKey(BIGINT, ForeignKey('Tag.id'), primary_key=True)


class Record(Base, Mix):

    anotation = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    amount = Column(BIGINT, nullable=False)
    account_debit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    account_credit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    my_tags = relationship('Tag', secondary=TagRecord, back_populates='my_records')

    my_accounts = relationship('Account', back_populates='records')
