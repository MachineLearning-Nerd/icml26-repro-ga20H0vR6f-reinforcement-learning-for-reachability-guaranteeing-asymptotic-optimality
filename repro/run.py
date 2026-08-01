import json
import os
import platform
import subprocess
import time
from pathlib import Path

from repro.check_claim1 import independent_check as independent_check_claim1
from repro.check_claim2 import independent_check as independent_check_claim2
from repro.check_claim3 import independent_check as independent_check_claim3
from repro.check_claim4 import independent_check as independent_check_claim4
from repro.claim1 import negative_control as negative_control_claim1
from repro.claim1 import run_pac_existence_certificate
from repro.claim2 import negative_control as negative_control_claim2
from repro.claim2 import run_gap_certificate
from repro.claim3 import negative_control as negative_control_claim3
from repro.claim3 import run_borel_cantelli_certificate
from repro.claim4 import negative_control as negative_control_claim4
from repro.claim4 import run_exhaustive_check
from repro.qvbs_full import independent_check as independent_check_qvbs
from repro.qvbs_full import negative_control as negative_control_qvbs
from repro.qvbs_full import run_full_benchmarks


ARTIFACTS = Path(".openresearch/artifacts")


def write_json(relative_path, value):
    path = ARTIFACTS / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_sha():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def main():
    started = time.monotonic()
    claim1_result = run_pac_existence_certificate()
    claim1_checker = independent_check_claim1(claim1_result)
    claim1_control = negative_control_claim1(claim1_result)
    claim1_passed = claim1_result["passed"] and claim1_checker["passed"] and claim1_control["control_rejected_as_intended"]
    claim4_result = run_exhaustive_check()
    claim4_checker = independent_check_claim4(claim4_result)
    claim4_control = negative_control_claim4()
    claim4_passed = claim4_result["theorem_disjunction_holds"] and claim4_checker["passed"] and claim4_control["control_rejected_as_intended"]
    claim2_result = run_gap_certificate()
    claim2_checker = independent_check_claim2()
    claim2_control = negative_control_claim2()
    claim2_passed = claim2_result["passed"] and claim2_checker["passed"] and claim2_control["control_rejected_as_intended"]
    claim3_result = run_borel_cantelli_certificate()
    claim3_checker = independent_check_claim3()
    claim3_control = negative_control_claim3()
    claim3_passed = claim3_result["passed"] and claim3_checker["passed"] and claim3_control["control_rejected_as_intended"]
    qvbs_result = run_full_benchmarks(Path(".openresearch/work/qvbs-full"))
    qvbs_checker = independent_check_qvbs(qvbs_result)
    qvbs_control = negative_control_qvbs(qvbs_result)
    qvbs_passed = qvbs_checker["passed"] and qvbs_control["control_rejected_as_intended"]
    passed = claim1_passed and claim2_passed and claim3_passed and claim4_passed and qvbs_passed
    metadata = {
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "estimated_cores": 32,
        "os_cpu_count": os.cpu_count(),
        "cpu_affinity_count": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "seeds": [trial["seed"] for trial in qvbs_result["trials"]],
        "runtime_seconds": time.monotonic() - started,
    }
    verdicts = {
        "claim1": {
            "claim": "Theorem 3.1",
            "status": "VERIFIED" if claim1_passed else "BLOCKED",
            "scope": "independently reconstructed existence proof, exact minimum-N calibration, and adaptive-process checker",
            "passed": claim1_passed,
            "result": claim1_result,
            "independent_checker": claim1_checker,
            "negative_control": claim1_control,
        },
        "claim2": {
            "claim": "Theorem 3.2",
            "status": "VERIFIED" if claim2_passed else "BLOCKED",
            "scope": "universal symbolic implication, exact stage witness, and exhaustive finite rational-spectrum audit",
            "passed": claim2_passed,
            "result": claim2_result,
            "independent_checker": claim2_checker,
            "negative_control": claim2_control,
        },
        "claim3": {
            "claim": "Theorem 3.3",
            "status": "VERIFIED" if claim3_passed else "BLOCKED",
            "scope": "machine-checked summability and first Borel-Cantelli derivation",
            "passed": claim3_passed,
            "result": claim3_result,
            "independent_checker": claim3_checker,
            "negative_control": claim3_control,
        },
        "claim4": {
            "claim": "Theorem 4.1",
            "status": "VERIFIED" if claim4_passed else "BLOCKED",
            "scope": "symbolic denominator certificate plus exhaustive complete finite rational subdomain",
            "passed": claim4_passed,
            "result": claim4_result,
            "independent_checker": claim4_checker,
            "negative_control": claim4_control,
        },
    }
    for claim, verdict in verdicts.items():
        write_json(f"{claim}/raw_results.json", verdict["result"])
        write_json(f"{claim}/independent_checker_output.json", verdict["independent_checker"])
        write_json(f"{claim}/negative_control_output.json", verdict["negative_control"])
        write_json(f"{claim}/verifier_output.json", {**verdict, "metadata": metadata})
    cumulative = {"passed": passed, "verdicts": verdicts, "metadata": metadata}
    cumulative["claim5"] = {
        "passed": qvbs_passed,
        "status": "VERIFIED" if qvbs_passed else "BLOCKED",
        "result": qvbs_result,
        "independent_checker": qvbs_checker,
        "negative_control": qvbs_control,
    }
    write_json("claim5/raw_results.json", qvbs_result)
    write_json("claim5/independent_checker_output.json", qvbs_checker)
    write_json("claim5/negative_control_output.json", qvbs_control)
    write_json("claim5/verifier_output.json", {**cumulative["claim5"], "metadata": metadata})
    write_json("cumulative_verifier_output.json", cumulative)
    print("BEGIN_REPRO_EVIDENCE_JSON")
    print(json.dumps(cumulative, indent=2, sort_keys=True))
    print("END_REPRO_EVIDENCE_JSON")
    print(
        "REPRO_SUMMARY "
        f"claim1={verdicts['claim1']['status']} "
        f"claim2={verdicts['claim2']['status']} "
        f"claim3={verdicts['claim3']['status']} "
        f"claim4={verdicts['claim4']['status']} "
        f"claim5={cumulative['claim5']['status']} "
        f"runtime_seconds={metadata['runtime_seconds']:.3f}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
