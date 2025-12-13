# -*- coding: utf-8 -*-
"""
Sistema Guardian: Ferramenta de Análise Estática de Código.

Este script analisa o código-fonte do motor Apolo para garantir
sua integridade estrutural, semântica e detectar possíveis conflitos.
"""
import ast
import os
from typing import List, Dict, Any

class GuardianCodeAnalyzer:
    """
    Realiza uma análise estática abrangente no código-fonte do motor.
    """
    def __init__(self, project_root: str = "apolo_engine"):
        self.project_root = project_root
        self.riscos: List[str] = []
        self.mapa_arquivos: Dict[str, Dict[str, Any]] = {}

    def analisar_projeto(self) -> bool:
        """
        Executa todas as fases da análise no projeto.
        """
        print(f"--- GUARDIAN: INICIANDO ANÁLISE DO PROJETO EM '{self.project_root}' ---")

        arquivos_py = self._encontrar_arquivos_py()
        if not arquivos_py:
            self.riscos.append("FALHA CRÍTICA: Nenhum arquivo Python encontrado.")
            return False

        print(f"Encontrados {len(arquivos_py)} arquivos para análise...")

        # 1. Análise individual de cada arquivo
        for arquivo in arquivos_py:
            self._analisar_arquivo(arquivo)

        # 2. Análise global do projeto
        self._verificacao_semantica_global()
        self._detectar_conflitos_de_nome()
        self._detectar_arquivos_suspeitos()

        # 3. Exibir relatório
        self._exibir_relatorio()

        return not self.riscos

    def _encontrar_arquivos_py(self) -> List[str]:
        """Lista todos os arquivos .py no diretório do projeto."""
        arquivos = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(".py"):
                    arquivos.append(os.path.join(root, file))
        return arquivos

    def _analisar_arquivo(self, path: str):
        """Analisa um único arquivo para extrair metadados e estrutura AST."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                codigo = f.read()

            tree = ast.parse(codigo)

            self.mapa_arquivos[path] = {
                "path": path,
                "linhas": codigo.count('\n') + 1,
                "tamanho_kb": len(codigo) / 1024,
                "funcoes": [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
                "classes": [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            }
        except SyntaxError as e:
            self.riscos.append(f"ERRO DE SINTAXE em '{path}': {e}")
        except Exception as e:
            self.riscos.append(f"ERRO INESPERADO ao ler '{path}': {e}")

    def _verificacao_semantica_global(self):
        """Verifica se classes críticas do domínio estão presentes."""
        classes_criticas = ["ApoloEngine", "EntidadeBase", "SistemaDeCombate", "SistemaDeFisica"]
        todas_as_classes = set()
        for dados in self.mapa_arquivos.values():
            todas_as_classes.update(dados["classes"])

        ausentes = [c for c in classes_criticas if c not in todas_as_classes]
        if ausentes:
            self.riscos.append(f"AVISO SEMÂNTICO: Classes de domínio críticas estão ausentes: {ausentes}")

    def _detectar_conflitos_de_nome(self):
        """Detecta funções e classes com o mesmo nome em arquivos diferentes."""
        mapa_funcoes = {}
        mapa_classes = {}

        for path, dados in self.mapa_arquivos.items():
            for func in dados["funcoes"]:
                mapa_funcoes.setdefault(func, []).append(path)
            for cls in dados["classes"]:
                mapa_classes.setdefault(cls, []).append(path)

        # A verificação de funções foi removida por gerar muitos falsos positivos com métodos (ex: __init__).
        # A verificação de classes é a mais importante e foi mantida.
        for nome, paths in mapa_classes.items():
            if len(paths) > 1:
                self.riscos.append(f"CONFLITO: Classe '{nome}' duplicada em: {paths}")

    def _detectar_arquivos_suspeitos(self):
        """Verifica se há arquivos muito pequenos ou muito grandes, ignorando __init__.py."""
        for path, dados in self.mapa_arquivos.items():
            # Ignorar arquivos __init__.py que são naturalmente pequenos
            if "__init__.py" in path:
                continue

            if dados["linhas"] < 5:
                self.riscos.append(f"AVISO: Arquivo '{path}' é muito pequeno ({dados['linhas']} linhas).")
            if dados["tamanho_kb"] > 200: # Limite de 200 KB
                self.riscos.append(f"AVISO: Arquivo '{path}' é muito grande ({dados['tamanho_kb']:.1f} KB).")

    def _exibir_relatorio(self):
        """Imprime o resultado final da análise."""
        print("\n--- RELATÓRIO DA ANÁLISE GUARDIAN ---")
        total_classes = sum(len(d["classes"]) for d in self.mapa_arquivos.values())
        total_funcoes = sum(len(d["funcoes"]) for d in self.mapa_arquivos.values())

        print(f"Total de Arquivos Analisados: {len(self.mapa_arquivos)}")
        print(f"Total de Classes Encontradas: {total_classes}")
        print(f"Total de Funções Encontradas: {total_funcoes}")

        if self.riscos:
            print(f"\n[!] {len(self.riscos)} RISCOS OU AVISOS DETECTADOS:")
            for i, risco in enumerate(self.riscos, 1):
                print(f"  {i}. {risco}")
        else:
            print("\n[✓] ANÁLISE CONCLUÍDA. Nenhum risco crítico detectado.")
        print("------------------------------------")

if __name__ == "__main__":
    # Analisa o diretório do projeto e o diretório raiz para uma varredura completa.
    analisador = GuardianCodeAnalyzer(project_root=".")
    analisador.analisar_projeto()
