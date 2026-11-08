"""Google Maps seat: the Apify guide "How to use the Google Maps API in
Python" (blog.apify.com, May 7 2025), merged from Darion's screen recording
of the article. The guide's two functions, kept with their names:

  get_lati_longi(api_key, address) - Geocoding API: address -> (lat, lng)
  get_dist_dur(api_key, start, end) - Distance Matrix: driving distance + time

NetX differences, stated honestly: the guide uses the `requests` library;
NetX is zero-dependency, so live calls use urllib from the stdlib. Live
calls need the owner's GOOGLE_MAPS_API_KEY (environment only, never in the
repo - HOLD gate). Without a key the seat works fully offline: it parses
API-shaped payloads the caller supplies and demos on the article's own
published Prague examples, outputs and all."""
import json
import os
import urllib.parse
import urllib.request

GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"
DISTANCE_ENDPOINT = "https://maps.googleapis.com/maps/api/distancematrix/json"
STATICMAP_ENDPOINT = "https://maps.googleapis.com/maps/api/staticmap"

# The article's own published examples (Prague), shaped like the real API
# responses - the offline ground truth the parsers are tested against.
ARTICLE_ADDRESS = "Vodickova 704/36, 11000 Prague 1, Czech Republic"
ARTICLE_LAT = 50.08138847866026
ARTICLE_LNG = 14.425403029872987
GEOCODE_SAMPLE = {"status": "OK", "results": [
    {"formatted_address": ARTICLE_ADDRESS,
     "geometry": {"location": {"lat": ARTICLE_LAT, "lng": ARTICLE_LNG}}}]}

ARTICLE_START = "Palace Lucerna, Stepanska 61, 116 02 Nove Mesto, Czech Republic"
ARTICLE_END = "Project FOX, Rohacova 705/3, 130 00 Praha 3-Zizkov, Czech Republic"
DISTANCE_SAMPLE = {"status": "OK", "rows": [{"elements": [
    {"status": "OK",
     "distance": {"text": "6.7 km", "value": 6700},
     "duration": {"text": "23 mins", "value": 1380}}]}]}


def parse_geocode(payload):
    """Geocoding payload -> (lat, lng), or None when the API found nothing."""
    if not payload or payload.get("status") != "OK" or not payload.get("results"):
        return None
    loc = payload["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


def parse_distance(payload):
    """Distance Matrix payload -> distance/duration dict, or None."""
    if not payload or payload.get("status") != "OK" or not payload.get("rows"):
        return None
    el = payload["rows"][0]["elements"][0]
    if el.get("status") != "OK":
        return None
    return {"distance_text": el["distance"]["text"],
            "distance_m": el["distance"]["value"],
            "duration_text": el["duration"]["text"],
            "duration_s": el["duration"]["value"]}


def geocode_url(address, api_key):
    q = urllib.parse.urlencode({"address": address, "key": api_key})
    return f"{GEOCODE_ENDPOINT}?{q}"


def distance_url(start, end, api_key, mode="driving"):
    q = urllib.parse.urlencode({"origins": start, "destinations": end,
                                "mode": mode, "key": api_key})
    return f"{DISTANCE_ENDPOINT}?{q}"


def static_map_url(lat, lng, api_key, zoom=15, size="600x400"):
    """The article's next step (Maps Static API): builds the URL only -
    nothing is fetched, rendered=False by construction."""
    q = urllib.parse.urlencode({"center": f"{lat},{lng}", "zoom": zoom,
                                "size": size, "key": api_key})
    return {"url": f"{STATICMAP_ENDPOINT}?{q}", "fetched": False}


def _key(api_key):
    return api_key or os.environ.get("GOOGLE_MAPS_API_KEY")


def _fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:  # live, key-gated
        return json.loads(r.read().decode("utf-8"))


def get_lati_longi(address, api_key=None):
    """The guide's geocoder. No key -> HOLD (gate: geo-api-key); the seat
    never invents coordinates. With the owner's key -> live Geocoding call."""
    key = _key(api_key)
    if not key:
        return {"status": "HOLD", "gate": "geo-api-key",
                "needs": "GOOGLE_MAPS_API_KEY in the environment",
                "offline_demo": parse_geocode(GEOCODE_SAMPLE)}
    return {"status": "OK", "coordinates": parse_geocode(_fetch(geocode_url(address, key)))}


def get_dist_dur(start, end, api_key=None):
    """The guide's distance/duration lookup (driving). Same key rule."""
    key = _key(api_key)
    if not key:
        return {"status": "HOLD", "gate": "geo-api-key",
                "needs": "GOOGLE_MAPS_API_KEY in the environment",
                "offline_demo": parse_distance(DISTANCE_SAMPLE)}
    return {"status": "OK", **parse_distance(_fetch(distance_url(start, end, key)))}


def demo_pairs():
    """Offline demo on the article's published examples - exact outputs."""
    lat, lng = parse_geocode(GEOCODE_SAMPLE)
    d = parse_distance(DISTANCE_SAMPLE)
    return {"address": ARTICLE_ADDRESS, "latitude": lat, "longitude": lng,
            "from": ARTICLE_START, "to": ARTICLE_END,
            "distance": d["distance_text"], "time_take": d["duration_text"],
            "static_map": static_map_url(lat, lng, "KEY")["fetched"]}
