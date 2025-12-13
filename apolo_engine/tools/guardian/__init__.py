# -*- coding: utf-8 -*-
"""
Pacote Guardian (v2.0): Sistema unificado de análise e proteção de código.
"""
from .analisador_estrutural import AnalisadorEstrutural
from .analisador_semantico import AnalisadorSemantico
from .mapeador_dependencias import MapeadorDeDependencias
from .detector_conflitos import DetectorDeConflitos
from .sistema_autocura import SistemaDeAutocura
from .gerenciador_memoria import GerenciadorDeMemoria

class Guardian:
    """
    Sistema unificado que combina todos os componentes de análise para
    fornecer uma visão completa da qualidade e integridade do código.
    """
    def __init__(self):
        self.analisador_estrutural = AnalisadorEstrutural()
        self.analisador_semantico = AnalisadorSemantico()
        self.mapeador_dependencias = MapeadorDeDependencias()
        self.detector_conflitos = DetectorDeConflitos()
        self.sistema_autocura = SistemaDeAutocura()
        self.gerenciador_memoria = GerenciadorDeMemoria
        self.relatorios = []

    def analisar_arquivo(self, caminho: str, codigo: str) -> dict:
        """
        Executa uma análise completa em um arquivo de código-fonte.
        """
        codigo_curado = self.sistema_autocura.corrigir_sintaxe(codigo)

        estrutura = self.analisador_estrutural.analisar(codigo_curado)
        semantica = self.analisador_semantico.analisar(codigo_curado)
        dependencias = self.mapeador_dependencias.mapear(codigo_curado)

        relatorio = {
            "arquivo": caminho,
            "estrutura": estrutura,
            "semantica": semantica,
            "dependencias": dependencias,
            "autocura_aplicada": codigo != codigo_curado
        }
        self.relatorios.append(relatorio)
        return relatorio

    def comparar_arquivos(self, relatorio1: dict, relatorio2: dict) -> dict:
        """
        Compara dois relatórios de análise para encontrar conflitos e similaridades.
        """
        conflitos = self.detector_conflitos.detectar(
            relatorio1["estrutura"], relatorio2["estrutura"]
        )
        similaridade = self.analisador_semantico.calcular_similaridade(
            relatorio1["semantica"], relatorio2["semantica"]
        )
        return {"conflitos": conflitos, "similaridade_semantica": similaridade}
