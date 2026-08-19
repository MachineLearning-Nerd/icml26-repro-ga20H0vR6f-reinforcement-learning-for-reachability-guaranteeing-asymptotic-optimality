#!/usr/bin/env python3
"""Fail-closed structural checks for the published reachability audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = "MachineLearning-Nerd/icml26-rl-reachability-asymptotic-optimality"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_SOURCE_SHA = (
    "59583e49aea8bf3b4d5104485d22fc62448c7d89ebdef2e4081bf9d4638bb5e2"
)
EXPECTED_BRANCHES = {
    "main",
    "audit/qvbs-ingestion-calibration",
    "audit/theorem-3-1-pac-existence",
    "audit/theorem-4-1-value-gap",
    "audit/theorems-3-2-3-3-exact-certificates",
    "release/qvbs-nine-benchmark",
}
EXPECTED_CLAIMS = {
    "C1": "VERIFIED",
    "C2": "VERIFIED",
    "C3": "VERIFIED",
    "C4": "VERIFIED",
    "C5": "PENDING",
}
EXPECTED_OVERALL_VERDICT = "VERIFIED_CLAIMS_1_TO_4_PENDING_CLAIM_5"
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "REPORT.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "BRANCH_AUDIT.md",
    "ENVIRONMENT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "reproduction_verdicts.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "AUTONOMOUS_STATE.json",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def read_json(relative_path: str) -> object:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(relative_path: str) -> str:
    digest = hashlib.sha256()
    with (ROOT / relative_path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_branches() -> set[str]:
    refs = run(
        "git",
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:strip=2)",
    )
    return {ref.strip() for ref in refs.splitlines() if ref.strip()}


def remote_branches() -> set[str]:
    prefix = "refs/remotes/origin/"
    refs = run(
        "git",
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname)",
    )
    return {
        ref.strip()[len(prefix):]
        for ref in refs.splitlines()
        if ref.strip().startswith(prefix)
        and ref.strip() != prefix + "HEAD"
    }


def verify_remote() -> None:
    remote = run("git", "config", "--get", "remote.origin.url").strip()
    normalized = remote.removesuffix(".git").rstrip("/")
    if not normalized.endswith(EXPECTED_REPOSITORY):
        fail(f"origin is {remote!r}, expected {EXPECTED_REPOSITORY!r}")


def verify_branch_tips() -> None:
    remote = remote_branches()
    if remote != EXPECTED_BRANCHES:
        fail(f"remote branch set is {sorted(remote)!r}")
    local = local_branches()
    if "main" not in local:
        fail("local main branch is missing")
    for branch in EXPECTED_BRANCHES:
        remote_tip = run(
            "git",
            "rev-parse",
            f"refs/remotes/origin/{branch}",
        ).strip()
        if branch in local:
            local_tip = run(
                "git",
                "rev-parse",
                f"refs/heads/{branch}",
            ).strip()
            if local_tip != remote_tip:
                fail(f"local and origin tips differ for {branch}")
    head = run("git", "symbolic-ref", "refs/remotes/origin/HEAD").strip()
    if head != "refs/remotes/origin/main":
        fail(f"origin HEAD is {head!r}, expected origin/main")


def verify_history() -> None:
    records = run(
        "git",
        "log",
        "--all",
        "--format=%an%x00%ae%x00%cn%x00%ce",
    ).splitlines()
    if not records:
        fail("no reachable commits")
    expected = (
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}\x00"
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}"
    )
    unexpected = sorted({record for record in records if record != expected})
    if unexpected:
        fail(f"non-canonical reachable identities: {unexpected}")
    if "Co-authored-by:" in run("git", "log", "--all", "--format=%B"):
        fail("co-author trailer found")
    if int(run("git", "rev-list", "--count", "--all").strip()) < 9:
        fail("historical evidence commits are missing")
    if run(
        "git",
        "for-each-ref",
        "refs/original",
        "--format=%(refname)",
    ).strip():
        fail("temporary refs/original remain")
    refs = run("git", "for-each-ref", "--format=%(refname)").splitlines()
    if any("/orx/" in ref or ref.endswith("/orx") for ref in refs):
        fail("legacy orx ref remains")


def verify_manifest() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    if not isinstance(manifest, dict):
        fail("manifest must be a JSON object")
    if manifest.get("repository") != EXPECTED_REPOSITORY:
        fail("manifest repository marker is wrong")
    if manifest.get("claim_statuses") != EXPECTED_CLAIMS:
        fail("manifest claim statuses are wrong")
    if manifest.get("overall_verdict") != EXPECTED_OVERALL_VERDICT:
        fail("manifest overall verdict is wrong")
    if manifest.get("publication_allowed") is not True:
        fail("manifest publication boundary is wrong")
    if manifest.get("publication_boundary") != "SCOPED_AUDIT_ONLY":
        fail("manifest publication scope is wrong")
    if manifest.get("score_claim") is not False:
        fail("manifest score boundary is wrong")
    if manifest.get("official_author_endorsement") is not False:
        fail("manifest endorsement boundary is wrong")
    expected_audit_files = REQUIRED_FILES
    if set(manifest.get("required_audit_files", [])) != expected_audit_files:
        fail("manifest audit-file list is wrong")
    if set(manifest.get("branches", {}).get("expected_final", [])) != EXPECTED_BRANCHES:
        fail("manifest branch set is wrong")
    if manifest.get("attribution", {}).get("email") != CANONICAL_EMAIL:
        fail("manifest attribution is wrong")
    artifacts = manifest.get("content_addressed_artifacts", [])
    if not artifacts:
        fail("manifest has no content-addressed artifacts")
    for item in artifacts:
        relative_path = item.get("path")
        expected_hash = item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_hash, str):
            fail("malformed content-addressed artifact")
        if not (ROOT / relative_path).is_file():
            fail(f"missing content-addressed artifact: {relative_path}")
        if sha256(relative_path) != expected_hash:
            fail(f"artifact hash mismatch: {relative_path}")


def verify_evidence() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    for relative_path in manifest.get("required_evidence_files", []):
        if not (ROOT / relative_path).is_file():
            fail(f"missing required evidence file: {relative_path}")
    for relative_path in manifest.get("required_evidence_directories", []):
        if not (ROOT / relative_path).is_dir():
            fail(f"missing required evidence directory: {relative_path}")
    if manifest.get("claim_5_evidence_complete") is not False:
        fail("Claim 5 evidence boundary is not explicitly pending")
    tracked = set(run("git", "ls-files").splitlines())
    forbidden_pending_outputs = {
        ".openresearch/artifacts/claim5/raw_results.json",
        ".openresearch/artifacts/claim5/verifier_output.json",
    }
    if tracked & forbidden_pending_outputs:
        fail("generated Claim 5 output is tracked while Claim 5 is pending")


def verify_ledgers_and_state() -> None:
    claims = read_json("claims.json")
    verdicts = read_json("reproduction_verdicts.json")
    state = read_json("AUTONOMOUS_STATE.json")
    if {row.get("id"): row.get("status") for row in claims["claims"]} != EXPECTED_CLAIMS:
        fail("claims.json statuses are wrong")
    if claims.get("repository") != EXPECTED_REPOSITORY:
        fail("claims.json repository marker is wrong")
    if claims.get("paper", {}).get("source_html_sha256") != EXPECTED_SOURCE_SHA:
        fail("claims.json source hash is wrong")
    if claims.get("overall_verdict") != EXPECTED_OVERALL_VERDICT:
        fail("claims.json overall verdict is wrong")
    if claims.get("publication_allowed") is not True:
        fail("claims.json publication boundary is wrong")
    if claims.get("publication_boundary") != "SCOPED_AUDIT_ONLY":
        fail("claims.json publication scope is wrong")
    if claims.get("score_claim") is not False:
        fail("claims.json score boundary is wrong")
    if claims.get("official_author_endorsement") is not False:
        fail("claims.json endorsement boundary is wrong")
    if verdicts.get("repository") != EXPECTED_REPOSITORY:
        fail("reproduction verdict repository marker is wrong")
    if verdicts.get("overall_verdict") != EXPECTED_OVERALL_VERDICT:
        fail("reproduction verdict overall status is wrong")
    if verdicts.get("publication_allowed") is not True:
        fail("reproduction verdict publication boundary is wrong")
    if verdicts.get("publication_boundary") != "SCOPED_AUDIT_ONLY":
        fail("reproduction verdict publication scope is wrong")
    if verdicts.get("score_claim") is not False:
        fail("reproduction verdict score boundary is wrong")
    if verdicts.get("official_author_endorsement") is not False:
        fail("reproduction verdict endorsement boundary is wrong")
    if {
        row.get("id"): row.get("status") for row in verdicts["claims"]
    } != EXPECTED_CLAIMS:
        fail("reproduction verdict statuses are wrong")
    if state.get("target_github_repository") != (
        "https://github.com/" + EXPECTED_REPOSITORY
    ):
        fail("state repository marker is wrong")
    if state.get("canonical_branch") != "main":
        fail("state canonical branch is wrong")
    if state.get("canonical_identity", {}).get("name") != CANONICAL_NAME:
        fail("state canonical identity is wrong")
    if state.get("canonical_identity", {}).get("email") != CANONICAL_EMAIL:
        fail("state canonical email is wrong")
    if state.get("overall_verdict") != EXPECTED_OVERALL_VERDICT:
        fail("state overall verdict is wrong")
    if state.get("publication_allowed") is not True:
        fail("state publication boundary is wrong")
    if state.get("publication_boundary") != "SCOPED_AUDIT_ONLY":
        fail("state publication scope is wrong")
    if state.get("score_claim") is not False:
        fail("state score boundary is wrong")
    if state.get("official_author_endorsement") is not False:
        fail("state endorsement boundary is wrong")
    if state.get("branch_count") != len(EXPECTED_BRANCHES):
        fail("state branch count is wrong")
    if state.get("canonical_identity", {}).get("verified_reachable_commits") != 11:
        fail("state reachable commit checkpoint is wrong")
    if state.get("paper_html_sha256") != EXPECTED_SOURCE_SHA:
        fail("state source hash is wrong")
    if state.get("historical_branch_count") != 5:
        fail("state historical branch count is wrong")
    if set(state.get("expected_branches", [])) != EXPECTED_BRANCHES:
        fail("state branch set is wrong")
    if state.get("phase") not in {
        "dossier_ready_for_publication",
        "dossier_published",
        "published_scoped_audit",
    }:
        fail("state phase is not a published-dossier phase")


def verify_documentation() -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            fail(f"required file is missing: {relative_path}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "CLAIM_EVIDENCE.md",
        "SOURCE_AUDIT.md",
        "BRANCH_AUDIT.md",
        "ENVIRONMENT.md",
        "CITATION.cff",
        "AUTHOR_THANK_YOU.md",
        "reproduction_verdicts.json",
        "AUTONOMOUS_STATE.json",
        "publication_allowed",
        "score_claim",
        "official_author_endorsement",
        "VERIFIED",
        "PENDING",
        "verify_final.py",
    ):
        if marker not in readme:
            fail(f"README is missing marker {marker!r}")
    for relative_path in (
        "candidate/pages/claim-1.md",
        "candidate/pages/claim-2.md",
        "candidate/pages/claim-3.md",
    ):
        page = (ROOT / relative_path).read_text(encoding="utf-8")
        if "Pending HF cpu-upgrade run" in page:
            fail(f"stale pending verdict remains in {relative_path}")
        if "VERIFIED" not in page:
            fail(f"verified verdict is missing in {relative_path}")
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
    if branch_audit.count("| orx/") != 5:
        fail("branch migration table is incomplete")
    source_audit = (ROOT / "SOURCE_AUDIT.md").read_text(encoding="utf-8")
    if EXPECTED_SOURCE_SHA not in source_audit:
        fail("source audit hash is missing")
    thanks = (ROOT / "AUTHOR_THANK_YOU.md").read_text(encoding="utf-8")
    for author in ("Amogh Palasamudram", "Jakub Svoboda", "Suguman Bansal", "Krishnendu"):
        if author not in thanks:
            fail(f"author thanks is missing {author}")


def main() -> int:
    verify_documentation()
    verify_remote()
    verify_branch_tips()
    verify_history()
    verify_manifest()
    verify_evidence()
    verify_ledgers_and_state()
    print("PASS: published reachability audit state is structurally verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
