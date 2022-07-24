from .repository import DinheiroRepository
from .data import DinheiroData


class DinheiroService:
    def salvar(self, dinheiro: DinheiroData):
        pass

    @staticmethod
    async def busca(nome):
        return DinheiroRepository.busca_por_nome(nome) if nome else DinheiroRepository.busca_todos()
