# Claim-to-evidence map

This dossier records how each paper claim is produced. The common production
graph is:

    paper anchor -> explicit contract -> executable producer
                 -> independent checker -> negative control -> verdict

The fixed cumulative entrypoint is repro/run.py. It runs Claims 1–4 and then
the complete Claim 5 protocol. The dossier checkpoint below is narrower: it
ran the four exact proof producers and their independent checkers directly,
without launching the compute-heavy QVBS node.

## Evidence boundary

- The paper contracts, methods, limitations, and source anchors are committed
  under .openresearch/artifacts/claim1 through claim5.
- The executable producers are repro/claim1.py through repro/claim4.py and
  repro/qvbs_full.py; independent checkers are the corresponding check_claim
  files and the QVBS checker.
- The numerical checkpoint below is a targeted no-bytecode local check of
  Claims 1–4. It is not a full repro/run.py campaign and has no fabricated run
  identifier or runtime.
- No generated raw_results.json, verifier_output.json, or cumulative result
  is being claimed as committed evidence for this checkpoint. Claim 5 has no
  completed 90-trial result and remains PENDING.
- A future Claim 5 publication must include all 90 raw trials, independently
  reconstructed aggregation, fixed-policy intervals, and the deleted-trial
  control before changing its status.

## C1 — Theorem 3.1: PAC witness existence

Paper anchor: ar5iv HTML #S3.Thmtheorem1 and Appendix E #A5.

Producer path:

1. repro/claim1.py reconstructs the existential quantifiers: geometric
   schedules reach the minimum transition probability, conservative PAC-BVI
   supplies finite transition-hit requirements, positive exploration supplies
   a uniform conditional lower bound, and a union bound closes the error split.
2. Exact binary search calibrates the smallest adequate N in six regimes; no
   theorem-provided sample formula selects those values.
3. repro/check_claim1.py independently checks the binomial tail with a fresh
   convolution and an adversarial dynamic program over history-dependent hit
   probabilities.
4. N minus one and zero-exploration controls must be rejected.

Observed checkpoint:

- The stage witnesses were p_min = 1/2 -> K = 1, p_K = 1/2; 1/3 -> K = 2,
  p_K = 1/4; 1/10 -> K = 4, p_K = 1/16; and 1/1024 -> K = 10,
  p_K = 1/1024.
- The exact minimum N values for the six calibrations were
  [11, 31, 77, 232, 521, 1250].
- The independent checker passed 6 minimum-N calibrations and 84 adaptive
  probability processes.
- The N-minus-one and zero-exploration controls were rejected as intended.

Verdict: VERIFIED for the finite-MDP, positive-exploration, conservative
PAC-BVI contract. This verifies existence, not a practical sample-complexity
recommendation. The authors' heuristic N_k is kept separate from theorem
evidence.

Primary files: repro/claim1.py, repro/check_claim1.py, and
.openresearch/artifacts/claim1/.

## C2 — Theorem 3.2: exact optimality below the finite-policy gap

Paper anchors: ar5iv HTML #S3.Thmtheorem2 and the epsilon-optimal definition
at #S2.SS0.SSS0.Px2.p3.

Producer path:

1. repro/claim2.py proves the finite policy-order argument with exact rational
   arithmetic and constructs a strict later stage epsilon_k < epsilon_diff.
2. repro/check_claim2.py exhausts value spectra with two through five policies
   on denominator grids 2 through 12.
3. The equality boundary is an explicit negative control: inclusive
   epsilon-optimality allows the first runner-up when epsilon equals the gap.

Observed checkpoint:

- Strict witnesses were gap 1/2 -> stage 2, epsilon 1/4; gap 1/3 -> stage 2,
  epsilon 1/4; gap 1/17 -> stage 5, epsilon 1/32; and gap 7/64 -> stage 4,
  epsilon 1/16.
- The symbolic positive margin was 2/13.
- The independent value-spectrum, strict-implication, and equality-boundary
  checks each covered 26,653 cases.
