# -*- coding: utf-8 -*-
"""
Módulo do Motor Principal (v2.0): Orquestra todos os sistemas e gerencia
o ciclo de vida do jogo, agora com uma arquitetura mais robusta e integrada.
"""
from datetime import datetime
from typing import Dict, Any

# Importações dos sistemas principais da v2.0
from apolo_engine.core.logger import LOGGER, MotorLogger
from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, GerenciadorDeEventos, Evento
from apolo_engine.core.tempo import TEMPO, MotorDeTempo
from apolo_engine.entities.entidade import Entidade, ErroDeEntidade

# Importações dos sistemas modulares que vamos reconectar
from apolo_engine.systems.fisica import FISICA
from apolo_engine.systems.combate import COMBATE
from apolo_engine.systems.ia import IA
from apolo_engine.systems.crafting import CRAFTING
from apolo_engine.systems.talentos import TALENTOS

# ============================================================
# EXCEÇÕES
# ============================================================

class ErroDeMotor(Exception):
    """Exceção base para erros do motor Apolo."""
    pass

# ============================================================
# CLASSE PRINCIPAL DO MOTOR
# ============================================================

class ApoloEngine:
    """
    Motor principal do jogo que coordena todos os sistemas (v2.0).
    """

    def __init__(self):
        # --- Sistemas Principais (v2.0) ---
        self.logger: MotorLogger = LOGGER
        self.eventos: GerenciadorDeEventos = BARRAMENTO_DE_EVENTOS
        self.tempo: MotorDeTempo = TEMPO

        # --- Repositórios de Dados ---
        self.entidades: Dict[str, Entidade] = {}
        self.universos: Dict[str, Dict[str, Any]] = {}

        # --- Sistemas Modulares (Reconectados) ---
        self.fisica = FISICA
        self.combate = COMBATE
        self.ia = IA
        self.crafting = CRAFTING
        self.talentos = TALENTOS

        self.iniciado = False
        self.logger.registrar("ApoloEngine", "inicializacao", {"versao": "2.0"})

    def iniciar(self):
        """Inicia o motor e dispara o evento de inicialização."""
        if self.iniciado:
            self.logger.registrar("ApoloEngine", "aviso", {"mensagem": "O motor já foi iniciado."})
            return

        self.iniciado = True
        self.eventos.disparar(
            Evento(nome="MOTOR_INICIADO", origem="ApoloEngine", gravidade=1)
        )
        self.logger.registrar("ApoloEngine", "inicio", {"mensagem": "Motor Apolo (v2.0) iniciado com sucesso."})

    def registrar_entidade(self, entidade: Entidade, controlada_por_ia: bool = False):
        """
        Registra uma entidade no motor e em todos os subsistemas relevantes.
        """
        if entidade.id in self.entidades:
            raise ErroDeEntidade(f"A entidade '{entidade.nome}' (ID: {entidade.id}) já está registrada.")

        self.entidades[entidade.id] = entidade

        # Reconecta a entidade aos sistemas modulares
        self.fisica.registrar_entidade(entidade)
        self.talentos.registrar_entidade(entidade)
        if controlada_por_ia:
            self.ia.registrar_entidade(entidade)

        self.logger.registrar("ApoloEngine", "entidade_registrada", {"id": entidade.id, "nome": entidade.nome})

    def tick(self):
        """
        Executa um ciclo de atualização completo do motor.
        """
        if not self.iniciado:
            raise ErroDeMotor("O motor precisa ser iniciado antes de executar o tick.")

        # 1. Avança o tempo (que dispara o evento TEMPO_AVANCOU)
        self.tempo.tick()

        # 2. Processa a fila de eventos (isso fará a IA e a Física reagirem)
        self.eventos.processar_fila()

        # 3. Lógicas que não são baseadas em eventos podem ser chamadas aqui, se necessário.
        # Por exemplo, a regeneração de energia agora é baseada em tempo real, então não precisa de chamada explícita.

        LOGGER.registrar("ApoloEngine", "tick", {"tempo_de_jogo": self.tempo.tempo_de_jogo.isoformat()})

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna um compilado de estatísticas de todos os sistemas principais."""
        return {
            "motor": {"iniciado": self.iniciado, "total_entidades": len(self.entidades)},
            "log": self.logger.obter_estatisticas(),
            "eventos": self.eventos.obter_estatisticas(),
            "tempo": self.tempo.obter_info()
        }

# Instância única global do motor
MOTOR = ApoloEngine()
