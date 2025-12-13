# -*- coding: utf-8 -*-
"""
Componente Guardian: Gerenciador de Memória

Armazena em memória os resultados das análises de arquivos,
permitindo que as informações sejam reutilizadas sem a necessidade
de reanalisar o mesmo código repetidamente.
"""
from typing import Dict, Any, List, Optional

class GerenciadorDeMemoria:
    """Um simples armazenamento chave-valor em memória para os relatórios de análise."""

    def __init__(self):
        self.memoria: Dict[str, Dict[str, Any]] = {}

    def armazenar(self, chave: str, dados: Dict[str, Any]):
        """Armazena um relatório de análise associado a uma chave (caminho do arquivo)."""
        self.memoria[chave] = dados

    def obter(self, chave: str) -> Optional[Dict[str, Any]]:
        """Recupera um relatório da memória usando sua chave."""
        return self.memoria.get(chave)

    def listar_chaves(self) -> List[str]:
        """Retorna uma lista de todas as chaves (arquivos analisados) na memória."""
        return list(self.memoria.keys())

    def limpar(self):
        """Limpa todos os dados armazenados na memória."""
        self.memoria.clear()
