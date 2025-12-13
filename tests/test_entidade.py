# -*- coding: utf-8 -*-
"""
Testes Unitários para a classe Entidade (v2.0).
"""
import unittest
from apolo_engine.entities.entidade import Entidade, ErroDeEntidade

class TestEntidadeV2(unittest.TestCase):
    """Conjunto de testes para a nova classe Entidade."""

    def setUp(self):
        """Cria uma entidade padrão para os testes."""
        self.entidade = Entidade(nome="Herói", nivel=5, hp_base=100.0, energia_base=500.0)

    def test_criacao_com_sucesso(self):
        """Testa se a entidade é criada com os atributos corretos."""
        self.assertEqual(self.entidade.nome, "Herói")
        self.assertEqual(self.entidade.nivel, 5)
        self.assertEqual(self.entidade.hp_maximo, 150.0) # 100 + 5 * 10
        self.assertEqual(self.entidade.hp_atual, 150.0)
        self.assertTrue(self.entidade.esta_viva())

    def test_criacao_com_dados_invalidos(self):
        """Garante que a criação falha com nome vazio ou nível inválido."""
        with self.assertRaises(ErroDeEntidade):
            Entidade(nome="", nivel=1)
        with self.assertRaises(ErroDeEntidade):
            Entidade(nome="Vilão", nivel=0)

    def test_receber_dano_e_morrer(self):
        """Testa a lógica de receber dano e o estado de morte."""
        dano_sofrido = self.entidade.receber_dano(50)
        self.assertEqual(dano_sofrido, 50)
        self.assertEqual(self.entidade.hp_atual, 100)
        self.assertTrue(self.entidade.esta_viva())

        # Dano letal
        self.entidade.receber_dano(200)
        self.assertEqual(self.entidade.hp_atual, 0)
        self.assertTrue(self.entidade.esta_morta())

    def test_receber_dano_negativo_falha(self):
        """Verifica se um valor de dano negativo levanta uma exceção."""
        with self.assertRaises(ErroDeEntidade):
            self.entidade.receber_dano(-10)

    def test_cura_e_limite_maximo(self):
        """Testa a lógica de cura e garante que não ultrapassa o HP máximo."""
        self.entidade.receber_dano(100) # HP atual: 50
        cura_recebida = self.entidade.curar(30)
        self.assertEqual(cura_recebida, 30)
        self.assertEqual(self.entidade.hp_atual, 80)

        # Tenta curar além do máximo
        cura_excedente = self.entidade.curar(100)
        self.assertEqual(cura_excedente, 70) # 150 (max) - 80 (atual) = 70
        self.assertEqual(self.entidade.hp_atual, self.entidade.hp_maximo)

    def test_alterar_afeto_e_volicao_com_limites(self):
        """Garante que afeto e volição respeitam seus limites."""
        self.entidade.alterar_afeto(200)
        self.assertEqual(self.entidade.afeto, 100.0)
        self.entidade.alterar_afeto(-300)
        self.assertEqual(self.entidade.afeto, -100.0)

        self.entidade.alterar_volicao(20)
        self.assertEqual(self.entidade.volicao, 10.0)
        self.entidade.alterar_volicao(-15)
        self.assertEqual(self.entidade.volicao, 0.1)

if __name__ == '__main__':
    unittest.main()
