# Claim 3 — almost-sure eventual exact optimality

Exact contract: if the non-optimal-policy events satisfy `Pr(E_k) <= 2^-k` after `K_opt`, only finitely many occur almost surely.

The proof certificate reconstructs the first Borel-Cantelli argument from the exact tail `2^(1-n)`, a union bound, and continuity from above. No independence assumption is used. The harmonic schedule `1/k` is the negative control and is rejected with a dyadic-block divergence certificate.

Run `uv run --frozen python -m repro.run`. Executable sources: `repro/claim3.py` and independent checker `repro/check_claim3.py`.

Verdict: **Pending HF cpu-upgrade run**.
