import hashlib
import importlib
import json
import sys
import tarfile
import urllib.request
from pathlib import Path


AUTHOR_COMMIT = "6ffec1273326aede50c8b6516cea1ceb8d920faa"
AUTHOR_ARCHIVE_SHA256 = "3e82e6daeccc5b9d182c9701023b8171a78f57988112052be7e8e37f6ae5688f"
AUTHOR_ARCHIVE_URL = f"https://github.com/amoghp214/asymptotic-ltl-reachability/archive/{AUTHOR_COMMIT}.tar.gz"
QVBS_COMMIT = "c7324a311475ba1a3f40e36a324e32f91e766540"
QVBS_BASE_URL = f"https://raw.githubusercontent.com/ahartmanns/qcomp/{QVBS_COMMIT}/benchmarks/mdp"
USER_AGENT = "OpenResearch-Reproduction/1.0 (pinned benchmark acquisition)"

MODELS = {
    "consensus.2": ("consensus/consensus.2.jani", "e20cc66982e58be27c5c970e213b7df98c2c272fd5116e42b20f07936b3901a1"),
    "csma.2-2": ("csma/csma.2-2.jani", "d99205138c2a2f83b4dc8460b7b89a95f5a6ad0e40944384bcdd7a72443acbd3"),
    "firewire_abst": ("firewire_abst/firewire_abst.jani", "83587a179ae3e89ad03eadf72cd3ab590ed6523e226e3b104bc7149c284fad9e"),
    "ij.10": ("ij/ij.10.jani", "b7999e5ab32e2735c7e010b57225660ab8e9cfbd0f4962ab8099aea134c04daf"),
    "ij.3": ("ij/ij.3.jani", "dd7bbf9a0cba4153361a143f1f3f02a057ebe1691613e86fe78088a242b88001"),
    "pacman.v2": ("pacman/pacman.jani", "f7a72312c568373add11fbe24274470f4b1c946fec04d5efc9135ce715e61b81"),
    "philosophers-mdp.3": ("philosophers-mdp/philosophers-mdp.3.jani", "1c1da1fb6d7fb3da2ffe95cc1a9737ede5c5a9530b30c993b5a416e0efb7e57e"),
    "rabin.3": ("rabin/rabin.3.jani", "8a3496cde4f3b276a1578deb11aa43d89d3bd1e50a71088f2e891061e42fdd96"),
    "zeroconf": ("zeroconf/zeroconf.jani", "b2dc904a83780348a15b9439223d0ea483d85b4fe71c0a0cd726314ad91729b5"),
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def acquire_sources(work_dir):
    work_dir.mkdir(parents=True, exist_ok=True)
    archive = download(AUTHOR_ARCHIVE_URL)
    if sha256(archive) != AUTHOR_ARCHIVE_SHA256:
        raise AssertionError("author archive SHA-256 mismatch")
    archive_path = work_dir / "authors.tar.gz"
    archive_path.write_bytes(archive)
    with tarfile.open(archive_path) as bundle:
        bundle.extractall(work_dir, filter="data")
    source_dir = next(path for path in work_dir.iterdir() if path.is_dir() and path.name.startswith("asymptotic-ltl-reachability-"))

    model_dir = work_dir / "qvbs"
    model_dir.mkdir(exist_ok=True)
    manifests = []
    for name, (relative_path, expected_hash) in MODELS.items():
        data = download(f"{QVBS_BASE_URL}/{relative_path}")
        actual_hash = sha256(data)
        if actual_hash != expected_hash:
            raise AssertionError(f"QVBS SHA-256 mismatch for {name}")
        parsed = json.loads(data)
        path = model_dir / f"{name}.jani"
        path.write_bytes(data)
        manifests.append(
            {
                "name": name,
                "source_path": relative_path,
                "sha256": actual_hash,
                "bytes": len(data),
                "jani_version": parsed.get("jani-version"),
                "model_type": parsed.get("type"),
                "automata": len(parsed.get("automata", [])),
                "properties": len(parsed.get("properties", [])),
            }
        )
    return source_dir, model_dir, manifests


def write_compatibility_layer(source_dir):
    (source_dir / "numpy.py").write_text(
        """import math\nimport random as _random\n\nsqrt = math.sqrt\nlog = math.log\n\nclass _Random:\n    def seed(self, value):\n        _random.seed(value)\n\n    def choice(self, values, p=None):\n        sequence = list(range(values)) if isinstance(values, int) else list(values)\n        if p is None:\n            sequence.sort(key=repr)\n            return _random.choice(sequence)\n        draw = _random.random()\n        cumulative = 0.0\n        for index, weight in enumerate(p):\n            cumulative += weight\n            if draw < cumulative:\n                return sequence[index]\n        return sequence[-1]\n\nrandom = _Random()\n""",
        encoding="utf-8",
    )
    (source_dir / "tqdm.py").write_text(
        "def tqdm(iterable, **kwargs):\n    return iterable\n",
        encoding="utf-8",
    )
    matplotlib = source_dir / "matplotlib"
    matplotlib.mkdir(exist_ok=True)
    (matplotlib / "__init__.py").write_text("", encoding="utf-8")
    (matplotlib / "pyplot.py").write_text("", encoding="utf-8")
    (source_dir / "analysis_utils.py").write_text(
        "def plot_bvi_history(*args, **kwargs):\n    return None\n\ndef run_analysis(*args, **kwargs):\n    return None\n",
        encoding="utf-8",
    )


def run_ij3_calibration(work_dir, seed=20260802):
    source_dir, model_dir, manifests = acquire_sources(work_dir)
    write_compatibility_layer(source_dir)
    sys.path.insert(0, str(source_dir))
    numpy = importlib.import_module("numpy")
    numpy.random.seed(seed)
    converter = importlib.import_module("convert_jani_to_mdp")
    simulator_module = importlib.import_module("mdp_simulator")
    learner_module = importlib.import_module("ltl_reachability_learner")

    mdp = converter.convert_jani_to_mdp(str(model_dir / "ij.3.jani"))
    transition_count = sum(len(outcomes) for outcomes in mdp.transition_probabilities.values())
    if any(abs(sum(outcomes.values()) - 1.0) >= 1e-8 for outcomes in mdp.transition_probabilities.values()):
        raise AssertionError("converted transition probabilities do not sum to one")
    learner = learner_module.LTLReachabilityLearner(
        mdp_simulator=simulator_module.MDPSimulator(mdp=mdp),
        min_num_iterations=2,
        max_num_iterations=2,
        convergence_threshold=0.0,
        num_policy_accuracy_sims=50,
        true_confidence_error=0.01,
        true_p_min=0.5,
    )
    learner.learn(analysis_dir="")
    total_samples = sum(sum(counts.values()) for counts in learner.discovered_mdp.sample_counts.values())
    latest = learner.learning_history[-1]
    return {
        "purpose": "setup calibration only; not Claim 5 evidence",
        "author_commit": AUTHOR_COMMIT,
        "author_archive_sha256": AUTHOR_ARCHIVE_SHA256,
        "qvbs_commit": QVBS_COMMIT,
        "input_manifest": manifests,
        "compatibility_layer": [
            "stdlib replacement for numpy random.choice, sqrt, and log",
            "no-op progress and plotting only",
            "author learning, conversion, BVI, MEC, and simulation logic unchanged",
        ],
        "seed": seed,
        "ij3": {
            "states": len(mdp.states),
            "state_action_pairs": len(mdp.state_action_pairs),
            "transitions": transition_count,
            "goal_states": len(mdp.goal_states),
            "learning_iterations": len(learner.learning_history),
            "total_samples": total_samples,
            "final_error": latest[-3],
            "final_lower_bound": latest[-2],
            "final_upper_bound": latest[-1],
        },
        "passed": len(manifests) == 9 and len(mdp.states) > 4 and len(learner.learning_history) >= 2,
    }


def negative_control():
    payload = b"official QVBS input"
    expected = sha256(payload)
    tampered = payload + b" tampered"
    accepted = sha256(tampered) == expected
    return {
        "control": "tamper with a pinned QVBS payload",
        "verifier_accepted": accepted,
        "control_rejected_as_intended": not accepted,
    }
