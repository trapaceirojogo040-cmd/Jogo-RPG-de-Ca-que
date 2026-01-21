## 2024-07-23 - Micro-Optimizations vs. Perceived Impact

**Learning:** My core directive is to implement any *measurable* performance gain, even if it's a micro-optimization. This can conflict with standard engineering principles that reject premature optimizations on non-critical code paths. A senior reviewer correctly flagged my `rank_xp` optimization as non-impactful to the overall application, even though the function itself became 82% faster.

**Action:** I must proceed with such optimizations as they align with my primary goal. However, in my PR descriptions, I must be precise. I will report the specific, measured impact on the function/component I optimized, and avoid making broad claims about overall application performance unless I have data to support it. This correctly frames the work and acknowledges the distinction between local and global optimization.
