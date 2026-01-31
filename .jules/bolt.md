# Bolt's Journal

This journal is for CRITICAL performance learnings only.

## 2025-01-24 - O(1) Role Lookups
**Performance Bottleneck:** Using `list.index()` to find role hierarchy levels in every combat/command action (O(n)).
**Learning:** Frequent lookups in a static list should be optimized using a mapping dictionary.
**Prevention:** Pre-calculate a `CARGOS_ORDEM` dictionary to achieve O(1) lookup complexity for hierarchical roles.
