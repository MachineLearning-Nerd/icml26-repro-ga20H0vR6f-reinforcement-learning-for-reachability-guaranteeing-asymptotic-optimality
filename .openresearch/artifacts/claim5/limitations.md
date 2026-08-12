# Claim 5 limitations and deviations

- The authors did not publish their trial seeds. This reproduction fixes and reports 90 seeds.
- The frozen baseline environment has no third-party packages. A stdlib compatibility layer replaces NumPy random choice and disables only progress/plot rendering; author learning, conversion, BVI, MEC, simulation, and stopping logic are unchanged. Unweighted candidates are sorted before seeded choice.
- Trials run concurrently on HF `cpu-upgrade`; each individual learner is single-threaded. This changes wall-clock scheduling, not a trial's algorithm.
- The paper does not define an algorithm for converting noisy median accuracy curves into “Stages Conv.” We therefore report a predeclared 95% sampling criterion and the independent fixed-policy value interval rather than reverse-engineering a threshold to match Table 1.
