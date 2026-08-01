import json
import os
import platform
import subprocess
import time
from pathlib import Path

from repro.check_claim4 import independent_check
from repro.claim4 import negative_control, run_exhaustive_check


ARTIFACTS = Path(".openresearch/artifacts/claim4")


def write_json(name, value):
    path = ARTIFACTS / name
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_sha():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def main():
    started = time.monotonic()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    result = run_exhaustive_check()
    checker = independent_check(result)
    control = negative_control()
    passed = result["theorem_disjunction_holds"] and checker["passed"] and control["control_rejected_as_intended"]
    metadata = {
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "estimated_cores": 1,
        "os_cpu_count": os.cpu_count(),
        "cpu_affinity_count": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "seeds": [],
        "runtime_seconds": time.monotonic() - started,
    }
    verdict = {
        "claim": "Theorem 4.1",
        "status": "VERIFIED" if passed else "BLOCKED",
        "scope": "symbolic denominator certificate plus exhaustive complete finite rational subdomain",
        "passed": passed,
        "result": result,
        "independent_checker": checker,
        "negative_control": control,
        "metadata": metadata,
    }
    write_json("raw_results.json", result)
    write_json("independent_checker_output.json", checker)
    write_json("negative_control_output.json", control)
    write_json("verifier_output.json", verdict)
    print("BEGIN_REPRO_EVIDENCE_JSON")
    print(json.dumps(verdict, indent=2, sort_keys=True))
    print("END_REPRO_EVIDENCE_JSON")
    print(f"REPRO_SUMMARY claim4={verdict['status']} runtime_seconds={metadata['runtime_seconds']:.3f}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
