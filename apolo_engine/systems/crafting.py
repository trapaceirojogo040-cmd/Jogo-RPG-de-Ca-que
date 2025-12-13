# -*- coding: utf-8 -*-
"""
Módulo de Crafting: Gerencia as receitas e o processo de criação de
itens a partir de outros.
"""
from typing import Dict, NamedTuple

from apolo_engine.entities.inventario import Inventario
from apolo_engine.core.logger import LOGGER

# ---------------------------------------------------------------------------------------------------------
# Estruturas de Dados
# ---------------------------------------------------------------------------------------------------------

class Receita(NamedTuple):
    """
    Estrutura de dados imutável para representar uma receita de crafting.
    """
    ingredientes: Dict[str, int]  # "item_id" -> quantidade_necessaria
    item_resultante: str          # "item_id" do item criado
    quantidade_resultante: int = 1

# ---------------------------------------------------------------------------------------------------------
# Sistema de Crafting
# ---------------------------------------------------------------------------------------------------------

class SistemaDeCrafting:
    """
    Gerencia o registro de receitas e a lógica de criação de itens.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SistemaDeCrafting, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        self.receitas: Dict[str, Receita] = {}
        self._inicializado = True
        LOGGER.registrar("SistemaDeCrafting", "inicio", {"mensagem": "Sistema de crafting inicializado."})

    def registrar_receita(self, nome_receita: str, receita: Receita):
        """
        Adiciona uma nova receita ao sistema.

        Args:
            nome_receita (str): O nome único da receita (ex: "espada_de_ferro").
            receita (Receita): O objeto Receita contendo os detalhes.
        """
        if nome_receita not in self.receitas:
            self.receitas[nome_receita] = receita
            LOGGER.registrar("SistemaDeCrafting", "receita_registrada", {"receita": nome_receita})

    def craftar(self, inventario: Inventario, nome_receita: str) -> bool:
        """
        Tenta criar um item a partir de uma receita usando os itens de um inventário.

        Args:
            inventario (Inventario): O inventário do personagem que está tentando criar o item.
            nome_receita (str): O nome da receita a ser usada.

        Returns:
            bool: True se o item foi criado com sucesso, False caso contrário.
        """
        receita = self.receitas.get(nome_receita)
        if not receita:
            LOGGER.registrar("SistemaDeCrafting", "craft_falhou", {"motivo": f"Receita '{nome_receita}' não encontrada."})
            return False

        # 1. Verificar se há ingredientes suficientes
        for item_req, qtd_req in receita.ingredientes.items():
            if not inventario.tem_item(item_req, qtd_req):
                LOGGER.registrar("SistemaDeCrafting", "craft_falhou", {
                    "receita": nome_receita,
                    "motivo": f"Faltam ingredientes: {item_req} ({qtd_req})"
                })
                return False

        # 2. Consumir os ingredientes
        for item_req, qtd_req in receita.ingredientes.items():
            inventario.remover_item(item_req, qtd_req)

        # 3. Adicionar o item resultante
        inventario.adicionar_item(receita.item_resultante, receita.quantidade_resultante)

        LOGGER.registrar("SistemaDeCrafting", "craft_sucesso", {
            "receita": nome_receita,
            "item_criado": receita.item_resultante
        })
        return True

# Instância única global
CRAFTING = SistemaDeCrafting()
