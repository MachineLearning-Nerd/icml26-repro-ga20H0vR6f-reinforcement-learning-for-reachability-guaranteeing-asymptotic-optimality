# Claim 2 — exact optimality below the finite-policy gap

Exact contract: there exists a stage `K_opt` after which the PAC event from Theorem 3.1 implies an exactly optimal memoryless deterministic policy with probability at least `1-delta_k`.

The source defines epsilon-optimality with `>=`. Therefore `epsilon = epsilon_diff` still includes the runner-up; the paper proof's non-strict boundary is insufficient. The verifier uses the valid existential witness `epsilon_k < epsilon_diff`, proves the resulting event inclusion symbolically, and audits the equality boundary as a negative control.

Run `uv run --frozen python -m repro.run`. Executable sources: `repro/claim2.py` and independent checker `repro/check_claim2.py`.

Verdict: **VERIFIED** for the strict later-stage witness. The equality boundary remains a documented proof defect and rejected negative control; this claim is conditional on the PAC premise from Claim 1.
