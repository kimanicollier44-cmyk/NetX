"""HOLD gates - actions NetX plans and labels, but never performs autonomously."""

HOLD_GATES = [
    "live-exploitation: no exploiting any system, ever - labs and learning only",
    "foreign-network-scan: port scans only on networks the owner names as theirs",
    "untrusted-code: code runs only as the owner's own snippets in the timed sandbox",
    "agent-autonomy: agents never act without a human steering the session",
    "router-changes: Tether seat reports only - no router settings are changed",
    "vpn-traffic: Shield checks VPN presence - it does not route or log traffic",
    "tower-location: tower distances use caller-supplied coordinates - no tracking",
    "camera-accusation: a camera-like flag is a heuristic, never proof of a spy camera",
    "news-publish: the wire ranks bundled/sample items - no live story is published as fact",
    "exam-integrity: quiz answers stay local - no fetching live exam content",
    "geo-lookup: no third-party geolocation of IPs the owner does not control",
    "push-publish: NetX ships locally until Darion names a repo and says push",
    "home-profile-privacy: the owner's real ISP / public-IP / BSSID profile lives in private/ (gitignored) - it is never committed, pushed or published",
    "sandbox-never-executes: the sandbox-suite seat triages file metadata only - samples are never opened, run or detonated",
    "voice-no-identification: the Ppls seat matches abstract vectors the caller supplies - no audio capture, no identifying real people",
    "geo-api-key: live Google Maps calls need the owner's GOOGLE_MAPS_API_KEY (environment only, never committed) - until then the geo seat parses supplied payloads and demos on the article's published examples",
]


def hold_demo():
    return {"held": len(HOLD_GATES), "gates": HOLD_GATES, "exit_code": 2}
