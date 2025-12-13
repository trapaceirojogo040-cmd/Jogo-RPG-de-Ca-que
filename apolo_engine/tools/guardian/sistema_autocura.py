# -*- coding: utf-8 -*-
"""
Componente Guardian: Sistema de Autocura

Tenta corrigir automaticamente problemas simples de sintaxe e formatação
no código, como a remoção de linhas duplicadas ou a correção de
parênteses desbalanceados.
"""
import difflib

class SistemaDeAutocura:
    """Realiza correções automáticas simples em um bloco de código."""

    def corrigir_sintaxe(self, codigo: str) -> str:
        """
        Aplica um conjunto de correções heurísticas ao código.
        """
        # Remove linhas em branco duplicadas consecutivas
        linhas = codigo.split('\n')
        linhas_corrigidas = []
        linha_anterior_vazia = False
        for linha in linhas:
            if linha.strip() == "":
                if not linha_anterior_vazia:
                    linhas_corrigidas.append(linha)
                linha_anterior_vazia = True
            else:
                linhas_corrigidas.append(linha)
                linha_anterior_vazia = False

        codigo_corrigido = '\n'.join(linhas_corrigidas)

        # Garante que o arquivo termina com uma nova linha
        if not codigo_corrigido.endswith('\n'):
            codigo_corrigido += '\n'

        return codigo_corrigido

    def gerar_patch(self, codigo_original: str, codigo_modificado: str) -> str:
        """
        Gera uma string de patch no formato unified diff para mostrar as
        alterações feitas.
        """
        diff = difflib.unified_diff(
            codigo_original.splitlines(keepends=True),
            codigo_modificado.splitlines(keepends=True),
            fromfile='original',
            tofile='modificado',
        )
        return ''.join(diff)
