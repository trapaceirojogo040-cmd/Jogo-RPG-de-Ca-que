# -*- coding: utf-8 -*-
"""
Testes Unitários para o Sistema de Log (v2.0).
"""
import unittest
from apolo_engine.core.logger import MotorLogger, ErroDeLog

class TestLoggerV2(unittest.TestCase):
    """Conjunto de testes para a nova classe MotorLogger."""

    def setUp(self):
        """Configura um novo logger para cada teste."""
        self.logger = MotorLogger(tamanho_maximo=10)

    def test_registrar_evento_sucesso(self):
        """Testa se o registro de um evento válido funciona."""
        id_evento = self.logger.registrar("teste", "info", {"dado": 1})
        self.assertIsInstance(id_evento, str)
        self.assertEqual(len(self.logger.eventos), 1)
        self.assertEqual(self.logger.eventos[0].origem, "teste")

    def test_registrar_evento_falha_com_dados_invalidos(self):
        """Testa se o registro falha com origem ou tipo vazios."""
        with self.assertRaises(ErroDeLog):
            self.logger.registrar("", "info", {})
        with self.assertRaises(ErroDeLog):
            self.logger.registrar("teste", "", {})

    def test_limite_de_tamanho_do_log(self):
        """Garante que o log não excede o tamanho máximo definido."""
        for i in range(15):
            self.logger.registrar("loop", "numero", {"i": i})
        self.assertEqual(len(self.logger.eventos), 10)
        # Verifica se os primeiros eventos foram descartados
        self.assertEqual(self.logger.eventos[0].dados["i"], 5)

    def test_consulta_com_filtros(self):
        """Testa a funcionalidade de consulta com diferentes filtros."""
        self.logger.registrar("sistema", "inicio", {})
        self.logger.registrar("jogador", "acao", {})
        self.logger.registrar("sistema", "erro", {})

        self.assertEqual(len(self.logger.consultar(origem="sistema")), 2)
        self.assertEqual(len(self.logger.consultar(tipo="acao")), 1)
        self.assertEqual(len(self.logger.consultar(origem="sistema", tipo="erro")), 1)
        self.assertEqual(len(self.logger.consultar(limite=2)), 2)

    def test_obter_estatisticas(self):
        """Testa se as estatísticas do log são geradas corretamente."""
        self.logger.registrar("sistema", "inicio", {})
        self.logger.registrar("jogador", "acao", {})
        self.logger.registrar("sistema", "inicio", {})

        stats = self.logger.obter_estatisticas()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["tipos"]["inicio"], 2)
        self.assertEqual(stats["origens"]["jogador"], 1)

if __name__ == '__main__':
    unittest.main()
