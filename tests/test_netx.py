import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from netx.agents import AgentFleet
from netx.brains import council
from netx.catalog import DEDUPE, HUBS, counts
from netx.editor import Document, Library, run_code
from netx.engines import detect, solve, strip_fluff
from netx.gates import HOLD_GATES
from netx.learn import CERTS, QUESTIONS, SECPLUS_DOMAINS, check_lesson, quiz
from netx.netlab import beyond_end, kml_export, subnet_calc, topology_spof, track, tutor
from netx.network import Device, network_map, summarize
from netx.news import deduped, rank, topics
from netx.shield import protection_report, smart_scan
from netx.towers import generations, nearest


def test_catalog_counts():
    c = counts()
    assert c == {"sources": 33, "apps": 18, "own_images": 3, "own_repos": 1,
                 "own_tarballs": 10, "articles": 1, "hubs": 7}
    assert len(DEDUPE) == 7 and len(HUBS) == 7


def test_packages_seats():
    from netx.packages import (SEATS, decon_pipeline, globe_aggregate, mlx_pipeline,
                               s3lf_snapshot, sandbox_triage, slm_bigram, slm_narrow,
                               tpu_schedule, voice_match)
    assert len(SEATS) == 10
    r = mlx_pipeline([[0, 0], [0, 1], [9, 9], [8, 9], [0, 0], [9, 9]],
                     ["a", "a", "b", "b", "a", "b"])
    assert r["accuracy"] == 1.0
    assert slm_narrow("One fish swims. Two fish swim.")["narrowed_from"] == 2
    assert slm_bigram("the cat sat the cat ran", "the", 3) == "the cat sat"
    d = decon_pipeline("just a very messy basically raw idea")
    assert d["stages"] == ["ingest", "fact_snapshot", "pruner", "amplifier", "memory_ml"]
    assert tpu_schedule(["j"] * 65)["busiest_chip_load"] == 2
    assert s3lf_snapshot([{"name": "m1", "weight": 5}], "focus")["top_memory"] == "m1"
    t = sandbox_triage([{"name": "x.ps1"}])
    assert t["executed"] == 0 and t["files"][0]["risk"] == "held-high"
    assert globe_aggregate([("A", 1, 1, 3)])["quadrants"]["NE"]["total_value"] == 3
    assert voice_match({"a": [1, 0]}, [1, 0])["best_label"] == "a"


def test_internet_profile_and_runtime():
    from netx.internet import InternetProfile, SAMPLE, profile_check
    assert profile_check(SAMPLE)["ptr_published"] is False
    real = InternetProfile("Example", "8.8.8.8", hostname="dns.google")
    assert real.has_ptr is True and real.is_public is True
    from netx.runtime import run_all, snapshot
    ra = run_all(poll_ms=20)
    assert ra["jobs"] == 11 and ra["wall_ms"] < ra["sum_if_serial_ms"]
    snapshot()
    _, hit = snapshot()
    assert hit is True


def test_agent_board_and_steer():
    f = AgentFleet()
    f.new_task("Polish the checkout experience")
    s = f.new_task("Security sweep")
    f.steer("Security sweep", "Needs input", "waiting on scope")
    b = f.board()
    assert b["Working"] == 1 and b["Needs input"] == 1 and s.notes == ["waiting on scope"]


def test_editor_metadata_and_library():
    d = Document("Test Document", "import SwiftUI\nstruct A {}\n", ".swift")
    m = d.metadata()
    assert m["language"] == "swift" and m["extension"] == "swift"
    lib = Library(); lib.add(d)
    assert lib.favourite("Test Document") == ["Test Document"]


def test_runner_python_real_others_plan():
    assert run_code("python", "print('hi')")["stdout"].strip() == "hi"
    assert run_code("rust", "fn main(){}")["executed"] is False


