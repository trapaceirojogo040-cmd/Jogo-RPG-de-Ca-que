# -*- coding: utf-8 -*-
"""
Módulo da Entidade Base: Define a estrutura fundamental para todos
os objetos interativos do jogo (personagens, NPCs, monstros, etc.).
"""
import uuid
from typing import List

from apolo_engine.core.eventos import EVENT_BUS, Evento
from apolo_engine.core.logger import LOGGER
from apolo_engine.entities.recursos import Energia

class EntidadeBase:
    """
    Classe base para tudo que existe e interage no mundo do jogo.
    Inclui atributos de RPG, recursos de energia e mecânicas de IA.
    """
    def __init__(self, nome: str, nivel: int = 1, classe: str = "Indefinida"):
        """
        Args:
            nome (str): O nome da entidade.
            nivel (int): O nível de poder da entidade.
            classe (str): A classe ou tipo da entidade (ex: "Guerreiro", "Monstro").
        """
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = nivel
        self.classe = classe

        # Atributos de RPG
        self.hp_max = 100 + (nivel * 10)
        self.hp_atual = self.hp_max
        self.defesa = nivel * 2
        self.ataque = nivel * 5

        # Sistemas de Recursos
        self.energia = Energia(maxima=500 + (nivel * 25), regeneracao_por_segundo=5.0)

        # Inventário (simplificado por enquanto)
        self.inventario: List[str] = []

        # Atributos de IA (para NPCs)
        self.afeto = 0.0     # Relacionamento com jogador/facção (-100 a 100)
        self.volicao = 1.0   # Vontade de agir / Inteligência (0.1 a 10.0)

    def receber_dano(self, valor: float, origem: str):
        """
        Processa o dano recebido pela entidade, aplicando o valor de dano JÁ CALCULADO
        e disparando os eventos correspondentes.

        Args:
            valor (float): O valor LÍQUIDO do dano (defesa já foi aplicada).
            origem (str): O nome da entidade ou sistema que causou o dano.
        """
        dano_recebido = max(0, valor)  # Garante que o dano não seja negativo
        self.hp_atual = max(0, self.hp_atual - dano_recebido)

        EVENT_BUS.disparar(
            Evento(
                nome="DANO_RECEBIDO",
                origem=origem,
                gravidade=3,
                dados={"alvo_id": self.id, "dano": dano_recebido, "hp_restante": self.hp_atual}
            )
        )
        LOGGER.registrar(self.nome, "dano", {"dano": dano_recebido, "hp_restante": self.hp_atual})

        if self.hp_atual == 0:
            self.morrer()

    def curar(self, valor: float):
        """
        Cura a entidade, restaurando seus pontos de vida.

        Args:
            valor (float): A quantidade de HP a ser restaurada.
        """
        self.hp_atual = min(self.hp_max, self.hp_atual + valor)
        LOGGER.registrar(self.nome, "cura", {"valor": valor, "hp_atual": self.hp_atual})

    def morrer(self):
        """
        Processa a morte da entidade, disparando um evento crítico.
        """
        EVENT_BUS.disparar(
            Evento(
                nome="ENTIDADE_DESTRUIDA",
                origem="SistemaDeEntidades",
                gravidade=5,
                dados={"id": self.id, "nome": self.nome, "nivel": self.nivel}
            )
        )
        LOGGER.registrar(self.nome, "morte", {"mensagem": f"A entidade {self.nome} foi destruída."})

    def usar_habilidade(self, custo_energia: float) -> bool:
        """
        Tenta consumir energia para usar uma habilidade.

        Args:
            custo_energia (float): A quantidade de energia necessária.

        Returns:
            bool: True se a habilidade pôde ser usada, False caso contrário.
        """
        if self.energia.consumir(custo_energia):
            LOGGER.registrar(self.nome, "habilidade", {"custo": custo_energia})
            return True
        LOGGER.registrar(self.nome, "habilidade_falhou", {"motivo": "Energia insuficiente"})
        return False

    def __repr__(self):
        return (f"<Entidade '{self.nome}' (Nv {self.nivel}, HP: {int(self.hp_atual)}/{int(self.hp_max)}, "
                f"Energia: {self.energia.atual:.1f})>")
