# Claim 2 evaluator entry

Fixed command: `uv run --frozen python -m repro.run`

Primary verifier: `repro/claim2.py`. Independent checker: `repro/check_claim2.py`. The command prints raw results, checker output, control output, Git SHA, CPU allocation, and runtime, and exits nonzero if any obligation fails.
