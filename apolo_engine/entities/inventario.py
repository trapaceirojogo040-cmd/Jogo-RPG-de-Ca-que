# -*- coding: utf-8 -*-
"""
Módulo de Inventário: Define um sistema de gerenciamento de itens
que pode ser anexado a qualquer entidade.
"""
from typing import Dict
from apolo_engine.core.logger import LOGGER

class Inventario:
    """
    Componente que gerencia uma coleção de itens para uma entidade,
    rastreando a quantidade de cada um.
    """
    def __init__(self, proprietario_id: str, capacidade: int = 20):
        """
        Args:
            proprietario_id (str): O ID da entidade dona deste inventário.
            capacidade (int): O número máximo de tipos de itens distintos que o inventário pode conter.
        """
        self.proprietario_id = proprietario_id
        self.capacidade = capacidade
        self.itens: Dict[str, int] = {}  # "item_id" -> quantidade

    def adicionar_item(self, item_id: str, quantidade: int = 1) -> bool:
        """
        Adiciona uma certa quantidade de um item ao inventário.

        Args:
            item_id (str): O identificador único do item.
            quantidade (int): A quantidade a ser adicionada.

        Returns:
            bool: True se o item foi adicionado com sucesso, False caso contrário.
        """
        if quantidade <= 0:
            return False

        if item_id in self.itens:
            self.itens[item_id] += quantidade
        else:
            if len(self.itens) >= self.capacidade:
                LOGGER.registrar("Inventario", "adicionar_falhou", {
                    "proprietario": self.proprietario_id,
                    "motivo": "Capacidade máxima atingida"
                })
                return False
            self.itens[item_id] = quantidade

        return True

    def remover_item(self, item_id: str, quantidade: int = 1) -> bool:
        """
        Remove uma certa quantidade de um item do inventário.

        Args:
            item_id (str): O identificador único do item.
            quantidade (int): A quantidade a ser removida.

        Returns:
            bool: True se a remoção foi bem-sucedida, False caso contrário.
        """
        if quantidade <= 0 or item_id not in self.itens:
            return False

        if self.itens[item_id] >= quantidade:
            self.itens[item_id] -= quantidade
            if self.itens[item_id] == 0:
                del self.itens[item_id]
            return True

        return False

    def tem_item(self, item_id: str, quantidade: int = 1) -> bool:
        """
        Verifica se o inventário contém uma quantidade mínima de um item.

        Args:
            item_id (str): O identificador único do item.
            quantidade (int): A quantidade mínima necessária.

        Returns:
            bool: True se a quantidade necessária estiver presente, False caso contrário.
        """
        return self.itens.get(item_id, 0) >= quantidade

    def __repr__(self):
        return f"<Inventario (Proprietário: {self.proprietario_id}, Itens: {len(self.itens)}/{self.capacidade})>"
