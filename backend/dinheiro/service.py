from .repository import DinheiroRepository
from .data import DinheiroData


class DinheiroService:
    db = DinheiroRepository()

    def salvar(self, dinheiro: DinheiroData):
        pass

    def busca(self, nome):
        return self.db.busca_por_nome(nome)
