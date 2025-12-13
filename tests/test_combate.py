# -*- coding: utf-8 -*-
"""
Testes Unitários para o Sistema de Combate.

Garante que a lógica de cálculo de dano e a execução de ataques
estejam funcionando corretamente.
"""
import unittest

# Silencia os logs durante os testes para manter a saída limpa
from apolo_engine.core.logger import LOGGER
LOGGER.eventos = [] # Limpa logs de execuções anteriores
LOGGER.registrar = lambda *args, **kwargs: None

from apolo_engine.systems.combate import SistemaDeCombate
from apolo_engine.entities.entidade_base import EntidadeBase

class TestSistemaDeCombate(unittest.TestCase):
    """Conjunto de testes para a classe SistemaDeCombate."""

    def setUp(self):
        """
        Configura o ambiente para cada teste.
        Cria um atacante e um defensor padrão.
        """
        self.combate = SistemaDeCombate()
        self.atacante = EntidadeBase(nome="Guerreiro", nivel=10, classe="Guerreiro")
        self.atacante.ataque = 50
        self.atacante.energia.atual = self.atacante.energia.maxima

        self.defensor = EntidadeBase(nome="Goblin", nivel=5, classe="Monstro")
        self.defensor.defesa = 20
        self.defensor.hp_atual = 150

    def test_calcular_dano_base(self):
        """
        Testa se a fórmula de dano base está sendo calculada corretamente.
        Fórmula: (Ataque * (1 + Nível / 50)) - Defesa
        """
        # Dano esperado = (50 * (1 + 10 / 50)) - 20
        # Dano esperado = (50 * 1.2) - 20
        # Dano esperado = 60 - 20 = 40
        dano_calculado = self.combate.calcular_dano(self.atacante, self.defensor)
        self.assertAlmostEqual(dano_calculado, 40.0, places=2)

    def test_dano_minimo_garantido(self):
        """
        Testa se o dano é no mínimo 1, mesmo se a defesa for maior que o ataque.
        """
        self.defensor.defesa = 1000  # Defesa muito alta
        dano_calculado = self.combate.calcular_dano(self.atacante, self.defensor)
        self.assertEqual(dano_calculado, 1.0)

    def test_executar_ataque_aplica_dano(self):
        """
        Verifica se o método executar_ataque de fato reduz o HP do defensor.
        """
        hp_inicial_defensor = self.defensor.hp_atual
        dano_esperado = self.combate.calcular_dano(self.atacante, self.defensor)

        self.combate.executar_ataque(self.atacante, self.defensor)

        hp_final_defensor = self.defensor.hp_atual
        self.assertEqual(hp_final_defensor, hp_inicial_defensor - dano_esperado)

    def test_executar_ataque_falha_sem_energia(self):
        """
        Garante que um ataque não pode ser executado se o atacante não tiver energia.
        """
        self.atacante.energia.atual = 0  # Remove a energia do atacante
        hp_inicial_defensor = self.defensor.hp_atual

        self.combate.executar_ataque(self.atacante, self.defensor)

        hp_final_defensor = self.defensor.hp_atual
        self.assertEqual(hp_final_defensor, hp_inicial_defensor)

if __name__ == '__main__':
    unittest.main()
