# -*- coding: utf-8 -*-
"""
Módulo de Eventos: Implementa o padrão Observer para desacoplar
os diferentes sistemas do motor.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

from apolo_engine.core.logger import LOGGER

# ---------------------------------------------------------------------------------------------------------
# Estrutura do Evento
# ---------------------------------------------------------------------------------------------------------

class Evento:
    """
    Estrutura de dados para um evento disparado no motor.
    Contém informações sobre o que aconteceu, quem originou e dados relevantes.
    """
    def __init__(self, nome: str, origem: str, gravidade: int = 1, dados: Optional[Dict[str, Any]] = None):
        """
        Args:
            nome (str): Nome único do evento (ex: "DANO_RECEBIDO", "NOVO_DIA").
            origem (str): Módulo que disparou o evento.
            gravidade (int): Nível de importância do evento (1-5).
            dados (Optional[Dict[str, Any]]): Dados adicionais associados ao evento.
        """
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.origem = origem
        self.gravidade = gravidade
        self.dados = dados or {}
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return f"<Evento {self.nome} (Origem: {self.origem}, Gravidade: {self.gravidade})>"

# ---------------------------------------------------------------------------------------------------------
# Gerenciador de Eventos (Event Bus)
# ---------------------------------------------------------------------------------------------------------

class GerenciadorDeEventos:
    """
    Gerencia a fila de eventos e a notificação de assinantes (Observer Pattern).
    Funciona como um barramento central para toda a comunicação do motor.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorDeEventos, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        self.fila: List[Evento] = []
        self.assinantes: Dict[str, List[Callable]] = {}  # "nome_evento" -> [callback1, callback2]
        self._inicializado = True
        LOGGER.registrar("GerenciadorDeEventos", "inicio", {"mensagem": "Sistema de eventos inicializado."})

    def disparar(self, evento: Evento):
        """
        Adiciona um evento à fila de processamento e o registra no logger.

        Args:
            evento (Evento): O objeto de evento a ser disparado.
        """
        self.fila.append(evento)
        LOGGER.registrar(
            origem=evento.origem,
            tipo="evento_disparado",
            dados={"evento": evento.nome, "gravidade": evento.gravidade}
        )

    def assinar(self, nome_evento: str, callback: Callable):
        """
        Permite que um módulo ou função se registre para ser notificado sobre um evento.

        Args:
            nome_evento (str): O nome do evento ao qual se inscrever.
            callback (Callable): A função que será chamada quando o evento ocorrer.
        """
        if nome_evento not in self.assinantes:
            self.assinantes[nome_evento] = []
        self.assinantes[nome_evento].append(callback)
        LOGGER.registrar("GerenciadorDeEventos", "nova_assinatura", {"evento": nome_evento, "callback": callback.__name__})

    def processar_fila(self):
        """
        Processa todos os eventos na fila, notificando os assinantes.
        Este método deve ser chamado a cada ciclo (tick) do motor principal.
        """
        # Copia a fila para evitar problemas com eventos disparados durante o processamento
        eventos_para_processar = self.fila[:]
        self.fila.clear()

        for evento in eventos_para_processar:
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

# Instância única global
BARRAMENTO_DE_EVENTOS = GerenciadorDeEventos()
