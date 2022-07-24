from typing import Any

from pydantic import BaseModel


class CurrencyData(BaseModel):
    id: int
    name: str
    alias: str
    default: bool
    deleted: bool

    class Config:
        orm_mode = True