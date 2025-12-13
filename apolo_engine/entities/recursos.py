# -*- coding: utf-8 -*-
"""
Módulo de Recursos: Define recursos consumíveis pelas entidades,
como Energia, Mana, Vigor, etc.
"""
from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento

class Energia:
    """
    Recurso básico para todas as ações avançadas (Habilidades, IA, etc.).
    A regeneração é automática ao assinar o evento de avanço de tempo.
    """
    def __init__(self, maxima: float, regeneracao_por_segundo: float, tipo: str = "Nexus"):
        """
        Args:
            maxima (float): O valor máximo que este recurso pode atingir.
            regeneracao_por_segundo (float): A quantidade a ser regenerada por segundo.
            tipo (str): O nome do tipo de energia (ex: "Mana", "Vigor", "Nexus").
        """
        self.maxima = maxima
        self.atual = maxima
        self.regeneracao_por_segundo = regeneracao_por_segundo
        self.tipo = tipo

        # Se inscreve no evento de tempo para regenerar automaticamente
        BARRAMENTO_DE_EVENTOS.assinar("TEMPO_AVANCOU", self._on_tick)

    def _on_tick(self, evento: Evento):
        """
        Callback chamado pelo sistema de eventos para regenerar a energia.
        """
        delta_segundos = evento.dados.get("delta_s", 0.0)
        self.regenerar(delta_segundos)

    def consumir(self, valor: float) -> bool:
        """
        Tenta consumir uma quantidade de energia.

        Args:
            valor (float): A quantidade a ser consumida.

        Returns:
            bool: True se o consumo foi bem-sucedido, False caso contrário.
        """
        if valor <= self.atual:
            self.atual -= valor
            return True
        return False

    def regenerar(self, delta_segundos: float):
        """
        Regenera a energia com base no tempo decorrido.

        Args:
            delta_segundos (float): O tempo em segundos desde o último tick.
        """
        incremento = self.regeneracao_por_segundo * delta_segundos
        self.atual = min(self.maxima, self.atual + incremento)

    def __repr__(self):
        return f"<{self.tipo}: {self.atual:.1f}/{self.maxima:.1f}>"
