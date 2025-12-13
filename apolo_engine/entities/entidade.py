# -*- coding: utf-8 -*-
"""
Módulo da Entidade: Define a estrutura fundamental para todos os objetos
interativos do jogo, com validação e funcionalidades aprimoradas.
"""
import uuid
from typing import List, Dict, Any

from apolo_engine.core.eventos import BARRAMENTO_DE_EVENTOS, Evento
from apolo_engine.core.logger import LOGGER
from apolo_engine.entities.recursos import RecursoEnergetico

# ============================================================
# EXCEÇÕES
# ============================================================

class ErroDeEntidade(Exception):
    """Exceção para erros relacionados a entidades."""
    pass

# ============================================================
# CLASSE PRINCIPAL DA ENTIDADE
# ============================================================

class Entidade:
    """
    Classe aprimorada para tudo que existe e interage no mundo do jogo.
    Inclui validação de dados, atributos de RPG, recursos e mecânicas de IA.
    """
    def __init__(self, nome: str, nivel: int = 1, classe: str = "Indefinida",
                 hp_base: float = 100.0, energia_base: float = 500.0):
        if not nome:
            raise ErroDeEntidade("O nome da entidade é obrigatório.")
        if nivel < 1:
            raise ErroDeEntidade("O nível da entidade deve ser no mínimo 1.")

        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = nivel
        self.classe = classe

        # Atributos de RPG
        self.hp_maximo = hp_base + (nivel * 10)
        self.hp_atual = self.hp_maximo
        self.defesa = nivel * 2 # Simplificado por enquanto
        self.ataque = nivel * 5 # Simplificado por enquanto

        # Sistemas de Recursos
        self.energia = RecursoEnergetico(
            maxima=energia_base + (nivel * 25),
            regeneracao_por_segundo=5.0 + (nivel * 0.5)
        )

        # Inventário e Habilidades
        self.inventario: List[str] = []
        self.habilidades: List[str] = []

        # Atributos de IA
        self.afeto = 0.0     # Relacionamento com jogador/facção (-100 a 100)
        self.volicao = 1.0   # Vontade de agir / Inteligência (0.1 a 10.0)

    def receber_dano(self, valor: float) -> float:
        """
        Processa o dano recebido pela entidade. O valor já deve ter a defesa calculada.
        """
        if self.esta_morta():
            # Não pode receber dano se já estiver morta
            return 0
        if valor < 0:
            raise ErroDeEntidade("O valor do dano não pode ser negativo.")

        dano_recebido = max(0, valor)
        self.hp_atual = max(0, self.hp_atual - dano_recebido)

        BARRAMENTO_DE_EVENTOS.disparar(
            Evento(
                nome="ENTIDADE_RECEBEU_DANO",
                origem="Entidade",
                gravidade=3,
                dados={"alvo_id": self.id, "dano": dano_recebido, "hp_restante": self.hp_atual}
            )
        )

        if self.esta_morta():
            self.morrer()

        return dano_recebido

    def curar(self, valor: float) -> float:
        """Cura a entidade, retornando o valor de vida realmente recuperado."""
        if self.esta_morta() or valor <= 0:
            return 0

        hp_antes = self.hp_atual
        self.hp_atual = min(self.hp_maximo, self.hp_atual + valor)
        cura_real = self.hp_atual - hp_antes

        if cura_real > 0:
             BARRAMENTO_DE_EVENTOS.disparar(
                Evento(
                    nome="ENTIDADE_CURADA",
                    origem="Entidade",
                    gravidade=2,
                    dados={"alvo_id": self.id, "cura": cura_real, "hp_atual": self.hp_atual}
                )
            )
        return cura_real

    def morrer(self):
        """Dispara o evento de morte da entidade."""
        BARRAMENTO_DE_EVENTOS.disparar(
            Evento(
                nome="ENTIDADE_DESTRUIDA",
                origem="Entidade",
                gravidade=5,
                dados={"id": self.id, "nome": self.nome}
            )
        )

    def esta_viva(self) -> bool:
        return self.hp_atual > 0

    def esta_morta(self) -> bool:
        return not self.esta_viva()

    def alterar_afeto(self, delta: float) -> float:
        """Altera o afeto, respeitando os limites de -100 a 100."""
        self.afeto = max(-100.0, min(100.0, self.afeto + delta))
        return self.afeto

    def alterar_volicao(self, delta: float) -> float:
        """Altera a volição, respeitando os limites de 0.1 a 10.0."""
        self.volicao = max(0.1, min(10.0, self.volicao + delta))
        return self.volicao

    def obter_info(self) -> Dict[str, Any]:
        """Retorna um dicionário com o estado completo da entidade."""
        return {
            "id": self.id,
            "nome": self.nome,
            "nivel": self.nivel,
            "classe": self.classe,
            "hp_atual": self.hp_atual,
            "hp_maximo": self.hp_maximo,
            "afeto": self.afeto,
            "volicao": self.volicao,
            "esta_viva": self.esta_viva(),
            "energia": self.energia.obter_info()
        }

    def __repr__(self):
        status = "VIVA" if self.esta_viva() else "MORTA"
        return (f"<Entidade '{self.nome}' (Nv {self.nivel}, HP: {self.hp_atual:.0f}/{self.hp_maximo:.0f} [{status}])>")
