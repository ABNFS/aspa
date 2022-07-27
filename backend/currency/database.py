from sqlalchemy import Column, VARCHAR, BOOLEAN
from sqlalchemy.orm import relationship

from Database import Base, Mix


class Currency(Base, Mix):
    name = Column(VARCHAR(200), nullable=False)
    alias = Column(VARCHAR(5), nullable=False)
    default = Column(BOOLEAN, default=False)

    accounts = relationship("Account", back_populates="my_currency")
