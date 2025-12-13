# -*- coding: utf-8 -*-
"""
Módulo do Motor Principal: Orquestra todos os sistemas e gerencia
o ciclo de vida do jogo.
"""
from typing import Dict

from apolo_engine.core.logger import LOGGER
from apolo_engine.core.eventos import EVENT_BUS
from apolo_engine.core.tempo import TEMPO
from apolo_engine.systems.fisica import FISICA
from apolo_engine.systems.combate import COMBATE
from apolo_engine.systems.crafting import CRAFTING
from apolo_engine.systems.talentos import TALENTOS
from apolo_engine.entities.entidade_base import EntidadeBase

class ApoloEngine:
    """
    Classe central que gerencia o loop principal do jogo e a
    interação entre os diferentes sistemas.
    """
    def __init__(self):
        self.entidades: Dict[str, EntidadeBase] = {}
        self.iniciado = False

        # Armazena referências aos sistemas singleton para facilitar o acesso
        self.tempo = TEMPO
        self.eventos = EVENT_BUS
        self.fisica = FISICA
        self.combate = COMBATE
        self.crafting = CRAFTING
        self.talentos = TALENTOS

        LOGGER.registrar("ApoloEngine", "inicio", {"mensagem": "Motor Apolo inicializado."})
        self.iniciado = True

    def registrar_entidade(self, entidade: EntidadeBase):
        """
        Adiciona uma nova entidade ao motor e a registra nos sistemas relevantes.
        """
        if entidade.id not in self.entidades:
            self.entidades[entidade.id] = entidade
            self.fisica.registrar_entidade(entidade) # Adiciona um corpo físico
            self.talentos.registrar_entidade(entidade) # Adiciona o componente de talentos
            LOGGER.registrar("ApoloEngine", "entidade_registrada", {"id": entidade.id, "nome": entidade.nome})

    def tick(self):
        """
        Executa um único ciclo de atualização do jogo.
        Esta é a função que deve ser chamada repetidamente no loop principal.
        """
        if not self.iniciado:
            return

        # 1. Avançar o tempo (dispara o evento TEMPO_AVANCOU)
        self.tempo.tick()

        # 2. Processar a fila de eventos (notifica todos os sistemas que assinaram eventos)
        #    A física já é atualizada aqui, pois ela assina o evento TEMPO_AVANCOU.
        self.eventos.processar_fila()

        # 3. Lógica de IA (será adicionada no futuro)
        #    Aqui, a IA decidiria as ações das entidades.

        # 4. Outras lógicas de jogo podem ser adicionadas aqui.

    def encerrar(self):
        """
        Encerra o motor e salva o estado final (se necessário).
        """
        LOGGER.registrar("ApoloEngine", "encerramento", {"mensagem": "Motor Apolo encerrado."})
        self.iniciado = False
