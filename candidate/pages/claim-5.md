# Claim 5 — complete QVBS protocol

**Current status: pending remote evidence.** This page supersedes the historical random-MDP proxy once the complete run answers.

The exact Section 5.1 claim is that, across nine named QVBS benchmarks with ten trials each, policy reachability converges at median stage `k=2` and average stage `2.3`; Dining Philosophers value bounds begin converging only around `k=16`. Appendix H Table 1 reports benchmark stages `2,2,2,1,2,7,2,2,1`.

The fixed command is `uv run --frozen python -m repro.run`. The committed verifier downloads hash-pinned author source and nine official JANI payloads, applies the exact dispatcher settings, and runs 90 deterministic single-threaded learners on HF `cpu-upgrade`. It records all seeds, curves, state/action dimensions, sample counts, CPU allocation, and runtimes.

The paper's “policy accuracy” is a Monte Carlo reachability fraction, not an exact identity check. Alongside that metric, the independent checker constructs the Markov chain induced by every learned policy at every stage and returns a monotone lower/upper reachability interval. A deleted-trial mutation must be rejected. No result will be labeled VERIFIED merely because all jobs completed.

After the remote run, this page will contain the observed per-benchmark table, raw links, checker/control outputs, limitations, and the exact verdict.
