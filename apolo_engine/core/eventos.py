# -*- coding: utf-8 -*-
"""
Módulo de Eventos: Implementa um sistema de eventos robusto com padrão Observer,
validação de dados e estatísticas.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

from apolo_engine.core.logger import LOGGER

# ============================================================
# ESTRUTURAS E EXCEÇÕES
# ============================================================

class ErroDeEvento(Exception):
    """Exceção para erros relacionados ao sistema de eventos."""
    pass

@dataclass
class Evento:
    """Representa um evento no sistema, usando dataclass para validação e robustez."""
    nome: str
    origem: str
    gravidade: int = 1
    dados: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validação automática após a criação da instância."""
        if not self.nome or not self.origem:
            raise ErroDeEvento("Nome e origem do evento não podem ser vazios.")
        if not 1 <= self.gravidade <= 10:
            raise ErroDeEvento("A gravidade do evento deve estar entre 1 e 10.")

    def __repr__(self) -> str:
        return f"<Evento {self.nome} (Origem: {self.origem}, G{self.gravidade})>"

# ============================================================
# GERENCIADOR DE EVENTOS (EVENT BUS)
# ============================================================

class GerenciadorDeEventos:
    """
    Gerencia a fila de eventos e a notificação de assinantes (Observer Pattern).
    Combina o processamento em fila com um sistema de callbacks para desacoplamento.
    """
    def __init__(self):
        self.fila: List[Evento] = []
        self.assinantes: Dict[str, List[Callable]] = {}  # "nome_evento" -> [callback1, callback2]
        LOGGER.registrar("GerenciadorDeEventos", "inicio", {"mensagem": "Sistema de eventos (v2.0) inicializado."})

    def disparar(self, evento: Evento):
        """
        Adiciona um evento à fila de processamento e o registra no logger.
        """
        if not isinstance(evento, Evento):
            raise ErroDeEvento("O objeto disparado deve ser uma instância da classe Evento.")

        self.fila.append(evento)
        LOGGER.registrar(
            origem=evento.origem,
            tipo="evento_disparado",
            dados=evento.__dict__ # Loga o evento completo para melhor rastreabilidade
        )

    def assinar(self, nome_evento: str, callback: Callable):
        """
        Permite que um módulo ou função se registre para ser notificado sobre um evento.
        """
        if nome_evento not in self.assinantes:
            self.assinantes[nome_evento] = []
        if callback not in self.assinantes[nome_evento]:
            self.assinantes[nome_evento].append(callback)
            LOGGER.registrar("GerenciadorDeEventos", "nova_assinatura", {"evento": nome_evento, "callback": callback.__name__})

    def processar_fila(self):
        """
        Processa todos os eventos na fila, notificando os assinantes.
        Este método deve ser chamado a cada ciclo (tick) do motor principal.
        """
        if not self.fila:
            return

        # Processa todos os eventos pendentes na fila
        eventos_para_processar = self.fila[:]
        self.fila.clear()

        for evento in eventos_para_processar:
            # Notifica os assinantes registrados para este evento
            if evento.nome in self.assinantes:
                for callback in self.assinantes[evento.nome]:
                    try:
                        callback(evento)
                    except Exception as e:
                        LOGGER.registrar(
                            "GerenciadorDeEventos",
                            "erro_callback",
                            {
                                "evento": evento.nome,
                                "callback": callback.__name__,
                                "erro": str(e)
                            }
                        )

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas sobre a fila de eventos e assinantes."""
        distribuicao_assinantes = {nome: len(callbacks) for nome, callbacks in self.assinantes.items()}
        return {
            "eventos_na_fila": len(self.fila),
            "eventos_com_assinantes": len(self.assinantes),
            "distribuicao_assinantes": distribuicao_assinantes
        }

# Instância única global
BARRAMENTO_DE_EVENTOS = GerenciadorDeEventos()