- The equality control exposed the runner-up and was rejected as intended.

Verdict: VERIFIED for the existential strict-stage theorem, conditional on
the PAC premise from C1. The paper's displayed non-strict boundary is
reported as a proof defect rather than silently treated as sufficient.

Primary files: repro/claim2.py, repro/check_claim2.py, and
.openresearch/artifacts/claim2/.

## C3 — Theorem 3.3: almost-sure eventual exact optimality

Paper anchor: ar5iv HTML #S3.Thmtheorem3.

Producer path:

1. repro/claim3.py derives the exact tail sum from k = n to infinity of
   2^-k = 2^(1-n), then applies a union bound and continuity from above.
2. The first Borel–Cantelli lemma converts summability into an almost-sure
   finite number of failures; no independence assumption is used.
3. repro/check_claim3.py independently checks recurrence values and exact tail
   starts.
4. Replacing 2^-k with the divergent harmonic schedule 1/k is the negative
   control.

Observed checkpoint:

- 64 exact tail checks and 100 independent tail-start recurrence checks passed.
- The harmonic 1/k control was rejected because the required series diverges.

Verdict: VERIFIED conditionally on C2 and its stage-wise probability bound.
This is a proof certificate, not a finite simulation of a probability-one
event.

Primary files: repro/claim3.py, repro/check_claim3.py, and
.openresearch/artifacts/claim3/.

## C4 — Theorem 4.1: rational policy-value gap

Paper anchor: ar5iv HTML #S4.Thmtheorem1 and Appendix F #A6.

Producer path:

1. repro/claim4.py reconstructs the rational denominator argument and retains
   the theorem's disjunction: equal value vectors or a positive lower bound.
2. The complete four-state, denominator-2 subdomain is enumerated with exact
   Fraction arithmetic.
3. repro/check_claim4.py independently re-enumerates it with a separate
   two-by-two Cramer solver.
4. A positive gap below the bound is injected as a negative control.

Observed checkpoint:

- 10,000 MDPs were enumerated; 5,537 satisfied the halting condition.
- 33,222 policy pairs were checked: 9,918 zero-value-vector pairs and 23,304
  positive-gap pairs.
- The minimum positive L1 gap was 1/4.
- The minimum gap-to-bound ratio was 16,777,216/1.
- The case digest was
  fbad961b469e1af018ec13408048867b45ea309659b5d34abcb8335010370708.
- The independent checker reproduced the halting-MDP count, policy-pair
  count, and minimum gap; the below-bound injection was rejected.

Verdict: VERIFIED under the rational, halting, memoryless-deterministic
contract. The finite enumeration is calibration, not a replacement for the
universal denominator proof.

Primary files: repro/claim4.py, repro/check_claim4.py, and
.openresearch/artifacts/claim4/.

## C5 — Section 5.1 and Appendix H: nine QVBS benchmarks

Paper anchors: Section 5.1 and Appendix H Table 1.

Prepared producer path:

1. repro/qvbs.py acquires hash-pinned author code and official JANI inputs.
2. repro/qvbs_full.py runs nine named benchmarks, ten fixed-seed trials each,
   and records the paper's Monte Carlo policy metric.
3. The independent fixed-policy evaluator computes monotone lower and upper
   reachability intervals at every learned stage.
4. The checker requires exactly 90 trials and rejects the deleted-trial
   mutation.

Required comparison: paper stages [2, 2, 2, 1, 2, 7, 2, 2, 1], median 2,
mean 2.3, and Dining Philosophers value-bound convergence near stage 16.

Verdict: PENDING. The source pins, runner, checker, and controls are present,
but no complete 90-trial result is represented as evidence.

Primary files: repro/qvbs.py, repro/qvbs_full.py,
.openresearch/artifacts/claim5/, candidate/pages/claim-5.md, and
audits/logbook_gap_analysis.md.

## Overall decision

Claims 1–4 are verified only within the contracts written above. Claim 5 is
pending. No judge score increase, author endorsement, or universal claim from
the finite C4 calibration is asserted.
