"""NetX runtime: ALL hubs running at the same time, in one process, on local data.
Zero *network* latency is real here - the loop makes no network calls; every hub
works on in-memory/local data and a cached snapshot serves repeat reads.
Literal zero *time* is impossible, so NetX measures and prints the honest wall
time instead of claiming zero."""
import time
from concurrent.futures import ThreadPoolExecutor

from .agents import AgentFleet
from .brains import council
from .engines import detect
from .internet import SAMPLE, profile_check
from .learn import QUESTIONS, quiz
from .netlab import tutor
from .network import Device, summarize
from .news import rank
from .shield import smart_scan

POLL_MS = 30  # simulated per-hub poll cycle, labelled - the hub work itself is real


def _job(name, fn, poll_ms):
    t0 = time.perf_counter()
    time.sleep(poll_ms / 1000)  # one poll cycle per hub, all overlapping
    out = fn()
    return name, {"result": out, "ms": round((time.perf_counter() - t0) * 1000, 2)}


def _hub_work():
    devs = [Device("Router", "192.168.1.1", category="Router", trusted=True),
            Device("Unknown ESP", "192.168.1.117", ports=[80])]
    fleet = AgentFleet(); fleet.new_task("Polish the checkout experience")
    return {
        "code": lambda: fleet.board(),
        "network": lambda: summarize(devs),
        "shield": lambda: smart_scan({"os_updated": True})["verdict"],
        "news": lambda: rank("top")[0].title,
        "learn": lambda: quiz([q["answer"] for q in QUESTIONS])["pct"],
        "engines": lambda: detect([]),
        "netlab": lambda: tutor("what is dns")[0]["title"],
        "internet": lambda: profile_check(SAMPLE)["ptr_published"],
        "council": lambda: council("run all hubs at once")["verdict"],
    }


def run_all(poll_ms=POLL_MS):
    """Runs every hub + council concurrently. Wall time ~= the slowest hub,
    NOT the sum - that gap is the parallel proof."""
    work = _hub_work()
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(work)) as ex:
        results = dict(ex.map(lambda kv: _job(kv[0], kv[1], poll_ms), work.items()))
    wall = round((time.perf_counter() - t0) * 1000, 2)
    total = round(sum(v["ms"] for v in results.values()), 2)
    return {"mode": "parallel - all hubs at the same time", "jobs": len(results),
            "results": results, "wall_ms": wall, "sum_if_serial_ms": total,
            "speedup_x": round(total / wall, 1) if wall else None,
            "latency": "zero network latency (in-process, local data, no calls in the loop); "
                       "compute time is measured above, honestly, and is not zero"}


_cache = {}


def snapshot(poll_ms=POLL_MS):
    """Cached full snapshot: first call runs everything in parallel, repeat
    reads are served from memory - that is the zero-latency read path."""
    if "snap" not in _cache:
        _cache["snap"] = run_all(poll_ms)
        return _cache["snap"], False
    return _cache["snap"], True
