# Claim 1 method

Route 1 reconstructs the exact quantifier proof: geometric decay reaches `p_k <= p_min`; conservative PAC-BVI supplies finite transition-hit requirements; positive exploration gives a positive per-episode lower bound; shared-uniform coupling reduces the adaptive process to a Binomial lower-tail bound; finiteness plus a union bound closes the error split.

Route 2 independently calibrates the smallest adequate `N` by exact binary search over the Binomial tail for six `(s,q,eta)` regimes. No paper formula selects the search points or result. Every `N-1` must fail.

Route 3 uses a separately written Bernoulli convolution and an adversarial dynamic program over history-dependent probabilities. It verifies that the worst allowed adaptive process chooses the lower probability at every history.
