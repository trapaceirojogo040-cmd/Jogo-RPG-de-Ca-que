# -*- coding: utf-8 -*-
"""
Módulo de Combate: Gerencia todos os aspectos das batalhas,
incluindo cálculos de dano, aplicação de status e resolução de ataques.
"""
from apolo_engine.entities.entidade_base import EntidadeBase
from apolo_engine.core.logger import LOGGER

class SistemaDeCombate:
    """
    Processa as interações de combate entre entidades.
    """
    _instancia = None

    def __init__(self):
        LOGGER.registrar("SistemaDeCombate", "inicio", {"mensagem": "Sistema de combate inicializado."})

    def calcular_dano(self, atacante: EntidadeBase, defensor: EntidadeBase, tipo_dano: str = "Físico") -> float:
        """
        Calcula o dano final de um ataque com base nos atributos do atacante e do defensor.

        A fórmula considera o ataque do atacante, seu nível e a defesa do defensor.

        Args:
            atacante (EntidadeBase): A entidade que está realizando o ataque.
            defensor (EntidadeBase): A entidade que está se defendendo.
            tipo_dano (str): O tipo de dano (ex: "Físico", "Nexus"). Não utilizado na fórmula base,
                             mas disponível para expansões com resistências/vulnerabilidades.

        Returns:
            float: O valor final do dano a ser aplicado.
        """
        # Fórmula: (Ataque * (1 + Nível / 50)) - Defesa do Defensor
        dano_base = atacante.ataque * (1 + atacante.nivel / 50.0)

        # Multiplicadores elementais ou de tipo de dano podem ser adicionados aqui.
        # Ex: if tipo_dano == "Nexus" and defensor.classe == "Anti-Nexus": multiplicador = 0.5

        dano_final = max(1.0, dano_base - defensor.defesa) # Garante que o dano mínimo seja sempre 1.

        return dano_final

    def executar_ataque(self, atacante: EntidadeBase, defensor: EntidadeBase, tipo_dano: str = "Físico"):
        """
        Executa uma ação de ataque completa de uma entidade para outra.

        Args:
            atacante (EntidadeBase): A entidade que ataca.
            defensor (EntidadeBase): A entidade que defende.
            tipo_dano (str): O tipo de dano do ataque.
        """
        custo_energia_ataque = 25.0
        if not atacante.usar_habilidade(custo_energia_ataque):
            LOGGER.registrar(atacante.nome, "ataque_falhou", {"motivo": "Energia insuficiente"})
            return

        dano = self.calcular_dano(atacante, defensor, tipo_dano)
        defensor.receber_dano(dano, atacante.nome)

        LOGGER.registrar(atacante.nome, "ataque_executado", {
            "alvo": defensor.nome,
            "dano_calculado": dano,
            "tipo_dano": tipo_dano
        })

# Instância única global
COMBATE = SistemaDeCombate()
