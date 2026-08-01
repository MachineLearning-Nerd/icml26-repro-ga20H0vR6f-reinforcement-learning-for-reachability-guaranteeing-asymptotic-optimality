# Claim 5 method

Run the authors' converter and learner on the exact nine QVBS JANI payloads and exact dispatcher configurations, with ten deterministic trials each. The author learner remains single-threaded; 32 independent trials run concurrently on HF `cpu-upgrade`.

The paper calls Monte Carlo reachability “policy accuracy.” We reproduce that metric, but do not equate a finite simulation fraction with exact policy identity. At every stage an independent stdlib evaluator constructs the Markov chain induced by the learned (including collapsed-MEC) policy, removes states that cannot graph-reach a goal, and performs monotone lower/upper iteration until the initial-state interval is at most `1e-9` wide. Both empirical and certified-value convergence stages are reported.

The independent checker rejects an incomplete 9x10 design. The negative control deletes one trial and must exit through the rejection path.
