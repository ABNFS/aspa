from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr
from sqlalchemy import Column, BIGINT, BOOLEAN

Base = declarative_base()


@declarative_mixin
class Mix:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    deleted = Column(BOOLEAN, default=False)
