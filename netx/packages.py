"""Package seats: Darion's 10 tarball projects, merged as real stdlib seats.
Each seat implements the project's documented core in miniature, from its own
README/source audit (2026-11-08, ~/workspace/netx-sources/). Anything the real
project does with hardware, frameworks or live services is labelled, never faked."""
import hashlib
import math
import re
from collections import Counter

# --- ML-x seat (learn): full-stack ML template -> honest tiny ML pipeline ---
def mlx_pipeline(samples, labels, test_ratio=0.25):
    """Nearest-centroid classifier with a deterministic split - the ML-x shape
    (train -> infer -> metric) without claiming PyTorch/TF are bundled."""
    n_test = max(1, int(len(samples) * test_ratio))
    train_x, test_x = samples[:-n_test], samples[-n_test:]
    train_y, test_y = labels[:-n_test], labels[-n_test:]
    centroids = {}
    for x, y in zip(train_x, train_y):
        c = centroids.setdefault(y, [0.0] * len(x))
        for i, v in enumerate(x):
            c[i] += v
    for y, c in centroids.items():
        count = train_y.count(y)
        centroids[y] = [v / count for v in c]
    def predict(x):
        return min(centroids, key=lambda y: sum((a - b) ** 2 for a, b in zip(x, centroids[y])))
    correct = sum(1 for x, y in zip(test_x, test_y) if predict(x) == y)
    return {"frameworks_in_real_project": ["PyTorch", "TensorFlow", "XGBoost", "scikit-learn"],
            "seat_model": "nearest-centroid (stdlib)", "train": len(train_x),
            "test": len(test_x), "accuracy": round(correct / len(test_x), 3) if test_x else 0.0}


# --- slm seat (netlab): Small Language Model Narrower ---
def slm_narrow(text, keep_ratio=0.5):
    """SLM-filter shape: score sentences by word rarity, keep the top slice -
    a big text narrowed to its most information-dense lines."""
    sentences = [s.strip() for s in re.split(r"[.!?]\s+", text) if s.strip()]
    if not sentences:
        return {"kept": [], "narrowed_from": 0}
    freq = Counter(w for s in sentences for w in s.lower().split())
    scored = sorted(sentences, key=lambda s: -sum(1 / freq[w] for w in s.lower().split()))
    keep = max(1, int(len(sentences) * keep_ratio))
    return {"kept": scored[:keep], "narrowed_from": len(sentences), "kept_count": keep}


def slm_bigram(train_text, seed, length=8):
    """The staged-backbone tiny SLM: bigram generation, deterministic by seed word."""
    words = train_text.lower().split()
    nxt = {}
    for a, b in zip(words, words[1:]):
        nxt.setdefault(a, Counter())[b] += 1
    out, cur = [seed], seed
    for _ in range(length - 1):
        if cur not in nxt:
            break
        cur = nxt[cur].most_common(1)[0][0]
        out.append(cur)
    return " ".join(out)


# --- Deconstruction tarball seat (engines): the real 5-stage pipeline ---
DECON_STAGES = ["ingest", "fact_snapshot", "pruner", "amplifier", "memory_ml"]

def decon_pipeline(text):
    from .engines import strip_fluff
    snap = {"chars": len(text), "words": len(text.split()),
            "sha256": hashlib.sha256(text.encode()).hexdigest()[:16]}
    pruned = strip_fluff(text)
    return {"stages": DECON_STAGES, "fact_snapshot": snap,
            "pruned": pruned, "amplified_core": pruned["clean"][:120]}


# --- G-C-64-TPUs seat (engines): 64-chip cluster, scheduling SIMULATION ---
def tpu_schedule(jobs, chips=64):
    """Round-robin job placement over 64 simulated TPUs. No hardware exists here -
    this is the project's cluster design as a scheduler model, labelled as such."""
    loads = [0] * chips
    plan = {}
    for i, job in enumerate(jobs):
        chip = i % chips
        loads[chip] += 1
        plan.setdefault(chip, []).append(job)
    return {"chips": chips, "simulation": True, "jobs": len(jobs),
            "busiest_chip_load": max(loads) if loads else 0, "plan": plan}


