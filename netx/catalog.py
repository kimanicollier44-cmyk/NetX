"""Source catalog: every screenshot Darion supplied, where it landed in NetX,
and what was deduped. Nothing unique was dropped; duplicates were merged once."""

SOURCES = [
    # Batch 1 - App Store
    {"name": "Kilo Code: Code with AI Agents", "kind": "app", "hub": "code",
     "unique": "AI agent sessions in your pocket: Needs input / Working / Scheduled / Idle, steer agents, run-on target machine"},
    {"name": "QuickCode: Code Editor", "kind": "app", "hub": "code",
     "unique": "Code editor with document metadata (title, extension, size) and syntax-aware documents"},
    {"name": "Code - Compile & Run Program", "kind": "app", "hub": "code",
     "unique": "Compile & run instantly, 12-language file library, favourites"},
    {"name": "Crios: Network Scanner & Map", "kind": "app", "hub": "network",
     "unique": "Wi-Fi analyzer, IP & port scan, live network map, device inventory with unknowns flagged"},
    {"name": "Cellular Tower - Signal Finder", "kind": "app", "hub": "network",
     "unique": "All cellular towers 2G/3G/4G/5G on a map, nearest-tower signal finder"},
    {"name": "Cyber Security News & Reports", "kind": "app", "hub": "news",
     "unique": "Threats / breaches / research feed, Top / Latest / Most Discussed, multi-source stories"},
    {"name": "CyberNews - Cyber Security", "kind": "app", "hub": "news",
     "unique": "Threats / hacks / malware / prevention feed, trending, sites, topics, bookmarks"},
    {"name": "Learn Kali Linux & Hacking", "kind": "app", "hub": "learn",
     "unique": "Kali curriculum: 4 courses, 125 topics, 17 hours, 12-tool roster (Nmap to Nikto)"},
    {"name": "Pocket Prep IT & Cybersecurity", "kind": "app", "hub": "learn",
     "unique": "Exam prep for 27 IT/cyber certs, Question of the Day, Quick 10 Quiz, streaks"},
    {"name": "Mimo: Learn Python Coding & AI", "kind": "app", "hub": "learn",
     "unique": "Bite-size interactive coding lessons (Python/JS/TS/SQL/Swift) with in-lesson runs"},
    # Batch 2 - App Store
    {"name": "CompTIA Security+ Exam Prep", "kind": "app", "hub": "learn",
     "unique": "Security+ SY0-701 track: 5 official domains, study-by-topic, 1,000+ question model"},
    {"name": "HackerX: Learn Ethical Hacking", "kind": "app", "hub": "learn",
     "unique": "Bite-size practical hacking guide: footprinting, Wi-Fi/WEP, monitor mode, packet sniffing"},
    {"name": "Norton 360 Mobile Security VPN", "kind": "app", "hub": "shield",
     "unique": "360 Smart Scan, malware scan, VPN seat, 90-day Protection Report"},
    {"name": "Nearby Device Detector: Scan", "kind": "app", "hub": "network",
     "unique": "Radar device detection, suspicious-device count, confirmed status, ping/trace/remove management"},
    {"name": "TP-Link Tether", "kind": "app", "hub": "network",
     "unique": "Router management, parental controls, network reports, prevented-risk counts"},
    {"name": "Network Analyzer: WiFi Scan", "kind": "app", "hub": "network",
     "unique": "LAN scanner with MAC/vendor, ping, DNS, whois and traceroute tools, service flags"},
    {"name": "Hidden Camera Detector - Peek", "kind": "app", "hub": "network",
     "unique": "Spy-camera hunt: suspicious vs secure devices, camera heuristics, magnetic-detector seat"},
    # Batch 2 - Darion's own Docker Hub images (core engines)
    {"name": "credkellar/a-c-d-matrix-force", "kind": "own-image", "hub": "engines",
     "unique": "Packet dissection + port-scan/DoS/HTTP-flood detection core (123 pulls in screenshot)"},
    {"name": "credkellar/deconstruction", "kind": "own-image", "hub": "engines",
     "unique": "Deconstruction engine: strip fluff, optimize core logic, solve complex problems (678 pulls)"},
    {"name": "credkellar/sol-plex-problems", "kind": "own-image", "hub": "engines",
     "unique": "Cloud cognitive problem solver with secure quantum logic (1.9K pulls, 2 stars)"},
    {"name": "Fing - Network Tools (Internet tab)", "kind": "app", "hub": "network",
     "unique": "ISP internet profile (public IP, hostname/PTR, location, timezone), trend cards, user rating, 24/7 monitoring seat - owner's real profile stays in private/, never in the repo"},
    # Batch 4 - Darion's own project tarballs (v1.3.0, audited from source)
    {"name": "ML-x 0.1.0 (tarball)", "kind": "own-tarball", "hub": "learn",
     "unique": "Full-stack ML template (Next.js + FastAPI, PyTorch/TF/XGBoost/sklearn) - seat: honest stdlib ML pipeline with real accuracy metric"},
    {"name": "slm 0.1.0 (tarball)", "kind": "own-tarball", "hub": "netlab",
     "unique": "Small Language Model Narrower: slm_filter pipeline - seat: sentence-rarity narrowing + bigram SLM"},
    {"name": "Deconstruction 0.1.0 (tarball)", "kind": "own-tarball", "hub": "engines",
     "unique": "The fuller Deconstruction source: ingest -> fact_snapshot -> pruner -> amplifier -> memory_ml (upgrades the image seat, not a duplicate)"},
    {"name": "G-C-64-TPUs 0.1.0 (tarball)", "kind": "own-tarball", "hub": "engines",
     "unique": "64-TPU cluster design (Rust, 142 files) - seat: round-robin cluster scheduler, labelled simulation"},
    {"name": "S3lf-c0n8ci0us 0.1.0 (tarball)", "kind": "own-tarball", "hub": "engines",
     "unique": "Auto-cognitive reasoning surface (memory_manager, master_controller, autonomous_nav, biological_bridge) - seat: state snapshot, no consciousness claimed"},
    {"name": "malware-sandbox-suite 0.1.0 (tarball)", "kind": "own-tarball", "hub": "shield",
     "unique": "Sandbox suite (100 files: analyzer, api_gateway, cluster, audit) - seat: static triage chamber that NEVER executes samples"},
    {"name": "CyberSec-Directory 0.1.0 (tarball)", "kind": "own-tarball", "hub": "learn",
     "unique": "Delhi-NCR cyber training institute directory + 7 domain-check scripts (SSL, DMARC, DNSSEC, security.txt, expiry, IPv6, alive)"},
    {"name": "Globe-Data-Visualizer 0.2.0 (tarball)", "kind": "own-tarball", "hub": "network",
     "unique": "Globe data visualisation - seat: quadrant aggregation of geo data points (rendering stays the project's frontend)"},
    {"name": "Ppls-voice-recognition-speaker 0.1.0 (tarball)", "kind": "own-tarball", "hub": "engines",
     "unique": "Speaker-recognition ecosystem (ECAPA embeddings, C++ vector matching, Monad anchoring) - seat: cosine matching on supplied abstract vectors only, no audio, no identification"},
    {"name": "LLM-x 0.1.5 (tarball)", "kind": "own-tarball", "hub": "netlab",
     "unique": "Package form of the LLM-x architecture (34 files) - same family as LLM-X-NetLab repo, deduped into the one NetLab seat"},
    # Batch 3 - Darion's own repo, merged in full
    # Batch 4 - article supplied by video + link (Darion, 2026-11-08)
    {"name": "Apify guide: Google Maps API in Python", "kind": "article", "hub": "network",
     "unique": "Geocoding (address -> lat/lng, get_lati_longi) + Distance Matrix driving distance/duration (get_dist_dur) + Static Maps next step, as a stdlib seat; live calls need the owner's GOOGLE_MAPS_API_KEY"},
    {"name": "credkellar/LLM-X-NetLab", "kind": "own-repo", "hub": "netlab",
     "unique": "LLM-x poster as code: RAG tutor over 21 networking notes, subnet/topology/layer/device engines, IP hopper-tracker-mapper START/MIDDLE/END + beyond-END walker, live sockets, Earth KML + Flow seats"},
]

