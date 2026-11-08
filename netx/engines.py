"""Core Engines - Darion's own 3 Docker images, as seats inside NetX.
Detection thresholds are A-C-D-Matrix-FORCE's exact published values."""

# --- A-C-D-Matrix-FORCE detection seat ---
THRESHOLDS = {"port_scan": 10, "dos": 100, "http_flood": 50}  # flood = per minute


def detect(events):
    """events: list of dicts {src, kind} where kind in ports/dos/http, flood pre-windowed."""
    alerts = []
    ports, dos, http = {}, {}, {}
    for e in events:
        src = e["src"]
        if e["kind"] == "ports":
            ports.setdefault(src, set()).add(e.get("port"))
        elif e["kind"] == "dos":
            dos[src] = dos.get(src, 0) + 1
        elif e["kind"] == "http":
            http[src] = http.get(src, 0) + 1
    for src, ps in ports.items():
        if len(ps) >= THRESHOLDS["port_scan"]:
            alerts.append({"src": src, "type": "port_scan", "count": len(ps)})
    for src, n in dos.items():
        if n >= THRESHOLDS["dos"]:
            alerts.append({"src": src, "type": "dos", "count": n})
    for src, n in http.items():
        if n >= THRESHOLDS["http_flood"]:
            alerts.append({"src": src, "type": "http_flood", "count": n})
    return alerts


# --- Deconstruction seat: strip fluff, keep core logic ---
FLUFF = ("please note that", "it is important to", "in order to", "basically",
         "actually", "just", "really", "very", "as you can see", "needless to say")


def strip_fluff(text):
    out = text
    for f in FLUFF:
        out = out.replace(f + " ", "").replace(f.capitalize() + " ", "")
    lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
    return {"clean": "\n".join(lines), "removed_chars": len(text) - len(out),
            "lines_kept": len(lines)}


# --- Sol-Plex seat: cognitive problem solving, secure quantum logic (labelled simulation) ---
def solve(problem):
    words = problem.lower()
    if any(k in words for k in ("scan", "network", "port", "device")):
        route = "Network Atlas"
    elif any(k in words for k in ("learn", "exam", "study", "quiz")):
        route = "Learn Hub"
    elif any(k in words for k in ("code", "run", "agent", "edit")):
        route = "Code Studio"
    elif any(k in words for k in ("news", "threat", "breach")):
        route = "Threat News Wire"
    else:
        route = "Council review"
    return {"problem": problem, "route": route,
            "steps": ["frame the problem", "strip fluff (Deconstruction)",
                      f"route to {route}", "council review", "answer with evidence"],
            "quantum_logic": "simulation label only - no quantum hardware is claimed"}
