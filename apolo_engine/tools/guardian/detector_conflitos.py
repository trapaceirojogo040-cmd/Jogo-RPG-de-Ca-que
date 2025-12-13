# -*- coding: utf-8 -*-
"""
Componente Guardian: Detector de Conflitos

Compara as estruturas de dois ou mais arquivos de código para
encontrar nomes de classes ou funções duplicados, o que pode
levar a erros de importação e de lógica.
"""
from typing import Dict, Any, List

class DetectorDeConflitos:
    """Detecta conflitos de nomes entre duas estruturas de código."""

    def detectar(self, estrutura1: Dict[str, Any], estrutura2: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Compara as listas de funções e classes de duas análises estruturais.
        """
        funcoes1 = {f["nome"] for f in estrutura1.get("funcoes", [])}
        funcoes2 = {f["nome"] for f in estrutura2.get("funcoes", [])}

        classes1 = {c["nome"] for c in estrutura1.get("classes", [])}
        classes2 = {c["nome"] for c in estrutura2.get("classes", [])}

        return {
            "funcoes_duplicadas": sorted(list(funcoes1.intersection(funcoes2))),
            "classes_duplicadas": sorted(list(classes1.intersection(classes2)))
        }
