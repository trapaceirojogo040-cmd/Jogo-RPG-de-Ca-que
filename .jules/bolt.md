# Bolt's Journal

This journal is for CRITICAL performance learnings only.

## 2025-05-15 - O(1) Role Hierarchy Lookups
**Performance Bottleneck:** Using `list.index()` on the `CARGOS` list for every permission or hierarchy check ($O(n)$).
**Learning:** Frequent lookups in static lists can be optimized by pre-calculating a mapping dictionary.
**Prevention:** Implement a `CARGOS_ORDEM` dictionary to achieve $O(1)$ lookup complexity for role indexes.
