# Branch audit

Published branch names describe their mathematical or release role. Former
orx/ names are retained only as migration provenance; no final remote branch
uses that prefix.

## Pre-dossier snapshot

- Repository: MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality
- Former repository:
  MachineLearning-Nerd/icml26-repro-ga20H0vR6f-reinforcement-learning-for-reachability-guaranteeing-asymptotic-optimality
- Default branch: main
- Main tip before this dossier: a94954c4e14bf922e429498583f37cbad214154e
- Reachable commits before this dossier: 9 unique commits
- Remote branches before this dossier: 6
- Recovery bundle: created and verified locally before dossier edits; it is not
  part of the public repository.

## Final branch map

| Final branch | Former branch | Evidence role | Pre-dossier tip |
| --- | --- | --- | --- |
| main | main plus merged final lineage | Canonical README, claim contracts, source audits, and dossier | a94954c4e14bf922e429498583f37cbad214154e |
| audit/theorem-4-1-value-gap | orx/baseline-exact-theorem-4-1-contract | Theorem 4.1 contract and exact baseline verifier | 09f5b50bfead103f19674f2836788b8680c17ade |
| audit/theorems-3-2-3-3-exact-certificates | orx/exact-certificates-for-theorems-3-2-and-3-3 | Exact Theorems 3.2 and 3.3 certificates | ae8021805d7392fd017b45d48374ea9ffd2b4e0a |
| audit/theorem-3-1-pac-existence | orx/pac-existence-certificate-and-calibrated-n-searc | Theorem 3.1 PAC proof and calibration | b45fdb03ffc9028cd1166851f569905ab5c8fa4a |
| audit/qvbs-ingestion-calibration | orx/qvbs-ingestion-and-ij-3-calibration | Author/QVBS source pinning and ij.3 setup | e97ee3c33543548e792c367d2845b7bae4df8227 |
| release/qvbs-nine-benchmark | orx/full-nine-benchmark-ten-trial-qvbs-reproduction | Complete nine-benchmark, ten-trial Claim 5 runner | 6c33ff628c4189fb2960d43bcfac5b85cd34ab02 |

## Attribution and safety record

Every reachable pre-dossier commit has both author and committer set to:

    MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>

The dossier and checkpoint commits use the same identity. Co-author trailers
are not used. The final verifier checks that no refs/original, legacy orx
reference, or unexpected branch remains after a fresh clone.

The six-branch inventory is structural provenance. It does not imply that the
Claim 5 release branch has completed its benchmark run.
