"""Cellular Tower seat: all towers 2G-5G on a map + nearest-tower finder.
Tower data is caller-supplied / bundled sample data - NetX does not scrape a live tower DB."""
import math
from dataclasses import dataclass


@dataclass
class Tower:
    name: str
    lat: float
    lon: float
    generation: str  # 2G / 3G / 4G / 5G
    carrier: str = ""


SAMPLE_TOWERS = [
    Tower("Porter Ranch North", 34.292, -118.559, "5G", "T-Mobile"),
    Tower("Porter Ranch South", 34.278, -118.545, "4G", "AT&T"),
    Tower("Northridge Ridge", 34.238, -118.530, "5G", "Verizon"),
    Tower("Chatsworth Peak", 34.257, -118.600, "4G", "T-Mobile"),
    Tower("Granada Hills", 34.265, -118.495, "3G", "AT&T"),
    Tower("Old Site Legacy", 34.200, -118.500, "2G", "Verizon"),
]


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def nearest(lat, lon, towers=SAMPLE_TOWERS, generation=None, limit=3):
    rows = []
    for t in towers:
        if generation and t.generation != generation:
            continue
        rows.append({"name": t.name, "generation": t.generation, "carrier": t.carrier,
                     "distance_km": round(haversine_km(lat, lon, t.lat, t.lon), 3)})
    rows.sort(key=lambda r: r["distance_km"])
    return rows[:limit]


def generations(towers=SAMPLE_TOWERS):
    return sorted({t.generation for t in towers})
