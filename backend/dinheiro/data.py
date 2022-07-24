from typing import Any

from pydantic import BaseModel


class DinheiroData(BaseModel):
    id: int
    nome: str
    sigla: str
    padrao: bool
    excluido: bool

    class Config:
        orm_mode = True

    def __init__(self, id: int = 0, nome: str = "", sigla: str = "", padrao: bool = False, excluido: bool = False,
                 **data: Any):
        super().__init__(**data)
        self.id = id
        self.nome = nome
        self.sigla = sigla
        self.padrao = padrao
        self.excluido = excluido
