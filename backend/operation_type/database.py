from sqlalchemy import Column, BIGINT,BOOLEAN, VARCHAR,CHAR

from Database import Base


class OperationType(Base):

    __tablename__ = 'operation_type'
    id = Column(BIGINT, primary_key=True, autoincrement='auto')
    name = Column(VARCHAR(20), nullable=False, unique=True)
    alias = Column(CHAR(1), nullable=False, unique=True)
    deleted = Column(BOOLEAN, default=False)
