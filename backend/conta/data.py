from pydantic import BaseModel


class ContaData(BaseModel):
    id: int
    codigo: str
    nome: str
    saldo: int
    sigla: str
    moeda: int
    tipo_conta: int
    pai: int
    pode_movimentar: bool
    excluido: bool

    class Config:
        orm_mode = True
