# Claim 2 source audit

- Source: https://ar5iv.labs.arxiv.org/html/2605.24740
- Retrieved: 2026-08-02 (Asia/Kolkata), explicit User-Agent `OpenResearch-Reproduction/1.0 (paper audit; contact via project repository)`
- SHA-256: `59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2`
- Definition anchor: `#S2.SS0.SSS0.Px2.p3`; theorem anchor: `#S3.Thmtheorem2`

The source defines epsilon-optimality inclusively: `J(pi) >= J* - epsilon`. The proof writes `epsilon_k <= epsilon_diff`, but equality allows the first runner-up policy and therefore does not imply exact optimality. This is a proof-boundary defect, not a counterexample to the existential theorem: because `epsilon_k` tends to zero and `epsilon_diff > 0`, a strictly later `K_opt` always satisfies `epsilon_k < epsilon_diff`. The current contract uses that valid strict witness and exposes equality as a negative control.
