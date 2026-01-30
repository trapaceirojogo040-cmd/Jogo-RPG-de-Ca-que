# Bolt's Journal

This journal is for CRITICAL performance learnings only.

## 2024-05-23 - Otimização de Busca em Listas e Cadeias de Decisão
**Optimization:** Substituição de iteração em listas por cadeias `if/elif` e uso de dicionários para busca O(1) em categorias fixas.
**Reason:** `list.index()` e iterações em listas de limites têm custo O(n). Dicionários e `if/elif` são significativamente mais rápidos em Python para conjuntos pequenos de dados.
**Impact:** Redução do overhead em funções chamadas frequentemente no ciclo principal do jogo (análise de IA e cálculo de patente).
