# Branch audit — RL for Reachability

This ledger records the merge, identity cleanup, repository rename, and branch-name cleanup for the reachability reproduction.

## Initial remote snapshot

- Repository: MachineLearning-Nerd/icml26-repro-ga20H0vR6f-reinforcement-learning-for-reachability-guaranteeing-asymptotic-optimality
- Default branch: main
- Main before lineage merge: e327da0a971b273266569937dab65ca0239847a2
- Full reproduction lineage tip: e44350374a22508592a4931cafaa0d7d89a541a0
- Reachable commits before cleanup: 6
- Remote branches before cleanup: main plus 5 ORX branches
- Author implementation and QVBS pins are recorded in audits/paper_source.md and Claim 5 source_audit.md

## Main-lineage merge

The former main branch was only a placeholder README. The final ORX lineage contained the actual theorem contracts, verifiers, source audits, candidate pages, and the Claim 5 runner. That lineage was merged into main with a non-fast-forward merge before the documentation checkpoint, preserving both the placeholder history and the complete reproduction history.

## Identity policy

Every reachable commit will use this exact author and committer identity:

    MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>

The pre-cleanup history contains Dinesh Jinjala author/committer records and one GitHub noreply committer. The rewrite changes identity metadata only; files and branch roles are preserved.

## Branch rename map

| Old remote branch | New remote branch | Purpose |
| --- | --- | --- |
| main | main | Canonical documentation and complete reproduction lineage |
| orx/baseline-exact-theorem-4-1-contract | audit/theorem-4-1-value-gap | Theorem 4.1 contract and exact baseline |
| orx/exact-certificates-for-theorems-3-2-and-3-3 | audit/theorems-3-2-3-3-exact-certificates | Theorems 3.2 and 3.3 certificates |
| orx/pac-existence-certificate-and-calibrated-n-searc | audit/theorem-3-1-pac-existence | Theorem 3.1 PAC proof and calibration |
| orx/qvbs-ingestion-and-ij-3-calibration | audit/qvbs-ingestion-calibration | Author/QVBS source pinning and ij.3 setup |
| orx/full-nine-benchmark-ten-trial-qvbs-reproduction | release/qvbs-nine-benchmark | Nine-benchmark, ten-trial Claim 5 runner |

## Cleanup checks

Before publication:

- [x] Merge the complete verifier lineage into main.
- [x] README explains the paper, claims, evidence paths, branches, citation, and thank-you note.
- [x] STATUS.md records scientific and publication checkpoints.
- [x] AUTONOMOUS_STATE.json records the next action and pinned sources.
- [x] Target repository name is available.
- [x] Rewrite reachable commit identities.
- [x] Rename the GitHub repository.
- [x] Push descriptive branches and remove old ORX names.
- [x] Verify remote main, branch inventory, README blob, JSON parsing, and commit identities.

## Published state

- Repository: MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality
- Default branch: main
- Main before this final checkpoint commit: 1671b1cb62ec0d8ec192fd0c946ffec22267c69f
- Published branches: main plus audit/theorem-4-1-value-gap, audit/theorems-3-2-3-3-exact-certificates, audit/theorem-3-1-pac-existence, audit/qvbs-ingestion-calibration, release/qvbs-nine-benchmark
- Deleted branch prefix: orx/
- Reachable commit identity: MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>
