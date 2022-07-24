from .repository import ContaRepository


class ContaService:

    @staticmethod
    def busca(nome: str = ""):
        return ContaRepository.busca_por_nome(nome) if nome else ContaRepository.busca_todos()