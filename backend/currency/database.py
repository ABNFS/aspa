from sqlalchemy import Column, VARCHAR, BIGINT, BOOLEAN, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    alias = Column(VARCHAR(5), nullable=False)
    default = Column(BOOLEAN, default=False)
    deleted = Column(BOOLEAN, default=False)
