# -*- coding: utf-8 -*-
"""
Módulo Logger: Centraliza o registro de todos os eventos e
informações críticas do motor, agora com estrutura de dados e funcionalidades avançadas.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# ============================================================
# ESTRUTURAS E EXCEÇÕES
# ============================================================

class ErroDeLog(Exception):
    """Exceção para erros relacionados ao sistema de log."""
    pass

@dataclass
class EntradaDeLog:
    """Estrutura de dados para uma entrada de log, usando dataclass para robustez."""
    id: str
    origem: str
    tipo: str
    dados: Dict[str, Any]
    timestamp: str

    def para_dict(self) -> Dict[str, Any]:
        """Converte a entrada de log para um dicionário."""
        return self.to_dict() # Dataclasses já fornecem um método similar, mas vamos manter a consistência.

# ============================================================
# CLASSE PRINCIPAL DO LOGGER
# ============================================================

class MotorLogger:
    """
    Sistema de log centralizado, aprimorado com limite de tamanho,
    filtros avançados e estatísticas.
    """

    def __init__(self, tamanho_maximo: int = 5000):
        if tamanho_maximo <= 0:
            raise ErroDeLog("O tamanho máximo do log deve ser um número positivo.")
        self.tamanho_maximo = tamanho_maximo
        self.eventos: List[EntradaDeLog] = []

    def registrar(self, origem: str, tipo: str, dados: Dict[str, Any]) -> str:
        """
        Registra um novo evento no log.
        Retorna o ID do evento para rastreamento.
        """
        if not origem or not tipo:
            raise ErroDeLog("Origem e tipo são campos obrigatórios para o registro.")

        id_evento = str(uuid.uuid4())
        entrada = EntradaDeLog(
            id=id_evento,
            origem=origem,
            tipo=tipo,
            dados=dados,
            timestamp=datetime.utcnow().isoformat()
        )
        self.eventos.append(entrada)

        # Garante que o log não exceda o tamanho máximo
        if len(self.eventos) > self.tamanho_maximo:
            self.eventos = self.eventos[-self.tamanho_maximo:]

        return id_evento

    def consultar(self, tipo: Optional[str] = None, origem: Optional[str] = None, limite: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Consulta eventos no log com múltiplos filtros.
        """
        resultados = self.eventos

        if tipo:
            resultados = [e for e in resultados if e.tipo == tipo]
        if origem:
            resultados = [e for e in resultados if e.origem == origem]
        if limite and limite > 0:
            resultados = resultados[-limite:]

        return [e.__dict__ for e in resultados]

    def limpar(self) -> int:
        """Limpa todos os eventos do log e retorna a quantidade de itens removidos."""
        removidos = len(self.eventos)
        self.eventos.clear()
        return removidos

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas sobre os logs armazenados."""
        if not self.eventos:
            return {"total": 0, "tipos": {}, "origens": {}, "mais_recente": None}

        tipos = {}
        origens = {}
        for evento in self.eventos:
            tipos[evento.tipo] = tipos.get(evento.tipo, 0) + 1
            origens[evento.origem] = origens.get(evento.origem, 0) + 1

        return {
            "total": len(self.eventos),
            "tipos": tipos,
            "origens": origens,
            "mais_recente": self.eventos[-1].timestamp
        }

# Instância única global para ser importada por outros módulos
LOGGER = MotorLogger()
