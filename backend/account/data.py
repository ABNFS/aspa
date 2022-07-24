from pydantic import BaseModel


class AccountData(BaseModel):
    id: int
    code: str
    name: str
    balance: int
    alias: str
    currency: int
    account_type: int
    parent: int
    operate: bool
    deleted: bool

    class Config:
        orm_mode = True
