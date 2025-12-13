# -*- coding: utf-8 -*-
"""
Testes Unitários para o Sistema Guardian (v2.0).
"""
import unittest
from apolo_engine.tools.guardian import Guardian

class TestGuardianV2(unittest.TestCase):
    """Conjunto de testes para a nova ferramenta Guardian e seus componentes."""

    def setUp(self):
        """Cria uma nova instância do Guardian para cada teste."""
        self.guardian = Guardian()
        self.codigo_exemplo_simples = """
import os

class MinhaClasse:
    def meu_metodo(self, arg1):
        if arg1 > 0:
            return True
        return False
"""
        self.codigo_exemplo_complexo = """
from apolo_engine.core.eventos import Evento

class SistemaDeCombate:
    def __init__(self):
        self.rpg = "mundo"

    def calcular_dano(self, a, b):
        # Lógica de combate
        return a - b
"""

    def test_analise_de_arquivo_estrutura(self):
        """Verifica se o analisador estrutural extrai as informações corretamente."""
        relatorio = self.guardian.analisar_arquivo("simples.py", self.codigo_exemplo_simples)
        estrutura = relatorio["estrutura"]

        self.assertEqual(len(estrutura["classes"]), 1)
        self.assertEqual(estrutura["classes"][0]["nome"], "MinhaClasse")
        self.assertEqual(len(estrutura["funcoes"]), 1)
        self.assertEqual(estrutura["funcoes"][0]["nome"], "meu_metodo")

    def test_analise_de_arquivo_semantica(self):
        """Testa se o analisador semântico detecta os conceitos corretos."""
        relatorio = self.guardian.analisar_arquivo("complexo.py", self.codigo_exemplo_complexo)
        semantica = relatorio["semantica"]

        self.assertIn("combate", semantica["conceitos_detectados"])
        self.assertIn("rpg", semantica["conceitos_detectados"])
        self.assertIn("mundo", semantica["conceitos_detectados"])

    def test_comparacao_de_arquivos_sem_conflitos(self):
        """Verifica se a comparação de dois arquivos diferentes não aponta conflitos."""
        relatorio1 = self.guardian.analisar_arquivo("simples.py", self.codigo_exemplo_simples)
        relatorio2 = self.guardian.analisar_arquivo("complexo.py", self.codigo_exemplo_complexo)

        resultado = self.guardian.comparar_arquivos(relatorio1, relatorio2)
        self.assertEqual(len(resultado["conflitos"]["classes_duplicadas"]), 0)

    def test_comparacao_de_arquivos_com_conflitos(self):
        """Garante que a detecção de conflitos de classe funciona."""
        codigo_conflitante = """
class MinhaClasse: # Mesmo nome do outro arquivo
    pass
"""
        relatorio1 = self.guardian.analisar_arquivo("simples.py", self.codigo_exemplo_simples)
        relatorio2 = self.guardian.analisar_arquivo("conflitante.py", codigo_conflitante)

        resultado = self.guardian.comparar_arquivos(relatorio1, relatorio2)
        self.assertIn("MinhaClasse", resultado["conflitos"]["classes_duplicadas"])

if __name__ == '__main__':
    unittest.main()
