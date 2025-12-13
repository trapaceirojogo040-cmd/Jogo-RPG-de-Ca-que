# -*- coding: utf-8 -*-
"""
Módulo de Recursos: Define recursos consumíveis pelas entidades,
como Energia, Mana, Vigor, etc., com regeneração baseada em delta time.
"""
from datetime import datetime
from typing import Dict, Any

# ============================================================
# EXCEÇÕES
# ============================================================

class ErroDeRecurso(Exception):
    """Exceção para erros relacionados a recursos."""
    pass

# ============================================================
# CLASSE PRINCIPAL DE RECURSO
# ============================================================

class RecursoEnergetico:
    """
    Representa um recurso consumível, como energia ou mana, com regeneração
    precisa baseada no tempo decorrido.
    """
    def __init__(self, maxima: float, regeneracao_por_segundo: float, tipo: str = "Energia"):
        if maxima <= 0:
            raise ErroDeRecurso("A capacidade máxima do recurso deve ser positiva.")
        if regeneracao_por_segundo < 0:
            raise ErroDeRecurso("A regeneração por segundo não pode ser negativa.")

        self.maxima = maxima
        self.atual = maxima
        self.regeneracao_por_segundo = regeneracao_por_segundo
        self.tipo = tipo
        self.ultima_atualizacao = datetime.utcnow()

    def _atualizar_regeneracao(self):
        """
        Calcula e aplica a regeneração com base no tempo real decorrido
        desde a última atualização.
        """
        agora = datetime.utcnow()
        delta_segundos = (agora - self.ultima_atualizacao).total_seconds()

        if delta_segundos > 0:
            regenerado = delta_segundos * self.regeneracao_por_segundo
            self.atual = min(self.maxima, self.atual + regenerado)
            self.ultima_atualizacao = agora

    def consumir(self, valor: float) -> bool:
        """
        Tenta consumir uma quantidade do recurso. Atualiza a regeneração antes de consumir.
        Retorna True se o consumo foi bem-sucedido.
        """
        if valor < 0:
            raise ErroDeRecurso("O valor a ser consumido não pode ser negativo.")

        self._atualizar_regeneracao()

        if self.atual >= valor:
            self.atual -= valor
            return True
        return False

    def adicionar(self, valor: float):
        """Adiciona uma quantidade ao recurso, sem exceder o máximo."""
        if valor < 0:
            raise ErroDeRecurso("O valor a ser adicionado não pode ser negativo.")
        self._atualizar_regeneracao()
        self.atual = min(self.maxima, self.atual + valor)

    def alterar_maximo(self, novo_maximo: float, manter_proporcao: bool = True):
        """
        Altera o valor máximo do recurso.
        """
        if novo_maximo <= 0:
            raise ErroDeRecurso("O novo máximo deve ser um valor positivo.")

        if manter_proporcao and self.maxima > 0:
            proporcao_atual = self.atual / self.maxima
            self.atual = novo_maximo * proporcao_atual
        else:
            self.atual = min(self.atual, novo_maximo)

        self.maxima = novo_maximo

    def obter_info(self) -> Dict[str, Any]:
        """Retorna um dicionário com o estado atual do recurso."""
        self._atualizar_regeneracao()
        return {
            "tipo": self.tipo,
            "atual": self.atual,
            "maxima": self.maxima,
            "porcentagem": (self.atual / self.maxima) * 100 if self.maxima > 0 else 0
        }

    def __repr__(self):
        return f"<{self.tipo}: {self.atual:.1f}/{self.maxima:.1f}>"
