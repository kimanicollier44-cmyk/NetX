"""LLM-X-NetLab seat (credkellar/LLM-X-NetLab, merged in full):
RAG tutor over the 21-entry networking KB, subnet / topology / layer / device
engines, IP hopper-tracker-mapper START-MIDDLE-END + beyond-END walker,
Google Earth KML export. Live socket tools live in network.py (one copy only)."""
import ipaddress
import math
import re
from collections import Counter

KB = [
    ("subnet", "A subnet divides one network into smaller networks using a mask like /24; hosts = 2^(32-prefix) - 2."),
    ("osi model", "OSI has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application."),
    ("tcp ip model", "TCP/IP has 4 layers: Link, Internet, Transport, Application - the practical stack the internet runs on."),
    ("router", "A router forwards packets between networks using routing tables and the destination IP."),
    ("switch", "A switch forwards frames inside one LAN using a MAC address table."),
    ("gateway", "The gateway is the LAN's exit router - for 192.168.1.0/24 it is usually 192.168.1.1."),
    ("dns", "DNS translates names to IPs; a recursive resolver asks root, TLD, then authoritative servers."),
    ("dhcp", "DHCP leases IP, mask, gateway and DNS to devices joining a network (DORA: Discover Offer Request Ack)."),
    ("nat", "NAT rewrites private IPs to one public IP so a whole LAN shares a single internet address."),
    ("ping", "Ping uses ICMP echo to test reachability and round-trip time."),
    ("traceroute", "Traceroute raises TTL hop by hop to reveal the path packets take across routers."),
    ("arp", "ARP maps an IP to a MAC address inside the local network."),
    ("mac address", "A MAC is the hardware address of a network interface, used inside one LAN segment."),
    ("ipv4", "IPv4 is 32-bit, written as four octets; private ranges include 10/8, 172.16/12, 192.168/16."),
    ("ipv6", "IPv6 is 128-bit, written in hex groups; it removes the need for NAT in most designs."),
    ("tcp", "TCP is reliable, ordered, connection-oriented - handshake SYN, SYN-ACK, ACK."),
    ("udp", "UDP is fast and connectionless with no delivery guarantee - used for DNS, VoIP, streaming."),
    ("http", "HTTP is the application protocol of the web; HTTPS adds TLS encryption."),
    ("topology", "Topologies: star, mesh, bus, ring. A star's centre is a single point of failure."),
    ("firewall", "A firewall filters traffic by rules on IP, port and protocol - default-deny is safest."),
    ("bandwidth latency", "Bandwidth is capacity (bits per second); latency is delay (milliseconds). They are different problems."),
]

LAYERS = {"http": ("Application", 7), "dns": ("Application", 7), "tcp": ("Transport", 4),
          "udp": ("Transport", 4), "ip": ("Network", 3), "arp": ("Network", 3),
          "ethernet": ("Data Link", 2), "wifi": ("Physical", 1)}


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def tutor(question, top=2):
    """TF-IDF-style RAG over the KB: ranks entries, returns the best matches verbatim."""
    q = Counter(_tokens(question))
    scored = []
    for title, body in KB:
        doc = Counter(_tokens(title + " " + body))
        score = sum(min(q[t], doc[t]) * (1 + math.log(1 + doc[t])) for t in q if t in doc)
        if score:
            scored.append((score, title, body))
    scored.sort(reverse=True)
    return [{"title": t, "answer": b, "score": round(s, 3)} for s, t, b in scored[:top]]


def subnet_calc(cidr):
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = max(net.num_addresses - 2, 0) if net.prefixlen < 31 else net.num_addresses
    return {"network": str(net.network_address), "broadcast": str(net.broadcast_address),
            "mask": str(net.netmask), "prefix": net.prefixlen,
            "addresses": net.num_addresses, "usable_hosts": hosts,
            "first": str(net.network_address + 1) if hosts else None,
            "last": str(net.broadcast_address - 1) if hosts else None}


def layer_of(protocol):
    return LAYERS.get(protocol.lower(), ("Unknown", 0))


def topology_spof(links):
    """links: list of (a, b). A node is a SPOF if removing it disconnects the graph."""
    nodes = {n for pair in links for n in pair}
    def connected(skip=None):
        adj = {n: set() for n in nodes if n != skip}
        for a, b in links:
            if skip in (a, b):
                continue
            adj[a].add(b); adj[b].add(a)
        seen, stack = set(), [next(iter(adj))] if adj else []
        while stack:
            n = stack.pop()
            if n not in seen:
                seen.add(n); stack.extend(adj[n] - seen)
        return len(seen) == len(adj)
    return sorted(n for n in nodes if not connected(skip=n))


def track(hops):
    """IP tracker over a caller-supplied hop list: START / MIDDLE / END labels."""
    if not hops:
        return []
    out = []
    for i, h in enumerate(hops):
        role = "START" if i == 0 else "END" if i == len(hops) - 1 else "MIDDLE"
        out.append({"hop": i + 1, "ip": h, "role": role})
    return out


def beyond_end(hops, extra):
    """Past END: keep connecting endpoint to endpoint until one won't answer.
    extra: list of (name, connects_bool) supplied by the caller - NetX labels, never fakes."""
    out = track(hops)
    for name, ok in extra:
        out.append({"hop": len(out) + 1, "ip": name,
                    "role": "CONNECTS" if ok else "CAN'T CONNECT"})
        if not ok:
            break
    return out


def kml_export(name, lon, lat):
    """Google Earth seat: KML for caller-supplied coordinates only - no geolocation."""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark>'
            f'<name>{name}</name><Point><coordinates>{lon},{lat},0</coordinates>'
            f'</Point></Placemark></kml>')
