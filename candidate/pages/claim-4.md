# Claim 4 — Theorem 4.1 value-gap disjunction

Current contract: for a finite rational halting MDP, any pair of memoryless deterministic policies has either equal value vectors or L1 gap at least `(2D)^(-2|A||S|) 2^(-2|S|)`. The zero branch, rationality, and halting assumption were missing from the judged presentation.

Run `uv run --frozen python -m repro.run`. The executable source is in `repro/claim4.py`; an independent Cramer-rule checker is in `repro/check_claim4.py`. Raw results, checker output, and the negative-control output are generated under `.openresearch/artifacts/claim4/` and printed inline in the run log.

Baseline result on Hugging Face `cpu-upgrade`: **VERIFIED on the complete stated finite subdomain**. The run enumerated 10,000 transition tables, of which 5,537 were halting, and checked all 33,222 policy pairs. It found 9,918 zero-value pairs and 23,304 positive-gap pairs. The minimum positive L1 gap was `1/4`; the smallest gap/bound ratio was `16,777,216`. The independent checker reproduced the counts and minimum, and the below-bound injection was rejected. This is exhaustive finite-domain corroboration of the exact disjunction, not a universal proof of Theorem 4.1.