def test_inventory_suspicious_and_camera():
    devs = [Device("Router", "192.168.1.1", category="Router", trusted=True),
            Device("Cam", "192.168.1.50", vendor="Reolink", ports=[554]),
            Device("Phone", "192.168.1.9", category="Phones & Tablets", trusted=True)]
    s = summarize(devs)
    assert s["cameras"] == 1 and s["suspicious"] == 1
    assert network_map(devs)["centre"] == "Router"


def test_towers():
    assert generations() == ["2G", "3G", "4G", "5G"]
    n = nearest(34.292, -118.559)
    assert n[0]["name"] == "Porter Ranch North" and n[0]["distance_km"] < 0.1
    assert nearest(34.29, -118.56, generation="5G")[0]["generation"] == "5G"


def test_shield():
    good = {k: True for k in ("os_updated", "passcode_set", "unknown_apps",
                              "wifi_encrypted", "vpn_available", "backups_on")}
    # unknown_apps True means 'no unknown apps' fact key is satisfied in main; here raw:
    r = smart_scan({**good, "backups_on": False})
    assert r["passed"] == 5 and "Backups enabled" in r["failed"]
    assert protection_report([r])["scans"] == 1


def test_news_dedupe_and_rank():
    assert len(deduped()) == 6
    assert rank("discussed")[0].comments >= rank("discussed")[-1].comments
    assert "malware" in topics()


def test_netlab_tutor_subnet_spof_track():
    assert tutor("how does dns work")[0]["title"] == "dns"
    assert subnet_calc("10.0.0.0/30")["usable_hosts"] == 2
    assert topology_spof([("r", "a"), ("r", "b")]) == ["r"]
    roles = [x["role"] for x in track(["1.1.1.1", "2.2.2.2", "3.3.3.3"])]
    assert roles == ["START", "MIDDLE", "END"]
    be = beyond_end(["1.1.1.1"], [("Root DNS", True), ("Dead End", False), ("Never", True)])
    assert be[-1]["role"] == "CAN'T CONNECT" and len(be) == 3
    assert "<coordinates>-118.5,34.29,0</coordinates>" in kml_export("Home", -118.5, 34.29)


def test_learn_quiz_and_lessons():
    assert len(CERTS) == 27 and len(SECPLUS_DOMAINS) == 5
    assert quiz([q["answer"] for q in QUESTIONS])["pct"] == 100
    assert check_lesson("py-math", "print(19+23)")["ok"] is True
    assert check_lesson("py-math", "print(1)")["ok"] is False


def test_engines():
    ev = [{"src": "10.0.0.1", "kind": "http"} for _ in range(55)]
    assert detect(ev)[0]["type"] == "http_flood"
    assert strip_fluff("just run it")["clean"] == "run it"
    assert solve("help me study for my exam")["route"] == "Learn Hub"


def test_council_and_gates():
    c = council("deploy", severity="critical")
    assert c["verdict"] == "HOLD" and c["advisor"]["authority"] == "none"
    assert c["flow"]["rendered"] is False
    assert len(HOLD_GATES) == 16


def test_geo_seat():
    from netx.geo import (demo_pairs, distance_url, get_dist_dur,
                          get_lati_longi, parse_distance, parse_geocode,
                          DISTANCE_SAMPLE, GEOCODE_SAMPLE, static_map_url)
    assert parse_geocode(GEOCODE_SAMPLE) == (50.08138847866026, 14.425403029872987)
    d = parse_distance(DISTANCE_SAMPLE)
    assert d["distance_text"] == "6.7 km" and d["duration_text"] == "23 mins"
    assert d["distance_m"] == 6700 and d["duration_s"] == 1380
    assert parse_geocode({"status": "ZERO_RESULTS", "results": []}) is None
    assert "origins=A" in distance_url("A", "B", "K")
    assert get_lati_longi("X", api_key="")["status"] == "HOLD"
    assert get_dist_dur("A", "B", api_key="")["offline_demo"]["distance_text"] == "6.7 km"
    assert static_map_url(50.08, 14.42, "K")["fetched"] is False
    gp = demo_pairs()
    assert gp["distance"] == "6.7 km" and gp["static_map"] is False
