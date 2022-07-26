from typing import Optional

from pydantic import BaseModel

from .database import Currency


class CurrencyData(BaseModel):
    id: Optional[int]
    name: str
    alias: str
    default: Optional[bool]
    deleted: Optional[bool]

    class Config:
        orm_mode = True

    def to_database(self, _db: Optional[Currency] = None) -> Currency:
        if self.id:
            if _db is None:
                raise Exception("For update Currency first find the account to update")
            _db.name = self.name if self.name else _db.name
            _db.alias = self.alias if self.alias else _db.alias
            _db.default = self.default if self.default else _db.default
            _db.deleted = self.deleted if self.deleted else _db.deleted
            return _db
        return Currency(name=self.name, alias=self.alias, default=self.default, deleted=self.deleted)
