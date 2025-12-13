# -*- coding: utf-8 -*-
"""
Módulo de Talentos: Gerencia a progressão de habilidades e a
aplicação de bônus para as entidades.
"""
from typing import Dict, List, NamedTuple, Optional

from apolo_engine.entities.entidade_base import EntidadeBase
from apolo_engine.core.logger import LOGGER

# ---------------------------------------------------------------------------------------------------------
# Estruturas de Dados
# ---------------------------------------------------------------------------------------------------------

class Talento(NamedTuple):
    """
    Estrutura que define um talento, seus bônus e requisitos.
    """
    nome: str
    descricao: str
    bonus: Dict[str, float]  # "atributo" -> valor_bonus (ex: {"ataque": 10, "hp_max": 50})
    pre_requisitos: List[str] = []  # Lista de nomes de talentos necessários

# ---------------------------------------------------------------------------------------------------------
# Componente de Talentos (Anexado a uma Entidade)
# ---------------------------------------------------------------------------------------------------------

class ArvoreDeTalentosComponente:
    """
    Gerencia os talentos e pontos de uma entidade específica.
    """
    def __init__(self, entidade_id: str):
        self.entidade_id = entidade_id
        self.pontos_disponiveis = 0
        self.talentos_desbloqueados: List[str] = []

# ---------------------------------------------------------------------------------------------------------
# Sistema de Talentos
# ---------------------------------------------------------------------------------------------------------

class SistemaDeTalentos:
    """
    Gerencia as árvores de talentos do jogo e a lógica de desbloqueio.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SistemaDeTalentos, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        # "classe_personagem" -> {"nome_talento": Talento}
        self.arvores_de_talentos: Dict[str, Dict[str, Talento]] = {}
        # "entidade_id" -> ArvoreDeTalentosComponente
        self.componentes: Dict[str, ArvoreDeTalentosComponente] = {}
        self._inicializado = True

    def registrar_arvore_para_classe(self, nome_classe: str, talentos: List[Talento]):
        """
        Registra uma lista de talentos como a árvore para uma classe de personagem.
        """
        if nome_classe not in self.arvores_de_talentos:
            self.arvores_de_talentos[nome_classe] = {t.nome: t for t in talentos}
            LOGGER.registrar("SistemaDeTalentos", "arvore_registrada", {"classe": nome_classe})

    def registrar_entidade(self, entidade: EntidadeBase):
        """
        Cria um componente de árvore de talentos para uma entidade.
        """
        if entidade.id not in self.componentes:
            self.componentes[entidade.id] = ArvoreDeTalentosComponente(entidade.id)

    def desbloquear_talento(self, entidade_id: str, nome_talento: str, nome_classe_entidade: str) -> bool:
        """
        Tenta desbloquear um talento para uma entidade.
        """
        componente = self.componentes.get(entidade_id)
        arvore = self.arvores_de_talentos.get(nome_classe_entidade)

        if not componente or not arvore: return False

        talento = arvore.get(nome_talento)
        if not talento: return False

        # 1. Verificar pontos
        if componente.pontos_disponiveis < 1: return False
        # 2. Verificar se já não foi desbloqueado
        if nome_talento in componente.talentos_desbloqueados: return False
        # 3. Verificar pré-requisitos
        for req in talento.pre_requisitos:
            if req not in componente.talentos_desbloqueados: return False

        # Desbloquear
        componente.pontos_disponiveis -= 1
        componente.talentos_desbloqueados.append(nome_talento)

        # Aplicar bônus (em um motor real, isso seria um evento ou um sistema de stats)
        # Por simplicidade, vamos registrar no log.
        LOGGER.registrar("SistemaDeTalentos", "talento_desbloqueado", {
            "entidade": entidade_id, "talento": nome_talento, "bonus": talento.bonus
        })
        return True

# Instância única global
TALENTOS = SistemaDeTalentos()