# --- S3lf-c0n8ci0us seat (engines): auto-cognitive state snapshot ---
def s3lf_snapshot(memory_items, focus):
    """Conscious-surface shape: master controller reads memory, ranks focus,
    returns a state snapshot. It is a state model - no consciousness is claimed."""
    ranked = sorted(memory_items, key=lambda m: -m.get("weight", 0))
    return {"surface": ["memory_manager", "master_controller", "autonomous_nav",
                        "biological_bridge", "dashboard"],
            "focus": focus, "top_memory": ranked[0]["name"] if ranked else None,
            "memory_items": len(memory_items), "claim": "state model only"}


# --- malware-sandbox-suite seat (shield): the chamber - triage, NEVER executes ---
RISKY_EXT = {".exe", ".dll", ".scr", ".bat", ".ps1", ".vbs", ".js", ".jar", ".docm", ".xlsm"}

def sandbox_triage(files):
    """Static metadata triage over caller-described files (name, size, sha256).
    Mirrors sandbox-api's chamber: files are classified and HELD - nothing is
    opened, run or detonated, ever."""
    out = []
    for f in files:
        ext = "." + f["name"].rsplit(".", 1)[-1].lower() if "." in f["name"] else ""
        risk = "held-high" if ext in RISKY_EXT else "held-review"
        out.append({"name": f["name"], "ext": ext, "risk": risk,
                    "executed": False, "sha256": f.get("sha256", "")[:16]})
    return {"triaged": len(out), "executed": 0, "files": out,
            "note": "static triage only - the chamber never executes samples"}


# --- CyberSec-Directory seat (learn): institute directory + domain-check catalog ---
DIRECTORY = [
    {"name": "Example Institute Alpha", "area": "Delhi-NCR", "tracks": ["Ethical Hacking", "SOC Analyst"], "fee_band": "mid"},
    {"name": "Example Institute Beta", "area": "Delhi-NCR", "tracks": ["VAPT", "Ethical Hacking"], "fee_band": "high"},
    {"name": "Example Institute Gamma", "area": "Delhi-NCR", "tracks": ["SOC Analyst"], "fee_band": "low"},
]
DOMAIN_CHECKS = ["check_ssl_certs", "check_dmarc", "check_dnssec", "check_security_txt",
                 "check_domain_expiry", "check_ipv6_support", "check_site_alive"]

def directory_search(track):
    return [d for d in DIRECTORY if track in d["tracks"]]


# --- Globe-Data-Visualizer seat (network): globe data aggregation ---
def globe_aggregate(points):
    """points: (name, lat, lon, value). Buckets by hemisphere + region grid -
    the visualiser's data layer; rendering is the project's frontend, not claimed here."""
    buckets = {}
    for name, lat, lon, value in points:
        key = ("N" if lat >= 0 else "S") + ("E" if lon >= 0 else "W")
        b = buckets.setdefault(key, {"points": 0, "total_value": 0})
        b["points"] += 1
        b["total_value"] += value
    return {"quadrants": buckets, "points": len(points), "rendered": False}


# --- Ppls voice seat (engines): speaker-embedding MATCHING on supplied vectors ---
def voice_match(enrolled, probe, threshold=0.8):
    """Cosine match between numeric embedding vectors the caller supplies.
    No audio is captured or processed, and no real person is identified -
    this is the project's vector-matching math on abstract vectors only."""
    def cos(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0
    scored = sorted(((name, round(cos(vec, probe), 4)) for name, vec in enrolled.items()),
                    key=lambda t: -t[1])
    best = scored[0] if scored else (None, 0.0)
    return {"best_label": best[0], "score": best[1],
            "match": best[1] >= threshold, "audio_processed": False,
            "note": "abstract supplied vectors only - no audio, no identification of real people"}


SEATS = ["mlx_pipeline", "slm_narrow", "slm_bigram", "decon_pipeline", "tpu_schedule",
         "s3lf_snapshot", "sandbox_triage", "directory_search", "globe_aggregate", "voice_match"]
