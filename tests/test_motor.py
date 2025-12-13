# -*- coding: utf-8 -*-
"""
Testes Unitários para o Motor Principal (v2.0).
"""
import unittest
from unittest.mock import Mock, patch
from apolo_engine.motor import ApoloEngine
from apolo_engine.entities.entidade import Entidade

class TestMotorV2(unittest.TestCase):
    """Conjunto de testes para a nova classe ApoloEngine."""

    def setUp(self):
        """Cria um novo motor para cada teste."""
        # Usamos patch para evitar que as instâncias globais interfiram nos testes
        with patch('apolo_engine.motor.LOGGER', Mock()), \
             patch('apolo_engine.motor.BARRAMENTO_DE_EVENTOS', Mock()), \
             patch('apolo_engine.motor.TEMPO', Mock()), \
             patch('apolo_engine.motor.FISICA', Mock()), \
             patch('apolo_engine.motor.COMBATE', Mock()), \
             patch('apolo_engine.motor.IA', Mock()), \
             patch('apolo_engine.motor.CRAFTING', Mock()), \
             patch('apolo_engine.motor.TALENTOS', Mock()):
            self.motor = ApoloEngine()

    def test_iniciar_motor(self):
        """Testa se o motor inicia corretamente e dispara o evento esperado."""
        self.motor.iniciar()
        self.assertTrue(self.motor.iniciado)
        # Verifica se o evento 'MOTOR_INICIADO' foi disparado
        self.motor.eventos.disparar.assert_called_once()
        self.assertEqual(self.motor.eventos.disparar.call_args[0][0].nome, "MOTOR_INICIADO")

    def test_registrar_entidade_com_sucesso(self):
        """Testa o registro de uma nova entidade e sua conexão com os subsistemas."""
        entidade = Entidade("Teste")
        self.motor.registrar_entidade(entidade, controlada_por_ia=True)

        self.assertIn(entidade.id, self.motor.entidades)
        # Verifica se a entidade foi registrada em todos os sistemas relevantes
        self.motor.fisica.registrar_entidade.assert_called_with(entidade)
        self.motor.talentos.registrar_entidade.assert_called_with(entidade)
        self.motor.ia.registrar_entidade.assert_called_with(entidade)

    def test_registrar_entidade_duplicada_falha(self):
        """Garante que registrar a mesma entidade duas vezes levanta um erro."""
        entidade = Entidade("Duplicada")
        self.motor.registrar_entidade(entidade)
        # O erro agora é levantado pelo motor, não pela entidade
        with self.assertRaises(Exception):
            self.motor.registrar_entidade(entidade)

    def test_tick_orquestra_sistemas(self):
        """Verifica se o tick chama os métodos de atualização dos sistemas principais."""
        self.motor.iniciar()
        self.motor.tick()

        # Garante que o tempo e o processamento de eventos são o coração do loop
        self.motor.tempo.tick.assert_called_once()
        self.motor.eventos.processar_fila.assert_called_once()

if __name__ == '__main__':
    unittest.main()
