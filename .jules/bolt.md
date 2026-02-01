# Bolt's Performance Journal ⚡

This journal contains CRITICAL performance-related learnings for this project.

## 2025-05-15 - [Hierarchical Role Lookups]
**Learning:** Using `list.index()` on the `CARGOS` list for hierarchical checks creates O(n) overhead in performance-critical paths like command confirmation and AI decision making.
**Action:** Implement a `CARGOS_ORDEM` mapping dictionary to achieve O(1) complexity for role-based lookups. Avoid combining performance optimizations with breaking changes (like renames), as they violate the "No breaking changes" constraint and decouple data from presentation.
