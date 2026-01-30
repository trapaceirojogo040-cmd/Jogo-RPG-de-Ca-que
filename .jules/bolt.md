## 2025-05-14 - Optimization of XP Ranking and Cargo Lookups
**Learning:** In Python, direct `if/elif/else` chains for small, fixed threshold checks (like XP ranks) are significantly faster (~75% improvement) than iterating through a list of limits and tags. Additionally, using a dictionary for lookups instead of `list.index()` provides a measurable performance gain (~40% improvement for a small list like CARGOS) by moving from O(n) to O(1) complexity.
**Action:** Always prefer `if/elif/else` for static threshold checks and dictionaries for frequent index-based lookups.
