# Claim 1 — PAC witness existence

Exact contract: there is a finite `K_PAC` such that every later stage has some finite `N_k` making the returned policy `epsilon_k`-optimal with probability at least `1-delta_k`.

The current verifier reconstructs the existential proof, replaces an unjustified iid Binomial statement with a coupling valid for adaptive episode probabilities, and independently binary-searches exact minimum `N` values across six regimes. A separately written convolution and adversarial dynamic program checks the tail calculation. `N-1` and zero exploration are failing controls.

The author implementation's own comment says its practical `N_k` is heuristic and lacks the paper guarantee; it is not used as PAC evidence.

Run `uv run --frozen python -m repro.run`. Executable sources: `repro/claim1.py` and `repro/check_claim1.py`.

Verdict: **Pending HF cpu-upgrade run**.
