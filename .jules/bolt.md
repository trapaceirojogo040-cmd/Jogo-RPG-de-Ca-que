## 2024-07-16 - Initial Performance Analysis

**Learning:** The `rank_xp` function is inefficient. It uses a linear scan over a list of thresholds, which is slow and scales poorly. For a core function that is likely called frequently, this is a clear performance bottleneck.

**Action:** Replace the linear scan with a more efficient lookup method. A binary search approach using Python's `bisect` module is ideal, as it will reduce the complexity from O(n) to O(log n).
