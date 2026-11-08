"""Network Atlas: Crios map + Network Analyzer tools + Nearby radar +
TP-Link Tether router reports + Hidden Camera hunt - ONE inventory."""
import socket
from dataclasses import dataclass, field

CATEGORIES = ("Router", "Computers", "Phones & Tablets", "Entertainment",
              "Smart Home & IoT", "Servers & Storage", "Cameras", "New device")
CAMERA_VENDORS = ("hikvision", "dahua", "axis", "reolink", "wyze", "nest", "ring")
CAMERA_PORTS = {554, 8000, 8080, 37777}


@dataclass
class Device:
    name: str
    ip: str
    mac: str = ""
    vendor: str = ""
    category: str = "New device"
    ports: list = field(default_factory=list)
    trusted: bool = False

    @property
    def is_camera_like(self):
        v = self.vendor.lower()
        return self.category == "Cameras" or any(k in v for k in CAMERA_VENDORS) \
            or bool(set(self.ports) & CAMERA_PORTS)

    @property
    def suspicious(self):
        """Nearby + Peek rule: untrusted + (unknown or camera-like showing as unknown)."""
        return (not self.trusted) and (self.category == "New device" or self.is_camera_like)


def summarize(devices):
    by_cat = {}
    for d in devices:
        by_cat[d.category] = by_cat.get(d.category, 0) + 1
    return {"total": len(devices), "by_category": by_cat,
            "unknown": by_cat.get("New device", 0),
            "suspicious": sum(1 for d in devices if d.suspicious),
            "cameras": sum(1 for d in devices if d.is_camera_like)}


def network_map(devices):
    """Crios live map: star topology, router at the centre."""
    router = next((d for d in devices if d.category == "Router"), None)
    centre = router.name if router else "gateway"
    return {"centre": centre,
            "nodes": [d.name for d in devices],
            "edges": [[centre, d.name] for d in devices if d.name != centre]}


def port_scan(host, ports=(22, 80, 443, 554, 8000), timeout=0.5):
    """Real TCP connect scan against a host the caller names (their own network)."""
    open_ports = []
    for p in ports:
        s = socket.socket()
        s.settimeout(timeout)
        try:
            if s.connect_ex((host, p)) == 0:
                open_ports.append(p)
        finally:
            s.close()
    return {"host": host, "open": open_ports, "scanned": list(ports)}


def dns_lookup(name):
    try:
        return {"name": name, "ip": socket.gethostbyname(name), "ok": True}
    except socket.gaierror as e:
        return {"name": name, "ip": None, "ok": False, "error": str(e)}


def router_report(devices, prevented_this_week=0, prevented_last_week=0):
    """TP-Link Tether report seat: network security summary over the inventory."""
    s = summarize(devices)
    return {"devices": s["total"], "unknown": s["unknown"], "suspicious": s["suspicious"],
            "risks_prevented_this_week": prevented_this_week,
            "risks_prevented_last_week": prevented_last_week,
            "parental_controls": "seat present - schedules are owner-set, NetX ships none"}
