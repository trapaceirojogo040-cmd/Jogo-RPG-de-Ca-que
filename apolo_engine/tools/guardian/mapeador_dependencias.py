# -*- coding: utf-8 -*-
"""
Componente Guardian: Mapeador de Dependências

Analisa o código para identificar os módulos que ele importa,
ajudando a visualizar as conexões entre diferentes partes do projeto.
"""
import re
from typing import List

class MapeadorDeDependencias:
    """Extrai dependências de importação de um bloco de código."""

    def mapear(self, codigo: str) -> List[str]:
        """
        Usa expressões regulares para encontrar todas as declarações
        de `import` e `from ... import`.
        """
        # Encontra `import modulo` e `from modulo import ...`
        imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_.]+)', codigo, re.MULTILINE)

        # Remove duplicatas e retorna a lista ordenada
        return sorted(list(set(imports)))
