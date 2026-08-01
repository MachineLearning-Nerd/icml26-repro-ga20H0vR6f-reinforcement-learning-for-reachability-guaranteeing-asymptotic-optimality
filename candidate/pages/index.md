# Current verification

This candidate begins with the current verifier. Historical pages from the judged Space will be preserved additively at release and labeled **Historical rejected baseline**.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Theorem 3.1](claim-1.md) | `repro/claim1.py` | Pending cumulative run | `.openresearch/artifacts/claim1/raw_results.json` | `repro/check_claim1.py` | `N-1`; zero exploration | Yes, exact existential quantifiers | Pending |
| 2 | [Theorem 3.2](claim-2.md) | `repro/claim2.py` | Pending cumulative run | `.openresearch/artifacts/claim2/raw_results.json` | `repro/check_claim2.py` | equality boundary | Yes, including strict-boundary repair | Pending |
| 3 | [Theorem 3.3](claim-3.md) | `repro/claim3.py` | Pending cumulative run | `.openresearch/artifacts/claim3/raw_results.json` | `repro/check_claim3.py` | harmonic schedule | Yes, no independence assumed | Pending |
| 4 | [Theorem 4.1](claim-4.md) | `repro/claim4.py` | 5,537 halting MDPs; 33,222 pairs; min positive gap `1/4` | `.openresearch/artifacts/claim4/raw_results.json` | `repro/check_claim4.py` | bound/2 injection | Yes, including zero branch and assumptions | VERIFIED on complete finite subdomain |

Claim 5 is not yet release-ready. Claim 1 remains pending until the cumulative remote verifier completes.
