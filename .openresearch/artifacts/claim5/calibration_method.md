# Claim 5 setup calibration

This node is not Claim 5 evidence. It acquires the author implementation at commit `6ffec1273326aede50c8b6516cea1ceb8d920faa` and all nine official QVBS JANI files at commit `c7324a311475ba1a3f40e36a324e32f91e766540`, verifies every SHA-256, then exercises `ij.3` end to end with seed `20260802`.

The frozen uv environment has no third-party dependencies. To keep that contract, the runner supplies standard-library equivalents for the small numerical surface the scientific code uses (`random.choice`, `sqrt`, and `log`), replaces only progress bars and plotting with no-ops, and leaves conversion, learning, BVI, MEC handling, simulation, and stopping logic unchanged. The calibration uses two configured minimum/maximum iterations and is explicitly not promoted as the paper's ten-trial benchmark result.
