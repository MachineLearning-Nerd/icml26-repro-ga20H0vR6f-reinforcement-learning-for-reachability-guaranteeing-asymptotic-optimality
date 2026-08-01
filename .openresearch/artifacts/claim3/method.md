# Claim 3 method

The verifier reconstructs the proof directly: the exact tail is `sum_{k=n}^infinity 2^-k = 2^(1-n)`; a union bound caps the probability of any failure after `n`; continuity from above sends the limsup probability to zero. Exact `Fraction` checks cover 64 tail starts, and an independently written recurrence covers 100. The negative control substitutes `1/k` and certifies divergence because every dyadic block contributes at least one half.
