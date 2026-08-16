# Environment and artifact record

## Fixed reproduction command

From a clean checkout:

    uv sync --frozen && uv run --frozen python -m repro.run

The project requires Python 3.10 through 3.13 and has no declared third-party
dependencies. The committed uv.lock SHA-256 is
5f9027d68db7ed4db07a1226b953f6eeb82fe11b204277e2359a9ea89c04aee6.

The command writes generated JSON below .openresearch/artifacts and runs the
compute-heavy nine-benchmark node after Claims 1–4. Generated output is not
automatically a published verdict: it must pass the independent checkers and
negative controls.

## Dossier checkpoint

The documentation checkpoint directly invoked the four exact proof producers
and independent checkers with Python bytecode disabled. It did not run
repro.run.py, acquire external QVBS sources, or claim a completed benchmark.
No run ID, wall-clock time, CPU allocation, or judge score is invented.

| Claim | Checkpoint scope |
| --- | --- |
| C1 | Exact minimum-N calibration, adaptive-process checker, N-minus-one control, and zero-exploration control. |
| C2 | Exact strict-stage witnesses, rational-spectrum checker, and inclusive-equality control. |
| C3 | Exact geometric tails, independent recurrence, and harmonic divergence control. |
| C4 | Complete four-state denominator-2 calibration, independent Cramer checker, and below-bound control. |
| C5 | Not run; source pins and the 9 x 10 runner are prepared. |

The observed values and their production paths are recorded in
CLAIM_EVIDENCE.md. The absence of committed raw JSON is an evidence boundary,
not a claim that the producers cannot generate it.

## Claim 5 protocol

The prepared protocol has nine named QVBS benchmarks, ten deterministic
trials per benchmark, 32 concurrent trial workers, and base seed 2026080200.
The author learner remains single-threaded inside each trial. The intended
external inputs are the author implementation at
6ffec1273326aede50c8b6516cea1ceb8d920faa and qcomp at
c7324a311475ba1a3f40e36a324e32f91e766540.

The paper's reported stages are [2, 2, 2, 1, 2, 7, 2, 2, 1], with median 2
and mean 2.3. Dining Philosophers value bounds are reported as beginning to
converge near stage 16. A complete publication must record all 90 trials,
seeds, dimensions, curves, independent fixed-policy intervals, aggregation,
and the missing-trial rejection.

## Reproduction policy

- Keep universal proof certificates separate from finite calibration.
- Keep paper source, code pins, and lockfile hashes stable.
- Report proof-boundary repairs, especially the strict C2 witness.
- Do not promote C5 from PENDING without complete raw and independently
  checked evidence.
