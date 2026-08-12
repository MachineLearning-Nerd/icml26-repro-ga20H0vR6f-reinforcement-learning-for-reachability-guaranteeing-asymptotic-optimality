# Claim 1 evaluator entry

Fixed command: `uv run --frozen python -m repro.run`

Primary verifier: `repro/claim1.py`. Independent checker: `repro/check_claim1.py`. The command prints exact quantifiers, calibrated minimum resources, controls, Git SHA, CPU allocation, and runtime, and exits nonzero on any failed obligation.
