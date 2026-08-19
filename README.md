# RL for Reachability — claim-by-claim reproduction

> Independent reproduction and theorem audit for *Reinforcement Learning for Reachability: Guaranteeing Asymptotic Optimality*.

## Current status

The canonical main branch contains the complete verifier lineage through the nine-benchmark QVBS node. The repository's cumulative evidence record reports Claims 1–4 as verified under their stated contracts. Claim 5 is intentionally still PENDING/BLOCKED: the source and verifier for the complete 9 × 10 benchmark protocol are present, but no committed 90-trial result is being represented as completed evidence.

| Claim | Paper location | Status | What the repository establishes |
| --- | --- | --- | --- |
| 1 | Theorem 3.1 | VERIFIED | Reconstructed the existential PAC witness proof, calibrated finite sample counts, and checked adaptive-process tails. |
| 2 | Theorem 3.2 | VERIFIED | Proved the strict-gap event inclusion and audited the equality boundary where the paper's displayed non-strict inequality is insufficient. |
| 3 | Theorem 3.3 | VERIFIED | Machine-checked geometric summability, the union-bound tail, and first Borel–Cantelli inference without independence. |
| 4 | Theorem 4.1 | VERIFIED within the stated rational/halting contract | Proved the denominator lower bound and exhaustively calibrated the complete four-state denominator-2 subdomain. |
| 5 | Section 5.1 and Appendix H | PENDING | The exact author implementation, nine QVBS inputs, 90 trials, aggregation, and independent fixed-policy audit are prepared; the complete run remains required. |

No judge score change is claimed by this repository.

Publication boundary: `publication_allowed=true` applies only to this scoped
audit dossier. `score_claim=false` and `official_author_endorsement=false`.
Claim 5 remains pending until the complete 9 × 10 QVBS protocol produces
committed raw evidence.

## Audit dossier

The standardized audit record is split into small, reviewable files:

- [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) maps each paper claim to its producer, checks, controls, and evidence boundary.
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the pinned paper source, theorem anchors, author implementation, and QVBS inputs.
- [BRANCH_AUDIT.md](BRANCH_AUDIT.md) records the published branch names, former workspace labels, tips, and attribution policy.
- [ENVIRONMENT.md](ENVIRONMENT.md) records the fixed command, lockfile, targeted verification checkpoint, and Claim 5 run boundary.
- [REPORT.md](REPORT.md) states the scoped scientific decision and limitations.
- [CITATION.cff](CITATION.cff) and [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) provide citation and author acknowledgement.
- [reproduction_verdicts.json](reproduction_verdicts.json) records the machine-readable claim verdicts and publication boundary.
- [AUTONOMOUS_STATE.json](AUTONOMOUS_STATE.json) records the resumable repository state, branch topology, and attribution checkpoint.
- [verify_final.py](verify_final.py) performs fail-closed structural checks on a local or fresh clone.

The dossier is deliberately more conservative than a benchmark-only README: a passing theorem certificate does not imply that the complete QVBS experiment was reproduced.

## Paper and provenance

