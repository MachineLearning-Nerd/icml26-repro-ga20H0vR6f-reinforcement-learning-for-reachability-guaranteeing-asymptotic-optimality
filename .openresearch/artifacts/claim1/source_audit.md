# Claim 1 source audit

- Paper source: https://ar5iv.labs.arxiv.org/html/2605.24740
- Retrieved: 2026-08-02 (Asia/Kolkata), explicit User-Agent `OpenResearch-Reproduction/1.0 (paper audit; contact via project repository)`
- SHA-256: `59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2`
- Theorem anchor: `#S3.Thmtheorem1`; full proof: Appendix E `#A5`, especially E.3-E.6
- Supporting primary source: Ashok, Křetínský, and Weininger, *PAC Statistical Model Checking for Markov Decision Processes and Stochastic Games*, arXiv:1905.04403 / CAV 2019
- Supporting PDF retrieved 2026-08-02 from https://arxiv.org/pdf/1905.04403 with an explicit User-Agent; SHA-256 `ad45e27478d00d58b531c984a38f4fc5a444c510aaa6d0a95f40717423b3566f`

The exact theorem is existential in both `K_PAC` and every subsequent `N_k`; it does not prescribe a practical sample count. Appendix E splits `delta_k` across transition estimation, EC detection, and insufficient transition hits. Its Binomial wording assumes identical independent episode hits even though the guiding policy adapts. The current proof repairs that step with stochastic domination: a uniform conditional lower bound on every episode is enough, and no iid claim about actual hits is needed.

The authors' repository at commit `6ffec1273326aede50c8b6516cea1ceb8d920faa` explicitly labels its implemented `N_k` as a heuristic that lacks the paper guarantee. That heuristic is excluded from Claim 1 verification.
