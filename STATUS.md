# Status — RL for Reachability

## Identification

- Paper: Reinforcement Learning for Reachability: Guaranteeing Asymptotic Optimality
- Authors: Amogh Palasamudram, Jakub Svoboda, Suguman Bansal, Krishnendu Chatterjee
- Source: arXiv:2605.24740
- Venue marker: ICML 2026
- OpenReview identifier: ga20H0vR6f
- HTML source SHA-256: 59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2
- Former repository: icml26-repro-ga20H0vR6f-reinforcement-learning-for-reachability-guaranteeing-asymptotic-optimality
- Current repository: icml26-rl-reachability-asymptotic-optimality
- Canonical branch: main

## Scientific checkpoint

| Claim | Verdict | Evidence checkpoint |
| --- | --- | --- |
| 1 / Theorem 3.1 | VERIFIED | Existential PAC proof, exact minimum-N calibration across six regimes, adaptive tail checker, and failing controls. |
| 2 / Theorem 3.2 | VERIFIED | Strict-gap event inclusion and independent rational-spectrum enumeration; equality boundary is rejected as a control. |
| 3 / Theorem 3.3 | VERIFIED | Exact geometric tail, union-bound limit, first Borel–Cantelli inference, and harmonic divergence control. |
| 4 / Theorem 4.1 | VERIFIED under rational/halting assumptions | Universal denominator certificate plus complete four-state denominator-2 calibration; zero branch retained. |
| 5 / Section 5.1 | PENDING | Author implementation, official QVBS inputs, runner, checker, and controls are prepared; complete 90-trial evidence is still required. |

## Reproduction checkpoint

- Fixed command: uv sync --frozen && uv run --frozen python -m repro.run
- Runtime: dependency-free Python 3.10–3.13 with uv.lock
- Historical compute: Hugging Face cpu-upgrade
- Claim 5 protocol: nine named QVBS models × ten fixed-seed trials
- Author implementation pin: 6ffec1273326aede50c8b6516cea1ceb8d920faa
- QVBS source pin: c7324a311475ba1a3f40e36a324e32f91e766540

## Publication checkpoint

- Main contains the complete verifier lineage through the Claim 5 runner.
- Per-claim contracts, source audits, methods, limitations, and evaluator pages are committed.
- Historical ORX branches are preserved under descriptive audit/release names after cleanup.
- Claim 5 is not labeled verified without generated 90-trial raw evidence.