| Field | Record |
| --- | --- |
| Full title | Reinforcement Learning for Reachability: Guaranteeing Asymptotic Optimality |
| Authors | Amogh Palasamudram, Jakub Svoboda, Suguman Bansal, Krishnendu Chatterjee |
| Primary source | [arXiv:2605.24740](https://arxiv.org/abs/2605.24740) |
| Venue | ICML 2026; the current arXiv record says the main text and appendix were accepted |
| OpenReview identifier | ga20H0vR6f, as carried by the original reproduction workspace |
| Pinned HTML source | https://ar5iv.labs.arxiv.org/html/2605.24740 |
| HTML SHA-256 | 59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2 |
| Source record | [audits/paper_source.md](audits/paper_source.md) |
| Author implementation | [amoghp214/asymptotic-ltl-reachability](https://github.com/amoghp214/asymptotic-ltl-reachability), pinned in the Claim 5 audit at commit 6ffec1273326aede50c8b6516cea1ceb8d920faa |
| Official QVBS source | [ahartmanns/qcomp](https://github.com/ahartmanns/qcomp), pinned in the Claim 5 audit at commit c7324a311475ba1a3f40e36a324e32f91e766540 |
| Former repository | icml26-repro-ga20H0vR6f-reinforcement-learning-for-reachability-guaranteeing-asymptotic-optimality |
| Canonical repository | [MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality](https://github.com/MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality) |
| Canonical branch | main |

The paper-source hash, retrieval date, theorem anchors, and supporting PAC source are recorded in audits/paper_source.md and the per-claim source audits.

## What the paper is doing

The paper studies reinforcement learning for reachability specifications in unknown finite Markov decision processes. Its algorithm works directly with the MDP rather than converting the specification into a reward objective:

1. Run the learner in stages.
2. At stage k, refine guesses for the minimum transition probability, confidence error, and approximation tolerance using geometric schedules.
3. Build a partial model from simulations, collapse end components, apply bounded value iteration, and extract a memoryless deterministic policy.
4. Use PAC-style finite-stage guarantees and a summable failure schedule to show that optimal policies eventually appear almost surely.
5. Bound the separation between distinct rational policy-value vectors and test the convergence dynamics on nine Quantitative Verification Benchmark Set (QVBS) models.

The reproduction therefore has two different evidence types: proof-level certificates for the universal statements and protocol-level benchmark evidence for the empirical claim. A finite benchmark result is not promoted to a universal theorem.

## Claim-to-evidence ledger

The exact contracts are under [.openresearch/artifacts](.openresearch/artifacts). Each contract states the quantifiers, assumptions, pass condition, failure condition, and intended verdict vocabulary.

### Claim 1 — Theorem 3.1: PAC witness existence

Exact statement: there is a finite K_PAC such that, for every later stage, some finite N_k makes Algorithm 1 return an epsilon_k-optimal policy with probability at least 1 - delta_k.

How the claim is produced:

1. [repro/claim1.py](repro/claim1.py) reconstructs the existential proof: geometric decay reaches p_k <= p_min; conservative PAC-BVI supplies finite transition-hit requirements; positive exploration gives a uniform conditional lower bound; and a union bound closes the error split.
2. The verifier replaces an unjustified iid-binomial reading of adaptive episodes with a shared-uniform coupling/stochastic-domination argument.
3. Exact binary search calibrates the smallest adequate N across six (s, q, eta) regimes without using a theorem-provided sample formula.
4. [repro/check_claim1.py](repro/check_claim1.py) independently checks the tail using a separately written convolution and an adversarial dynamic program.
5. N - 1 and zero-exploration controls must fail.

Verdict: VERIFIED for the stated finite-MDP, positive-exploration, conservative PAC-BVI contract. The potentially enormous existential witness is not presented as a practical sample-complexity recommendation. The author's practical N_k heuristic is kept separate from theorem evidence.

Evidence files: [.openresearch/artifacts/claim1](.openresearch/artifacts/claim1), [candidate/pages/claim-1.md](candidate/pages/claim-1.md).

### Claim 2 — Theorem 3.2: exact optimality below the finite-policy gap

Exact statement: after a finite stage K_opt, Algorithm 1 returns an exactly optimal memoryless deterministic policy with probability at least 1 - delta_k.

How the claim is produced:

1. [repro/claim2.py](repro/claim2.py) proves the finite-policy order argument with exact rational arithmetic.
2. It uses a strict later-stage witness epsilon_k < epsilon_diff, so every epsilon_k-optimal policy is optimal.
3. [repro/check_claim2.py](repro/check_claim2.py) exhausts rational value spectra with two through five policies on denominator grids 2 through 12.
4. The equality boundary is a negative control: because the source defines epsilon-optimality inclusively, epsilon_k = epsilon_diff can still include the runner-up.

Verdict: VERIFIED for the existential theorem after the strict-stage repair. The displayed non-strict proof boundary is documented as a proof defect, not silently ignored. This claim depends on Claim 1 for the PAC premise.

Evidence files: [.openresearch/artifacts/claim2](.openresearch/artifacts/claim2), [candidate/pages/claim-2.md](candidate/pages/claim-2.md).

### Claim 3 — Theorem 3.3: almost-sure eventual exact optimality

Exact statement: if post-K_opt non-optimal-policy events satisfy Pr(E_k) <= 2^-k, then only finitely many such stages occur with probability one.

How the claim is produced:

1. [repro/claim3.py](repro/claim3.py) derives the exact geometric tail sum from k=n to infinity of 2^-k = 2^(1-n).
2. A union bound gives a vanishing probability for any failure after stage n.
3. Continuity from above and the first Borel–Cantelli lemma give probability zero for infinitely many failures; independence is not assumed.
4. [repro/check_claim3.py](repro/check_claim3.py) independently checks 100 recurrence values and 64 exact tail starts.
5. The harmonic 1/k schedule is a divergence control and must be rejected.

Verdict: VERIFIED conditionally on the stage-wise guarantee from Claim 2.

Evidence files: [.openresearch/artifacts/claim3](.openresearch/artifacts/claim3), [candidate/pages/claim-3.md](candidate/pages/claim-3.md).

### Claim 4 — Theorem 4.1: rational policy-value gap

Exact statement: for rational, halting finite MDPs and memoryless deterministic policies, the L1 value-vector gap is either zero or at least the paper's denominator-dependent positive bound.

How the claim is produced:

1. [repro/claim4.py](repro/claim4.py) reconstructs the rational denominator argument using the row-wise transition denominator LCM D.
2. Equal value vectors take the theorem's zero branch; unequal rational components have a nonzero integer cross-product and therefore a positive minimum separation.
3. The complete four-state, two-transient-state, denominator-2 subdomain contains 10,000 transition tables; 5,537 are halting and all four deterministic policies and six policy pairs are checked for each.
4. [repro/check_claim4.py](repro/check_claim4.py) independently re-enumerates the domain with a separate two-by-two Cramer solver.
5. The negative control injects a forbidden positive gap below the bound and must be rejected.

The recorded calibration found 9,918 zero-value pairs, 23,304 positive-gap pairs, minimum positive gap 1/4, and minimum gap/bound ratio 16,777,216.

Verdict: VERIFIED under the stated rational, halting, memoryless-deterministic contract. The finite enumeration is implementation calibration, not a substitute for the universal denominator proof. The judged baseline's omission of the zero branch is explicitly repaired.

Evidence files: [.openresearch/artifacts/claim4](.openresearch/artifacts/claim4), [candidate/pages/claim-4.md](candidate/pages/claim-4.md).

### Claim 5 — Section 5.1 and Appendix H: nine QVBS benchmarks

Exact protocol claim: nine named QVBS benchmarks, ten trials each, should produce the paper's reported convergence stages [2, 2, 2, 1, 2, 7, 2, 2, 1], with median stage 2 and mean stage 2.3; Dining Philosophers value bounds begin converging near stage 16.

How the prepared reproduction will produce the claim:

1. [repro/qvbs.py](repro/qvbs.py) acquires the author implementation and official JANI payloads at pinned commits and verifies their hashes.
2. A standard-library compatibility layer changes only the small dependency surface needed for the frozen environment; the author's conversion, learner, bounded value iteration, MEC handling, simulation, and stopping logic remain intact.
3. [repro/qvbs_full.py](repro/qvbs_full.py) runs the exact nine benchmark configurations with ten fixed-seed trials each.
4. The paper's Monte Carlo policy accuracy is reported as-is, while an independent fixed-policy evaluator also computes monotone lower/upper reachability intervals.
5. The independent checker requires all 90 trials, and the deleted-trial control must be rejected.

Verdict: PENDING. The source, configuration, checker, and limitations are prepared, but this repository does not claim a completed 90-trial result until the run is actually executed and its raw evidence is committed.

Evidence files: [.openresearch/artifacts/claim5](.openresearch/artifacts/claim5), [candidate/pages/claim-5.md](candidate/pages/claim-5.md), [audits/logbook_gap_analysis.md](audits/logbook_gap_analysis.md).

The current numerical checkpoint for Claims 1–4 came from a targeted, no-bytecode exact check of the four proof producers and independent checkers. It did not invoke the full QVBS runner, and generated raw JSON from the fixed cumulative command is not represented as committed evidence in this dossier.

## Branch map

The original orx/ prefixes were workspace execution labels. They are retained below only for provenance; the published names describe each branch's role.

| Published branch | Former branch | Purpose | State |
| --- | --- | --- | --- |
| main | main plus merged final lineage | Canonical README, contracts, verifiers, candidate pages, and source audits. | Current |
| audit/theorem-4-1-value-gap | orx/baseline-exact-theorem-4-1-contract | Establishes the exact Theorem 4.1 contract and baseline verifier. | Verified evidence |
| audit/theorems-3-2-3-3-exact-certificates | orx/exact-certificates-for-theorems-3-2-and-3-3 | Adds exact Theorem 3.2 and 3.3 certificates and independent checks. | Verified evidence |
| audit/theorem-3-1-pac-existence | orx/pac-existence-certificate-and-calibrated-n-searc | Adds the PAC-existence proof, calibrated sample counts, and adaptive checker. | Verified evidence |
| audit/qvbs-ingestion-calibration | orx/qvbs-ingestion-and-ij-3-calibration | Pins author/QVBS inputs and calibrates end-to-end ingestion on ij.3. | Setup evidence |
| release/qvbs-nine-benchmark | orx/full-nine-benchmark-ten-trial-qvbs-reproduction | Adds the complete nine-benchmark, ten-trial runner and Claim 5 checker. | Pending run |

All renamed branches point to the same historical work after identity normalization. Branch naming does not alter scientific verdicts.

## Reproduce and inspect

The environment is dependency-free Python 3.10–3.13 with a committed uv.lock:

    uv sync --frozen
    uv run --frozen python -m repro.run

The command runs Claims 1–4 and then the complete Claim 5 benchmark protocol. It writes generated raw results under .openresearch/artifacts/ and exits nonzero if any claim checker or control fails. The full QVBS node is intentionally compute-heavy; do not interpret an unrun or interrupted command as a scientific verdict.

Useful entry points:

- [Claim contracts and source anchors](.openresearch/artifacts)
- [Paper source record](audits/paper_source.md)
- [Historical judged-work gap analysis](audits/logbook_gap_analysis.md)
- [Cumulative candidate index](candidate/pages/index.md)
- [Theorem 3.1 verifier](repro/claim1.py), [Theorem 3.2 verifier](repro/claim2.py), [Theorem 3.3 verifier](repro/claim3.py), [Theorem 4.1 verifier](repro/claim4.py)
- [QVBS source ingestion](repro/qvbs.py) and [full benchmark runner](repro/qvbs_full.py)

Historical research runs used Hugging Face cpu-upgrade compute. Claims 1–4 are exact-algebra/proof and finite-enumeration checks; Claim 5 uses the authors' learner and nine benchmark models.

## Reproduction policy

- Keep the arXiv paper version, source hash, theorem anchors, and claim quantifiers pinned.
- Separate universal proof certificates from finite-domain calibration and empirical benchmark outcomes.
- Keep independent checkers and negative controls beside every verdict.
- Record strict-boundary repairs explicitly rather than silently changing a paper statement.
- Treat the author's heuristic sample count and finite simulation fractions as different from theorem evidence.
- Do not mark Claim 5 verified until all 90 trials, aggregation, independent value audit, and missing-trial control are present.

## Citation

Please cite the paper as:

    @article{palasamudram2026reachability,
      title = {Reinforcement Learning for Reachability: Guaranteeing Asymptotic Optimality},
      author = {Palasamudram, Amogh and Svoboda, Jakub and Bansal, Suguman and Chatterjee, Krishnendu},
      journal = {arXiv preprint arXiv:2605.24740},
      year = {2026},
      doi = {10.48550/arXiv.2605.24740}
    }

The current arXiv record identifies the work as accepted to ICML 2026; use the final proceedings citation if one is required.

## Thank you

Thank you to Amogh Palasamudram, Jakub Svoboda, Suguman Bansal, and Krishnendu Chatterjee for developing a thoughtful direct-learning framework for reachability specifications. The separation between PAC existence, exact policy optimality, almost-sure convergence, rational value separation, and benchmark behavior makes the work especially suitable for careful claim-by-claim reproduction. This repository is intended as a respectful, transparent companion to the paper, with its proof boundaries and remaining empirical work clearly labeled.

## Limitations

- Claim 1 verifies existence, not the practical size or usefulness of its witness.
- Claim 2 uses the strict later-stage witness required by the inclusive epsilon-optimal definition; the source's displayed equality boundary is not silently treated as sufficient.
- Claim 3 is a conditional probabilistic inference from the previous theorem, not a finite simulation of a probability-one event.
- Claim 4's finite enumeration is complete only for its explicit four-state denominator-2 subdomain.
- Claim 5 remains pending until the full 9 × 10 protocol produces committed raw evidence; author seeds were not published, so this reproduction fixes and reports its own seeds.
- The frozen environment uses a standard-library compatibility layer and concurrent single-threaded trials, so wall-clock timing is not a direct reproduction of the paper's hardware.
