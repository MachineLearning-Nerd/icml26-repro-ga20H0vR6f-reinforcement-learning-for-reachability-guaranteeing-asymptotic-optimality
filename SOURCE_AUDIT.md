# Source audit

## Paper identity

| Field | Record |
| --- | --- |
| Title | Reinforcement Learning for Reachability: Guaranteeing Asymptotic Optimality |
| Authors | Amogh Palasamudram; Jakub Svoboda; Suguman Bansal; Krishnendu Chatterjee |
| Primary paper | [arXiv:2605.24740](https://arxiv.org/abs/2605.24740) |
| OpenReview record | [ga20H0vR6f](https://openreview.net/forum?id=ga20H0vR6f) |
| Venue marker | ICML 2026 |
| HTML used for theorem anchors | https://ar5iv.labs.arxiv.org/html/2605.24740 |
| HTML SHA-256 | 59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2 |
| Retrieval | 2026-08-02, Asia/Kolkata |
| User-Agent | OpenResearch-Reproduction/1.0 (paper audit; contact via project repository) |

The versioned source and theorem anchors are preserved in
audits/paper_source.md. The hash above is the source record used for the
claim contracts; a newer unpinned rendering is not silently substituted.

## Claim anchors

| Claim | Anchor | Scope used by this repository |
| --- | --- | --- |
| C1 | Theorem 3.1 and Appendix E | Existential PAC witness under finite-MDP, positive-exploration, conservative PAC-BVI assumptions. |
| C2 | Theorem 3.2 and the epsilon-optimal definition | Strict later-stage gap witness; inclusive equality boundary is audited separately. |
| C3 | Theorem 3.3 | Summable post-C2 failure events and first Borel–Cantelli; independence is not assumed. |
| C4 | Theorem 4.1 and Appendix F | Rational, halting finite MDPs with memoryless deterministic policies; zero branch retained. |
| C5 | Section 5.1 and Appendix H Table 1 | Nine QVBS models, ten trials each, paper aggregation and independently reconstructed intervals. |

The per-claim contracts and source audits under
.openresearch/artifacts/ are the authoritative local copies of the exact
quantifiers and limitations.

## External implementation pins

| Input | Pin |
| --- | --- |
| Author implementation | [amoghp214/asymptotic-ltl-reachability](https://github.com/amoghp214/asymptotic-ltl-reachability) at 6ffec1273326aede50c8b6516cea1ceb8d920faa |
| Author archive SHA-256 | 3e82e6daeccc5b9d182c9701023b8171a78f57988112052be7e8e37f6ae5688f |
| Official QVBS source | [ahartmanns/qcomp](https://github.com/ahartmanns/qcomp) at c7324a311475ba1a3f40e36a324e32f91e766540 |

These pins identify the intended Claim 5 inputs. They do not turn a prepared
input into completed benchmark evidence.

## Repository identity

- Former repository:
  icml26-repro-ga20H0vR6f-reinforcement-learning-for-reachability-guaranteeing-asymptotic-optimality
- Canonical repository:
  [MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality](https://github.com/MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality)
- Canonical branch: main
- Repository homepage: https://arxiv.org/abs/2605.24740
