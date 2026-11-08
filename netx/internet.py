"""Internet seat - Fing's Internet tab, merged into Network Atlas:
ISP profile (public IP, hostname/PTR, location, timezone), trend cards,
user rating and the 24/7 monitoring seat for the owner's OWN network.
PRIVACY RULE: a real owner's profile lives in private/ (gitignored) and is
loaded at runtime - real IPs / BSSIDs are never written into this repo."""
import ipaddress
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class InternetProfile:
    isp: str
    public_ip: str
    hostname: str = ""          # Fing shows the IP itself when no PTR exists
    location: str = ""
    timezone: str = ""
    bssid: str = ""             # the Wi-Fi network this profile belongs to
    trends: dict = field(default_factory=dict)   # e.g. {"performance": "Declining fast"}
    user_rating: int = 0        # 0-5 hearts, Fing style

    @property
    def has_ptr(self):
        return bool(self.hostname) and self.hostname != self.public_ip

    @property
    def is_public(self):
        try:
            return ipaddress.ip_address(self.public_ip).is_global
        except ValueError:
            return False


# Sample uses TEST-NET-3 (203.0.113.0/24, documentation range) - never a real address.
SAMPLE = InternetProfile(
    isp="Example ISP", public_ip="203.0.113.10", hostname="203.0.113.10",
    location="Example City", timezone="America/Los_Angeles",
    trends={"performance": "Declining fast", "user_rating": "Stable trend"},
    user_rating=0)


def profile_check(p):
    return {"isp": p.isp, "public_ip": p.public_ip, "is_public": p.is_public,
            "ptr_published": p.has_ptr,
            "ptr_note": "hostname present" if p.has_ptr else "no PTR - hostname falls back to the IP itself",
            "location": p.location, "timezone": p.timezone,
            "trends": p.trends, "user_rating": p.user_rating,
            "monitoring_24_7": "seat present - Fing-style monitoring runs on the owner's own network only"}


def load_profile(private_dir=None):
    """Loads the owner's private profile if it exists, else the sample.
    Returns (profile, source) where source is 'private' or 'sample'."""
    base = Path(private_dir) if private_dir else Path(__file__).parent.parent / "private"
    f = base / "home_internet.json"
    if f.exists():
        d = json.loads(f.read_text())
        return InternetProfile(**d), "private"
    return SAMPLE, "sample"
