#!/usr/bin/env python3
"""NetX - merged pocket system. One interface: python main.py <command>
Commands: catalog, hubs, agents, run, scan, towers, shield, news, tutor,
subnet, track, learn, quiz, engines, council, internet, run-all, checks, demo, hold-demo"""
import json
import sys

from netx import __version__
from netx.agents import AgentFleet
from netx.brains import council
from netx.catalog import DEDUPE, HUBS, SOURCES, counts
from netx.editor import Document, run_code
from netx.engines import detect, solve, strip_fluff
from netx.gates import HOLD_GATES, hold_demo
from netx.learn import CERTS, KALI_TOOLS, QUESTIONS, SECPLUS_DOMAINS, quiz
from netx.netlab import KB, subnet_calc, topology_spof, track, tutor
from netx.network import Device, network_map, port_scan, summarize
from netx.internet import SAMPLE, load_profile, profile_check
from netx.news import deduped, rank
from netx.packages import (decon_pipeline, directory_search, globe_aggregate,
                           mlx_pipeline, sandbox_triage, slm_narrow, tpu_schedule,
                           voice_match)
from netx.runtime import run_all, snapshot
from netx.shield import smart_scan
from netx.towers import generations, nearest

SAMPLE_DEVICES = [
    Device("Askey Router", "192.168.1.1", vendor="Askey", category="Router", trusted=True),
    Device("Darion iPhone", "192.168.1.10", vendor="Apple", category="Phones & Tablets", trusted=True),
    Device("ESP_3A1F7C", "192.168.1.117", vendor="Espressif", category="New device", ports=[80]),
    Device("Hall Camera", "192.168.1.140", vendor="Reolink", category="New device", ports=[554]),
]


def run_checks():
    checks = []
    def ck(name, ok):
        checks.append((name, bool(ok)))
    c = counts()
    ck("32 sources catalogued (18 apps + 3 own images + LLM-X-NetLab + 10 tarballs)",
       c["sources"] == 32 and c["apps"] == 18 and c["own_images"] == 3 and c["own_repos"] == 1 and c["own_tarballs"] == 10)
    ck("7 hubs", c["hubs"] == 7)
    ck("7 dedupe groups merged once", len(DEDUPE) == 7)
    ck("every source lands in a real hub", all(s["hub"] in HUBS for s in SOURCES))
    fleet = AgentFleet(); fleet.new_task("Polish the checkout experience")
    ck("agent board counts Working=1", fleet.board()["Working"] == 1)
    doc = Document("Test Document", "import SwiftUI\n", ".swift")
    ck("editor metadata: swift, 2 lines", doc.metadata()["language"] == "swift" and doc.metadata()["lines"] == 2)
    r = run_code("python", "print(6*7)")
    ck("python runner executes 42", r["executed"] and r["stdout"].strip() == "42")
    ck("non-python language is plan-only, never faked", run_code("go", "package main")["executed"] is False)
    s = summarize(SAMPLE_DEVICES)
    ck("inventory: 4 devices, 2 suspicious (unknown ESP + unknown camera)",
       s["total"] == 4 and s["suspicious"] == 2 and s["cameras"] == 1)
    ck("network map is a star on the router", network_map(SAMPLE_DEVICES)["centre"] == "Askey Router")
    ck("port scan loopback runs", isinstance(port_scan("127.0.0.1", ports=(9,))["open"], list))
    ck("tower generations cover 2G-5G", generations() == ["2G", "3G", "4G", "5G"])
    ck("nearest tower sorts by distance", nearest(34.29, -118.56)[0]["name"] == "Porter Ranch North")
    sc = smart_scan({"os_updated": True, "passcode_set": True, "unknown_apps": False,
                     "wifi_encrypted": True, "vpn_available": True, "backups_on": True})
    ck("smart scan: 5/6, unknown apps flagged", sc["passed"] == 5 and len(sc["failed"]) == 1)
    ck("news dedupe collapses the duplicate GitLab story", len(deduped()) == 6)
    ck("news ranks latest first by age", rank("latest")[0].hours_ago == 1)
    ck("KB has 21 entries", len(KB) == 21)
    ck("tutor answers subnet question from KB", tutor("what is a subnet")[0]["title"] == "subnet")
    sub = subnet_calc("192.168.1.0/24")
    ck("subnet /24 = 254 usable hosts", sub["usable_hosts"] == 254 and sub["broadcast"] == "192.168.1.255")
    ck("topology SPOF finds the star centre",
       topology_spof([("router", "a"), ("router", "b"), ("router", "c")]) == ["router"])
    t = track(["10.0.0.1", "45.1.1.1", "81.1.1.1"])
    ck("tracker labels START/MIDDLE/END", [x["role"] for x in t] == ["START", "MIDDLE", "END"])
    ck("27 certs catalogued", len(CERTS) == 27)
    ck("Security+ has exactly 5 domains", len(SECPLUS_DOMAINS) == 5)
    ck("Kali roster has 12 tools", len(KALI_TOOLS) == 12)
    q = quiz([q_["answer"] for q_ in QUESTIONS])
    ck("quiz: all-correct = 100%", q["pct"] == 100 and q["total"] == len(QUESTIONS))
    ev = [{"src": "10.0.0.9", "kind": "ports", "port": p} for p in range(15)]
    ck("A-C-D detector fires port_scan at >=10 ports", detect(ev)[0]["type"] == "port_scan")
    ck("deconstruction strips fluff", strip_fluff("Basically, just note: it is important to run the scan.")["removed_chars"] > 0)
    ck("sol-plex routes a scan problem to Network Atlas", solve("scan my network")["route"] == "Network Atlas")
    co = council("ship NetX", severity="low")
    ck("council: Carbon 4 decides, Muse advises with no authority",
       co["decider"]["role"] == "DECIDER" and co["advisor"]["authority"] == "none")
    ck("internet seat: sample profile has no PTR (hostname = IP), trends carried",
       profile_check(SAMPLE)["ptr_published"] is False and SAMPLE.trends["performance"] == "Declining fast")
    mlx = mlx_pipeline([[0, 0], [0, 1], [1, 0], [9, 9], [9, 8], [8, 9], [0, 0], [9, 9]],
                       ["a", "a", "a", "b", "b", "b", "a", "b"])
    ck("ML-x seat: pipeline trains and scores accuracy 1.0 on separable data", mlx["accuracy"] == 1.0)
    ck("slm seat narrows 4 sentences to 2", slm_narrow("Cats sleep all day. Quantum flux resonates deeply. Dogs bark. Zebras graze quietly.")["kept_count"] == 2)
    ck("decon tarball seat runs the real 5 stages", decon_pipeline("Basically, just clean this core idea.")["stages"][0] == "ingest")
    ck("TPU seat: 64-chip simulation, 128 jobs -> busiest load 2",
       tpu_schedule([f"job{i}" for i in range(128)])["busiest_chip_load"] == 2)
    tri = sandbox_triage([{"name": "invoice.pdf", "size": 10}, {"name": "update.exe", "size": 99}])
    ck("sandbox chamber triages, executes nothing", tri["executed"] == 0 and tri["files"][1]["risk"] == "held-high")
    ck("directory seat finds VAPT institutes", len(directory_search("VAPT")) == 1)
    ck("globe seat aggregates quadrants, renders nothing",
       globe_aggregate([("A", 10, 20, 5), ("B", -5, -30, 7)])["points"] == 2)
    vm = voice_match({"speaker-a": [1.0, 0.0], "speaker-b": [0.0, 1.0]}, [0.99, 0.01])
    ck("voice seat matches supplied vectors only, no audio", vm["match"] is True and vm["audio_processed"] is False)
    ra = run_all(poll_ms=20)
    ck("runtime: all 10 jobs (7 hubs + internet + packages + council) run at the same time",
       ra["jobs"] == 10 and ra["wall_ms"] < ra["sum_if_serial_ms"])
    snapshot()  # prime the cache with the parallel run
    snap, hit = snapshot()
    ck("snapshot cache serves repeat reads (zero-latency read path)", hit is True and snap["jobs"] == 10)
    ck("15 HOLD gates", len(HOLD_GATES) == 15)
    failed = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {n}")
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


