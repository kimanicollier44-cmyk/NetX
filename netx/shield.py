"""Shield: Norton 360 seat - Smart Scan, malware checklist, VPN seat, Protection Report.
Checks run over facts the owner supplies about their own device; no fake 'protected' claims."""

CHECKS = [
    ("os_updated", "Operating system is up to date"),
    ("passcode_set", "Device passcode / biometrics on"),
    ("unknown_apps", "No sideloaded or unknown apps present"),
    ("wifi_encrypted", "Joined Wi-Fi uses WPA2/WPA3"),
    ("vpn_available", "VPN seat configured"),
    ("backups_on", "Backups enabled"),
]


def smart_scan(facts):
    """facts: dict of CHECKS keys -> bool. Returns score + the exact failed items."""
    failed = [label for key, label in CHECKS if not facts.get(key, False)]
    passed = len(CHECKS) - len(failed)
    return {"passed": passed, "total": len(CHECKS),
            "score_pct": round(100 * passed / len(CHECKS)),
            "failed": failed,
            "verdict": "protected" if not failed else "issues found"}


def protection_report(scans):
    """90-day style roll-up over past smart_scan results."""
    if not scans:
        return {"scans": 0, "avg_score_pct": None}
    avg = round(sum(s["score_pct"] for s in scans) / len(scans))
    return {"scans": len(scans), "avg_score_pct": avg,
            "clean": sum(1 for s in scans if not s["failed"])}
