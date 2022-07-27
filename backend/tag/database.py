from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from Database import Base, Mix
from record.database import TagRecord

class Tag(Base, Mix):
    name = Column(VARCHAR(100), nullable=False)
    my_records = relationship('Record', secondary=TagRecord, back_populates='my_tags')
