# -*- coding: utf-8 -*-
"""
Sistema Guardian: Ferramenta de Análise Estática de Código.

Este script analisa o código-fonte do motor Apolo para garantir
sua integridade estrutural e semântica. Deve ser executado
separadamente para validar a qualidade do código.
"""
import ast
import os
from typing import List, Dict, Any

class GuardianCodeAnalyzer:
    """
    Realiza uma análise estática no código-fonte do motor.
    """
    def __init__(self, project_root: str = "apolo_engine"):
        self.project_root = project_root
        self.riscos: List[str] = []
        self.mapa_estrutural: Dict[str, Any] = {"classes": [], "funcoes": []}

    def analisar_projeto(self) -> bool:
        """
        Executa todas as fases da análise no projeto.
        """
        print(f"--- GUARDIAN: INICIANDO ANÁLISE DO PROJETO EM '{self.project_root}' ---")

        # 1. Encontrar todos os arquivos Python
        arquivos_py = self._encontrar_arquivos_py()
        if not arquivos_py:
            self.riscos.append("FALHA CRÍTICA: Nenhum arquivo Python encontrado no diretório do projeto.")
            return False

        print(f"Encontrados {len(arquivos_py)} arquivos para análise...")

        # 2. Analisar cada arquivo
        for arquivo in arquivos_py:
            self._analisar_arquivo(arquivo)

        # 3. Realizar checagem semântica global
        self._verificacao_semantica_global()

        # 4. Exibir relatório
        self._exibir_relatorio()

        return not self.riscos

    def _encontrar_arquivos_py(self) -> List[str]:
        """
        Lista todos os arquivos .py no diretório do projeto.
        """
        arquivos_encontrados = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(".py"):
                    arquivos_encontrados.append(os.path.join(root, file))
        return arquivos_encontrados

    def _analisar_arquivo(self, path: str):
        """
        Usa AST para analisar um único arquivo em busca de erros de sintaxe
        e para mapear sua estrutura.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                codigo = f.read()

            tree = ast.parse(codigo)

            # Mapear classes e funções
            self.mapa_estrutural["funcoes"].extend(
                [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            )
            self.mapa_estrutural["classes"].extend(
                [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            )
        except SyntaxError as e:
            self.riscos.append(f"ERRO DE SINTAXE CRÍTICO em '{path}': {e}")
        except Exception as e:
            self.riscos.append(f"ERRO INESPERADO ao analisar '{path}': {e}")

    def _verificacao_semantica_global(self):
        """
        Verifica se as classes e a complexidade do projeto estão dentro do esperado.
        """
        classes_criticas = ["ApoloEngine", "EntidadeBase", "SistemaDeCombate", "SistemaDeFisica"]
        classes_encontradas = self.mapa_estrutural["classes"]

        ausentes = [c for c in classes_criticas if c not in classes_encontradas]
        if ausentes:
            self.riscos.append(f"AVISO: Classes de domínio críticas estão ausentes: {ausentes}")

        if len(classes_encontradas) < 10:
            self.riscos.append(f"INFO: A complexidade de classes ({len(classes_encontradas)}) parece baixa. "
                               "Verifique se todos os sistemas foram implementados.")

    def _exibir_relatorio(self):
        """
        Imprime o resultado final da análise.
        """
        print("\n--- RELATÓRIO DA ANÁLISE GUARDIAN ---")
        print(f"Total de Classes Encontradas: {len(self.mapa_estrutural['classes'])}")
        print(f"Total de Funções Encontradas: {len(self.mapa_estrutural['funcoes'])}")

        if self.riscos:
            print(f"\n[!] {len(self.riscos)} RISCOS OU ERROS DETECTADOS:")
            for i, risco in enumerate(self.riscos, 1):
                print(f"  {i}. {risco}")
        else:
            print("\n[✓] ANÁLISE CONCLUÍDA. Nenhum risco crítico detectado.")
        print("------------------------------------")

if __name__ == "__main__":
    analisador = GuardianCodeAnalyzer()
    analisador.analisar_projeto()
