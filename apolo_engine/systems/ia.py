# -*- coding: utf-8 -*-
"""
Módulo de Inteligência Artificial (IA): Controla o comportamento
das entidades não jogadoras (NPCs).
"""
import random
from typing import Dict, Any

from apolo_engine.entities.entidade import Entidade
from apolo_engine.systems.combate import COMBATE
from apolo_engine.systems.fisica import FISICA
from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento
from apolo_engine.utils.vector2d import Vector2D

class SistemaDeIA:
    """
    Gerencia a tomada de decisão para todas as entidades controladas
    pela IA no jogo.
    """
    def __init__(self):
        self.entidades_controladas: Dict[str, Dict[str, Any]] = {}
        BARRAMENTO_DE_EVENTOS.assinar("TEMPO_AVANCOU", self._on_tick)

    def registrar_entidade(self, entidade: Entidade):
        """
        Adiciona uma entidade ao controle do sistema de IA.
        """
        if entidade.id not in self.entidades_controladas:
            self.entidades_controladas[entidade.id] = {"entidade": entidade, "estado": "PATRULHANDO"}

    def _on_tick(self, evento: Evento):
        """
        A cada tick do jogo, processa a lógica de decisão para cada NPC.
        """
        # Cria uma cópia para evitar problemas se a lista for modificada durante a iteração
        ids_npcs = list(self.entidades_controladas.keys())

        for npc_id in ids_npcs:
            dados_ia = self.entidades_controladas.get(npc_id)
            if not dados_ia: continue

            npc = dados_ia["entidade"]

            # Pular lógica para NPCs mortos
            if npc.hp_atual <= 0:
                # Remove o NPC do controle da IA
                del self.entidades_controladas[npc_id]
                continue

            alvo = self._encontrar_alvo_proximo(npc)
            contexto = {"alvo_proximo": alvo}

            acao = self.decidir_acao(npc, contexto)
            self.executar_acao(npc, acao, contexto)

    def decidir_acao(self, npc: Entidade, contexto: Dict[str, Any]) -> str:
        """
        Lógica de decisão da IA.
        """
        if npc.hp_atual < npc.hp_maximo * 0.3:
            return "FUGIR"
        if contexto.get("alvo_proximo"):
            return "ATACAR"
        return "PATRULHAR"

    def executar_acao(self, npc: Entidade, acao: str, contexto: Dict[str, Any]):
        """
        Traduz a decisão da IA em ações concretas no jogo.
        """
        alvo = contexto.get("alvo_proximo")

        if acao == "ATACAR" and alvo:
            COMBATE.executar_ataque(npc, alvo)

        elif acao == "FUGIR" and alvo:
            direcao_fuga = (FISICA.corpos[npc.id].posicao - FISICA.corpos[alvo.id].posicao).normalizar()
            FISICA.aplicar_forca(npc.id, direcao_fuga * 5)

        elif acao == "PATRULHAR":
            if random.random() < 0.01:
                forca_patrulha = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1)).normalizar()
                FISICA.aplicar_forca(npc.id, forca_patrulha * 2)

    def _encontrar_alvo_proximo(self, npc: Entidade) -> Entidade | None:
        """
        Método auxiliar para encontrar a entidade "inimiga" mais próxima.
        Para simplificar, considera qualquer outra entidade que não seja ela mesma como um alvo potencial.
        """
        corpo_npc = FISICA.corpos.get(npc.id)
        if not corpo_npc: return None

        alvo_mais_proximo = None
        menor_distancia_quadrada = float('inf')

        # BUG CRÍTICO CORRIGIDO: Importa a instância global MOTOR em vez de criar uma nova.
        from apolo_engine.motor import MOTOR

        for outra_entidade in MOTOR.entidades.values():
            if outra_entidade.id == npc.id or outra_entidade.hp_atual <= 0:
                continue

            corpo_outro = FISICA.corpos.get(outra_entidade.id)
            if not corpo_outro: continue

            # Usar distância quadrada para evitar o cálculo da raiz quadrada (mais performático)
            dist_x = corpo_npc.posicao.x - corpo_outro.posicao.x
            dist_y = corpo_npc.posicao.y - corpo_outro.posicao.y
            distancia_quadrada = dist_x**2 + dist_y**2

            if distancia_quadrada < menor_distancia_quadrada:
                menor_distancia_quadrada = distancia_quadrada
                alvo_mais_proximo = outra_entidade

        return alvo_mais_proximo

# Instância única global
IA = SistemaDeIA()
