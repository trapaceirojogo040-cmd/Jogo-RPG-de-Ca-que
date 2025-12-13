# -*- coding: utf-8 -*-
"""
Módulo de Tempo: Controla o fluxo do tempo dentro do jogo,
com funcionalidades avançadas de pausa, velocidade e avanço manual.
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento

# ============================================================
# EXCEÇÕES
# ============================================================

class ErroDeTempo(Exception):
    """Exceção para erros relacionados ao sistema de tempo."""
    pass

# ============================================================
# CLASSE PRINCIPAL DO TEMPO
# ============================================================

class MotorDeTempo:
    """
    Gerencia o tempo de jogo de forma dinâmica, com controle de velocidade,
    pausa e disparo de eventos de sincronização.
    """
    def __init__(self, tempo_inicial: Optional[datetime] = None):
        self.velocidade = 1.0
        self.tempo_de_jogo = tempo_inicial or datetime(3000, 1, 1, 6, 0, 0)
        self.ultimo_tick_real = datetime.utcnow()
        self.pausado = False
        self.dias_passados = 0

    def tick(self):
        """
        Avança o tempo do jogo e dispara os eventos de tempo.
        Deve ser chamado a cada ciclo do motor.
        """
        if self.pausado:
            return

        try:
            agora_real = datetime.utcnow()
            delta_segundos_real = (agora_real - self.ultimo_tick_real).total_seconds()
            self.ultimo_tick_real = agora_real

            avanco_jogo = delta_segundos_real * self.velocidade
            tempo_anterior = self.tempo_de_jogo
            self.tempo_de_jogo += timedelta(seconds=avanco_jogo)

            # Dispara o evento principal de passagem de tempo (essencial para a arquitetura)
            BARRAMENTO_DE_EVENTOS.disparar(
                Evento(
                    nome="TEMPO_AVANCOU",
                    origem="MotorDeTempo",
                    gravidade=1,
                    dados={"delta_s": avanco_jogo, "tempo_atual": self.tempo_de_jogo}
                )
            )

            # Verifica se um novo dia começou (essencial para a arquitetura)
            if self.tempo_de_jogo.day != tempo_anterior.day:
                self.dias_passados += 1
                BARRAMENTO_DE_EVENTOS.disparar(
                    Evento(
                        nome="NOVO_DIA",
                        origem="MotorDeTempo",
                        gravidade=3,
                        dados={"dia_numero": self.dias_passados}
                    )
                )
        except Exception as e:
            raise ErroDeTempo(f"Falha ao processar o tick de tempo: {e}")

    def definir_velocidade(self, velocidade: float):
        if not 0.01 <= velocidade <= 50.0:
            raise ErroDeTempo("A velocidade do tempo deve estar entre 0.01 e 50.0.")
        self.velocidade = velocidade

    def pausar(self):
        if not self.pausado:
            self.pausado = True
            BARRAMENTO_DE_EVENTOS.disparar(Evento(nome="TEMPO_PAUSADO", origem="MotorDeTempo"))

    def retomar(self):
        if self.pausado:
            self.pausado = False
            self.ultimo_tick_real = datetime.utcnow() # Reseta o delta time
            BARRAMENTO_DE_EVENTOS.disparar(Evento(nome="TEMPO_RETOMADO", origem="MotorDeTempo"))

    def avancar_segundos(self, segundos: float):
        if segundos > 0:
            self.tempo_de_jogo += timedelta(seconds=segundos)

    def obter_info(self) -> Dict[str, Any]:
        """Retorna um dicionário com o estado atual do sistema de tempo."""
        return {
            "tempo_de_jogo": self.tempo_de_jogo.isoformat(),
            "velocidade": self.velocidade,
            "pausado": self.pausado
        }

# Instância única global
TEMPO = MotorDeTempo()
