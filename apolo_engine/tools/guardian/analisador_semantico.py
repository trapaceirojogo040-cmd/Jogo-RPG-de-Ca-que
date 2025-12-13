# -*- coding: utf-8 -*-
"""
Componente Guardian: Analisador Semântico

Analisa o código para extrair seu "significado" ou "propósito",
buscando por palavras-chave de domínio e calculando uma métrica de complexidade.
"""
from typing import Dict, Any

class AnalisadorSemantico:
    """Extrai o contexto semântico de um bloco de código."""

    CONCEITOS_CHAVE = {
        "motor", "engine", "militar", "mundo", "rpg", "jogador",
        "economia", "ia", "combate", "inventario", "item",
        "classe", "magia", "unificacao", "multiverso", "entidade"
    }

    def analisar(self, codigo: str) -> Dict[str, Any]:
        """Busca por conceitos-chave e calcula a complexidade do código."""
        codigo_lower = codigo.lower()

        conceitos = [
            conceito for conceito in self.CONCEITOS_CHAVE if conceito in codigo_lower
        ]

        return {
            "conceitos_detectados": conceitos,
            "complexidade_estimada": self._calcular_complexidade(codigo_lower)
        }

    def _calcular_complexidade(self, codigo_lower: str) -> int:
        """Estima a complexidade com base em estruturas de controle."""
        estruturas = ["if", "for", "while", "def", "class", "try", "except"]
        contagem = sum(codigo_lower.count(estrutura) for estrutura in estruturas)
        return min(10, contagem // 5) # Normaliza para uma escala de 0-10

    def calcular_similaridade(self, semantica1: Dict[str, Any], semantica2: Dict[str, Any]) -> float:
        """Calcula a similaridade Jaccard entre dois conjuntos de conceitos."""
        conceitos1 = set(semantica1.get("conceitos_detectados", []))
        conceitos2 = set(semantica2.get("conceitos_detectados", []))

        if not conceitos1 and not conceitos2:
            return 1.0

        interseccao = len(conceitos1.intersection(conceitos2))
        uniao = len(conceitos1.union(conceitos2))

        return interseccao / uniao if uniao > 0 else 0
