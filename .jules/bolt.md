## 2025-05-15 - [Hierarchical Lookups and XP Ranking]
**Learning:** In this codebase, using a dictionary for role hierarchy lookups is ~14% faster than `list.index()`, and using a flat `if/elif/else` chain for fixed XP thresholds is ~80% faster than list iteration. These patterns are highly effective for the RPG logic which frequently checks ranks and hierarchies.
**Action:** Always prefer dictionary mapping (`CARGOS_ORDEM`) over `list.index()` and `if/elif` chains over loops for static threshold evaluations in performance-critical paths.
