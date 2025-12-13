# -*- coding: utf-8 -*-
"""
Módulo de Tempo: Controla o fluxo do tempo dentro do jogo,
disparando eventos cíclicos que sincronizam os sistemas.
"""
from datetime import datetime, timedelta

from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento

class MotorDeTempo:
    """
    Gerencia o tempo de jogo, sua velocidade e dispara eventos
    críticos como a passagem do tempo e a virada de dias.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(MotorDeTempo, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self, velocidade: float = 1.0):
        if self._inicializado:
            return

        self.velocidade = velocidade
        self.tempo_de_jogo = datetime(3000, 1, 1, 6, 0, 0) # Começa às 6h da manhã
        self.ultimo_tick_real = datetime.utcnow()
        self.dias_passados = 0
        self._inicializado = True

    def tick(self):
        """
        Avança o tempo do jogo com base no tempo real decorrido.
        Este método é o coração do motor, devendo ser chamado a cada frame/ciclo.
        """
        agora_real = datetime.utcnow()
        delta_segundos_real = (agora_real - self.ultimo_tick_real).total_seconds()
        self.ultimo_tick_real = agora_real

        # Calcula o avanço do tempo no jogo
        avanco_jogo = delta_segundos_real * self.velocidade
        tempo_anterior = self.tempo_de_jogo
        self.tempo_de_jogo += timedelta(seconds=avanco_jogo)

        # Dispara o evento principal de passagem de tempo
        BARRAMENTO_DE_EVENTOS.disparar(
            Evento(
                nome="TEMPO_AVANCOU",
                origem="MotorDeTempo",
                gravidade=1,
                dados={"delta_s": avanco_jogo, "tempo_atual": self.tempo_de_jogo}
            )
        )

        # Verifica se um novo dia começou
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

    def get_estado_dia_noite(self) -> str:
        """
        Retorna o período atual do dia (Manhã, Tarde, Noite, Madrugada).

        Returns:
            str: O estado atual do dia.
        """
        hora = self.tempo_de_jogo.hour
        if 6 <= hora < 12:
            return "MANHÃ"
        elif 12 <= hora < 18:
            return "TARDE"
        elif 18 <= hora < 24:
            return "NOITE"
        else:
            return "MADRUGADA"

# Instância única global
TEMPO = MotorDeTempo()
