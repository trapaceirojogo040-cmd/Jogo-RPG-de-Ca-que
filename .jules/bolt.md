## 2025-05-14 - O(1) Mapping for Static List Lookups
**Learning:** In Python, using `list.index()` for frequent lookups on static lists introduces $O(n)$ overhead. Even for small lists, this can be optimized to $O(1)$ by pre-calculating a mapping dictionary (hash map).
**Action:** Always check for `.index()` calls on static lists like `CARGOS` and replace them with a pre-computed dictionary mapping if they are used in performance-sensitive paths (like AI decision logic or security protocols).