def demo():
    print(f"NetX v{__version__} - {counts()}")
    print("Hubs:", "; ".join(HUBS.values()))
    print("Council:", council("merge 21 sources into NetX")["verdict"])
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "catalog":
        for s in SOURCES:
            print(f"[{s['hub']:7}] {s['name']} - {s['unique']}")
        print(counts())
    elif cmd == "hubs":
        for k, v in HUBS.items():
            print(f"{k}: {v}")
    elif cmd == "agents":
        f = AgentFleet(); f.new_task("Polish the checkout experience")
        f.new_task("Find and remediate vulnerabilities"); print(f.board())
    elif cmd == "run":
        print(json.dumps(run_code(argv[1], argv[2]), indent=2))
    elif cmd == "scan":
        print(json.dumps(summarize(SAMPLE_DEVICES), indent=2))
    elif cmd == "towers":
        print(json.dumps(nearest(34.29, -118.56), indent=2))
    elif cmd == "shield":
        print(smart_scan({k: True for k in
              ("os_updated", "passcode_set", "unknown_apps", "wifi_encrypted", "vpn_available", "backups_on")}))
    elif cmd == "news":
        for a in rank(argv[1] if len(argv) > 1 else "top"):
            print(f"- ({a.source}) {a.title}")
    elif cmd == "tutor":
        print(json.dumps(tutor(" ".join(argv[1:])), indent=2))
    elif cmd == "subnet":
        print(subnet_calc(argv[1]))
    elif cmd == "track":
        print(track(argv[1:]))
    elif cmd == "learn":
        print(f"Kali tools: {', '.join(KALI_TOOLS)}\nCerts: {len(CERTS)} | Security+ domains: {len(SECPLUS_DOMAINS)}")
    elif cmd == "quiz":
        print(quiz([int(x) for x in argv[1:]]))
    elif cmd == "engines":
        print(solve(" ".join(argv[1:]) or "scan my network"))
    elif cmd == "internet":
        prof, src = load_profile()
        out = profile_check(prof); out["profile_source"] = src
        print(json.dumps(out, indent=2))
    elif cmd == "packages":
        print("ML-x:", mlx_pipeline([[0, 0], [0, 1], [9, 9], [8, 9], [0, 0], [9, 9]],
                                   ["a", "a", "b", "b", "a", "b"]))
        print("Sandbox:", sandbox_triage([{"name": "sample.exe", "size": 1}]))
        print("TPU:", tpu_schedule(["train", "infer", "eval"])["jobs"], "jobs on 64 simulated chips")
    elif cmd == "run-all":
        print(json.dumps(run_all(), indent=2))
    elif cmd == "council":
        print(json.dumps(council(" ".join(argv[1:]) or "NetX"), indent=2))
    elif cmd == "checks":
        return run_checks()
    elif cmd == "demo":
        return demo()
    elif cmd == "hold-demo":
        print(json.dumps(hold_demo(), indent=2))
        return 2
    else:
        print(f"unknown command: {cmd}\n{__doc__}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