HUBS = {
    "code": "Code Studio - agents + editor + compile & run (3 apps, 1 studio)",
    "network": "Network Atlas - LAN map, port scan, radar, router, towers, camera hunt (6 apps, 1 atlas)",
    "shield": "Shield - Smart Scan, malware checklist, VPN seat, protection report (Norton 360)",
    "news": "Threat News Wire - both cyber-news apps merged into one deduped feed",
    "learn": "Learn Hub - Kali + HackerX + Mimo interactive + Pocket Prep + Security+ SY0-701 (5 apps, 3 tracks)",
    "engines": "Core Engines - A-C-D detection, Deconstruction optimizer, Sol-Plex solver (his 3 images)",
    "netlab": "NetLab - LLM-X-NetLab merged: RAG tutor, subnet/topology/layer engines, tracker + beyond-END walker, KML",
}

# Duplicate groups merged exactly once - the 'perfectly' part.
DEDUPE = [
    ("news feed", ["Cyber Security News & Reports", "CyberNews - Cyber Security"],
     "ONE feed engine: ranking (top/latest/discussed) + trending/topics/bookmarks kept from both"),
    ("device scanner", ["Crios: Network Scanner & Map", "Nearby Device Detector: Scan",
                         "Network Analyzer: WiFi Scan", "Hidden Camera Detector - Peek"],
     "ONE inventory: map + radar + ping/DNS/whois/route tools + camera heuristic kept from all four"),
    ("code on phone", ["Kilo Code: Code with AI Agents", "QuickCode: Code Editor",
                       "Code - Compile & Run Program"],
     "ONE studio: agent sessions + editor/metadata + multi-language runner kept from all three"),
    ("hacking lessons", ["Learn Kali Linux & Hacking", "HackerX: Learn Ethical Hacking"],
     "ONE curriculum: Kali course structure + HackerX bite-size practical modules kept from both"),
    ("exam prep", ["Pocket Prep IT & Cybersecurity", "CompTIA Security+ Exam Prep"],
     "ONE exam engine: 27-cert catalog + SY0-701 deep track (5 domains, study-by-topic) kept from both"),
    ("LLM-x twice", ["credkellar/LLM-X-NetLab", "LLM-x 0.1.5 (tarball)"],
     "ONE NetLab seat: the repo build is canonical; the tarball's package structure is recorded, not duplicated"),
    ("deconstruction twice", ["credkellar/deconstruction", "Deconstruction 0.1.0 (tarball)"],
     "ONE engine: the tarball's 5-stage pipeline (ingest/fact_snapshot/pruner/amplifier/memory_ml) upgrades the image seat"),
]


def hub_of(name):
    for s in SOURCES:
        if s["name"] == name:
            return s["hub"]
    return None


def counts():
    apps = sum(1 for s in SOURCES if s["kind"] == "app")
    own = sum(1 for s in SOURCES if s["kind"] == "own-image")
    repos = sum(1 for s in SOURCES if s["kind"] == "own-repo")
    tarballs = sum(1 for s in SOURCES if s["kind"] == "own-tarball")
    articles = sum(1 for s in SOURCES if s["kind"] == "article")
    return {"sources": len(SOURCES), "apps": apps, "own_images": own,
            "own_repos": repos, "own_tarballs": tarballs, "articles": articles,
            "hubs": len(HUBS)}
