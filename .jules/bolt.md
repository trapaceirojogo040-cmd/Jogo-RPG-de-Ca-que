# Bolt's Journal

## 2025-05-22 - O(1) Role Lookups and Flat Thresholds
**Optimization:** Replaced `list.index()` with a mapping dictionary and `for` loops with `if/elif` chains.
**Reason:** Performance measurements showed `list.index()` is O(n) and slower for frequent lookups, while list iteration for fixed thresholds is significantly slower than direct comparisons.
**Impact:** ~14% faster for role lookups and ~80% faster for rank calculation.
