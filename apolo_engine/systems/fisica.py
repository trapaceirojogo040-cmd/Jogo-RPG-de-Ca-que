# -*- coding: utf-8 -*-
"""
Módulo de Física: Gerencia o movimento, posição e colisão
das entidades no mundo do jogo.
"""
from typing import Dict

from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento
from apolo_engine.utils.vector2d import Vector2D
from apolo_engine.entities.entidade_base import EntidadeBase

# ---------------------------------------------------------------------------------------------------------
# Corpo Físico (Componente)
# ---------------------------------------------------------------------------------------------------------

class CorpoFisico:
    """
    Componente que adiciona propriedades físicas a uma entidade.
    """
    def __init__(self, entidade: EntidadeBase, raio_colisao: float = 1.0):
        self.entidade_id = entidade.id
        self.posicao = Vector2D(0, 0)
        self.velocidade = Vector2D(0, 0)
        self.aceleracao = Vector2D(0, 0)
        self.raio_colisao = raio_colisao  # Simplificação para colisões circulares

# ---------------------------------------------------------------------------------------------------------
# Sistema de Física
# ---------------------------------------------------------------------------------------------------------

class SistemaDeFisica:
    """
    Processa as atualizações de movimento e detecta colisões para
    todos os Corpos Físicos registrados.
    """
    _instancia = None

    def __init__(self):
        self.corpos: Dict[str, CorpoFisico] = {}
        BARRAMENTO_DE_EVENTOS.assinar("TEMPO_AVANCOU", self._on_tick)

    def registrar_entidade(self, entidade: EntidadeBase, raio_colisao: float = 1.0):
        """
        Cria um CorpoFisico para uma entidade e o adiciona ao sistema.
        """
        if entidade.id not in self.corpos:
            corpo = CorpoFisico(entidade, raio_colisao)
            self.corpos[entidade.id] = corpo

    def aplicar_forca(self, entidade_id: str, forca: Vector2D):
        """
        Aplica uma força a um corpo, alterando sua aceleração.
        (Assumindo massa = 1 para simplificar: F = a)
        """
        if entidade_id in self.corpos:
            self.corpos[entidade_id].aceleracao += forca

    def _on_tick(self, evento: Evento):
        """
        Atualiza a física do mundo a cada passo de tempo.
        """
        delta_s = evento.dados.get("delta_s", 0.0)
        if delta_s == 0:
            return

        # 1. Atualizar Posições (integração de Euler simples)
        for corpo in self.corpos.values():
            corpo.velocidade += corpo.aceleracao * delta_s
            corpo.posicao += corpo.velocidade * delta_s
            corpo.aceleracao = Vector2D(0, 0)  # Reseta a aceleração após aplicá-la

        # 2. Detectar Colisões
        ids_corpos = list(self.corpos.keys())
        for i in range(len(ids_corpos)):
            for j in range(i + 1, len(ids_corpos)):
                id_a, id_b = ids_corpos[i], ids_corpos[j]
                corpo_a = self.corpos[id_a]
                corpo_b = self.corpos[id_b]

                distancia_vec = corpo_a.posicao - corpo_b.posicao
                if distancia_vec.magnitude < (corpo_a.raio_colisao + corpo_b.raio_colisao):
                    BARRAMENTO_DE_EVENTOS.disparar(
                        Evento(
                            nome="COLISAO_DETECTADA",
                            origem="SistemaDeFisica",
                            gravidade=2,
                            dados={"entidade_a": id_a, "entidade_b": id_b}
                        )
                    )

# Instância única global
FISICA = SistemaDeFisica()
