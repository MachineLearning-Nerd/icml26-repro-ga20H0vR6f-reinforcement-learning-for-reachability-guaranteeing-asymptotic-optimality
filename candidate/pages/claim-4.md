# Claim 4 — Theorem 4.1 value-gap disjunction

Current contract: for a finite rational halting MDP, any pair of memoryless deterministic policies has either equal value vectors or L1 gap at least `(2D)^(-2|A||S|) 2^(-2|S|)`. The zero branch, rationality, and halting assumption were missing from the judged presentation.

Run `uv run --frozen python -m repro.run`. The executable source is in `repro/claim4.py`; an independent Cramer-rule checker is in `repro/check_claim4.py`. Raw results, checker output, and the negative-control output are generated under `.openresearch/artifacts/claim4/` and printed inline in the run log.

Verdict: **Pending baseline run**. No forecast credit is claimed until Hugging Face `cpu-upgrade` produces the evidence.
