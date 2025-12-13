# -*- coding: utf-8 -*-
"""
Componente Guardian: Analisador Estrutural

Analisa o código-fonte para extrair sua estrutura, como classes,
funções e imports, usando a árvore de sintaxe abstrata (AST).
"""
import ast
import hashlib
from typing import Dict, Any

class AnalisadorEstrutural:
    """Extrai a estrutura de um bloco de código usando AST."""

    def analisar(self, codigo: str) -> Dict[str, Any]:
        """Analisa o código e retorna um dicionário com a estrutura encontrada."""
        try:
            tree = ast.parse(codigo)
        except SyntaxError as e:
            return {"erro": f"Sintaxe inválida: {e}"}

        funcoes = [
            {"nome": node.name, "linha": node.lineno}
            for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        ]
        classes = [
            {"nome": node.name, "linha": node.lineno}
            for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        ]

        return {
            "funcoes": funcoes,
            "classes": classes,
            "hash_sha256": hashlib.sha256(codigo.encode()).hexdigest()
        }
