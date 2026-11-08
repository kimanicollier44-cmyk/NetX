"""Threat News Wire: both cyber-news apps merged into ONE deduped feed.
Ranking from News & Reports (Top/Latest/Most Discussed); trending, topics and
bookmarks from CyberNews. Bundled sample feed - live fetching is a seat, not claimed."""
from dataclasses import dataclass


@dataclass
class Article:
    title: str
    source: str
    topic: str
    hours_ago: int
    comments: int = 0
    sources_count: int = 1


FEED = [
    Article("PHP2Shell plus Fragnesia: a dangerous new route from web to shell",
            "CSO Online", "security", 48, 120, 10),
    Article("Security firm disables vulnerable Popcorn Time updater",
            "SC Magazine", "security", 144, 40, 3),
    Article("Windows 10 Version 1903 and later may 'forget' your USB printer after this simple operation",
            "Hot Hardware", "threats", 1, 5, 1),
    Article("Encryption utility firm accused of bundling malware functions in product",
            "Cyware", "malware", 1, 8, 1),
    Article("GitLab acquires Peach Tech and Fuzzit to beef up its DevOps security testing tools",
            "Silicon Angle", "security", 2, 15, 1),
    Article("Unstoppable Domains launches blockchain-based decentralized blogging service",
            "Silicon Angle", "web3", 5, 22, 1),
    # Deliberate near-duplicate (same story, second app) - the dedupe must collapse it:
    Article("GitLab acquires Peach Tech and Fuzzit to beef up DevOps security testing tools",
            "CyberNews wire", "security", 3, 2, 1),
]


def _key(title):
    return " ".join(title.lower().replace("its ", "").split())


def deduped(feed=FEED):
    seen, out = {}, []
    for a in feed:
        k = _key(a.title)
        if k in seen:
            seen[k].sources_count += 1
            continue
        seen[k] = a
        out.append(a)
    return out


def rank(mode="top", feed=None):
    arts = deduped(feed) if feed is not None else deduped()
    if mode == "latest":
        return sorted(arts, key=lambda a: a.hours_ago)
    if mode == "discussed":
        return sorted(arts, key=lambda a: -a.comments)
    return sorted(arts, key=lambda a: -(a.comments + 10 * a.sources_count))  # top


def topics(feed=None):
    return sorted({a.topic for a in (deduped(feed) if feed is not None else deduped())})


class Bookmarks:
    def __init__(self):
        self.saved = []

    def toggle(self, title):
        if title in self.saved:
            self.saved.remove(title)
        else:
            self.saved.append(title)
        return list(self.saved)
