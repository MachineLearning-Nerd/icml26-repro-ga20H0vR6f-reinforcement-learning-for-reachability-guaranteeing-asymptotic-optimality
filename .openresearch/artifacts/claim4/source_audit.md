# Claim 4 source audit

- Source: https://ar5iv.labs.arxiv.org/html/2605.24740
- Retrieved: 2026-08-02 (Asia/Kolkata), explicit User-Agent `OpenResearch-Reproduction/1.0 (paper audit; contact via project repository)`
- SHA-256: `59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2`
- Main anchor: `#S4.Thmtheorem1`; technical assumptions and proof: Appendix F, `#A6`

The exact theorem is a disjunction: the L1 value-vector gap is either zero or at least the positive bound. The judged baseline omitted the `or zero` branch when presenting its result. Appendix F additionally restricts this section to rational probabilities and assumes a halting MDP, meaning every policy eventually reaches a terminal goal/reward state. Those assumptions are part of the contract.

Let `B = (2D)^(|A||S|) 2^|S|`. The Appendix-F argument bounds every policy-value denominator by `B`. For two unequal rational components `p/q` and `p'/q'`, the integer `pq' - p'q` is nonzero, so the absolute difference is at least `1/(qq') >= 1/B^2`. The L1 gap is at least any nonzero component gap. This gives the stated bound; equal vectors take the theorem's zero branch.
