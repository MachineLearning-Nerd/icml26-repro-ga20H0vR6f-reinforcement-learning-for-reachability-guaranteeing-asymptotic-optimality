# Claim 4 method

The verifier uses exact `fractions.Fraction` arithmetic. It exhausts the complete domain of four-state MDPs with two decision states, one absorbing goal, one absorbing sink, two actions, and transition probabilities on the denominator-2 grid. There are 10 possible transition rows and 10,000 MDPs before enforcing the paper's halting assumption. All four deterministic memoryless policies and all six policy pairs are checked for every halting MDP.

The primary solver uses exact Gaussian elimination specialized to the two transient states. The independent checker re-enumerates the domain and uses a separately written two-by-two Cramer solver. Each MDP uses its actual row-LCM transition complexity, not the grid denominator. A negative control injects the forbidden positive gap `bound/2`; the same predicate must reject it.

Command: `uv run --frozen python -m repro.run`

Core estimate before launch: one core; selected flavor: Hugging Face `cpu-upgrade`. The run records the actual visible CPU allocation and wall time.
