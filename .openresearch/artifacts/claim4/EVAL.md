# Claim 4 evaluation

Status is determined only by the fixed command's exit code and `verifier_output.json`. A passing run must print the exact exhaustive counts, minimum positive gap, digest, independent-checker output, negative-control output, Git SHA, CPU allocation, and runtime between `BEGIN_REPRO_EVIDENCE_JSON` and `END_REPRO_EVIDENCE_JSON`.

The verifier exits nonzero if it encounters a forbidden positive gap, if the independent enumeration disagrees, or if the negative control is accepted.
