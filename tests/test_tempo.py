# -*- coding: utf-8 -*-
"""
Testes Unitários para o Sistema de Tempo (v2.0).
"""
import unittest
import time
from datetime import datetime, timedelta
from apolo_engine.core.tempo import MotorDeTempo, ErroDeTempo

class TestTempoV2(unittest.TestCase):
    """Conjunto de testes para a nova classe MotorDeTempo."""

    def setUp(self):
        """Cria um novo motor de tempo para cada teste."""
        self.tempo = MotorDeTempo()

    def test_inicializacao_padrao(self):
        """Verifica se o tempo é inicializado corretamente."""
        self.assertEqual(self.tempo.velocidade, 1.0)
        self.assertFalse(self.tempo.pausado)
        self.assertIsInstance(self.tempo.tempo_de_jogo, datetime)

    def test_tick_avanca_tempo(self):
        """Testa se o tick avança o tempo do jogo."""
        tempo_inicial = self.tempo.tempo_de_jogo
        time.sleep(0.01) # Espera um pouco para o tempo real passar
        self.tempo.tick()
        self.assertGreater(self.tempo.tempo_de_jogo, tempo_inicial)

    def test_pausar_e_retomar(self):
        """Garante que o tempo não avança quando pausado."""
        self.tempo.pausar()
        self.assertTrue(self.tempo.pausado)
        tempo_pausado = self.tempo.tempo_de_jogo
        time.sleep(0.01)
        self.tempo.tick()
        self.assertEqual(self.tempo.tempo_de_jogo, tempo_pausado)

        self.tempo.retomar()
        self.assertFalse(self.tempo.pausado)
        self.tempo.tick()
        self.assertGreater(self.tempo.tempo_de_jogo, tempo_pausado)

    def test_definir_velocidade(self):
        """Testa a alteração da velocidade do tempo."""
        self.tempo.definir_velocidade(10.0)
        self.assertEqual(self.tempo.velocidade, 10.0)

        # Testa os limites
        with self.assertRaises(ErroDeTempo):
            self.tempo.definir_velocidade(0.0)
        with self.assertRaises(ErroDeTempo):
            self.tempo.definir_velocidade(100.0)

    def test_avancar_segundos_manualmente(self):
        """Testa a função de avanço manual do tempo."""
        tempo_inicial = self.tempo.tempo_de_jogo
        self.tempo.avancar_segundos(3600) # Avança 1 hora
        tempo_final = self.tempo.tempo_de_jogo
        self.assertEqual(tempo_final, tempo_inicial + timedelta(seconds=3600))

if __name__ == '__main__':
    unittest.main()
