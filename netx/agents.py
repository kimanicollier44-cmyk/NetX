"""Kilo seat: AI coding-agent sessions you steer from your pocket."""
from dataclasses import dataclass, field

STATUSES = ("Needs input", "Working", "Scheduled", "Idle")


@dataclass
class Session:
    title: str
    status: str = "Idle"
    run_on: str = "MacBook Pro"
    notes: list = field(default_factory=list)

    def __post_init__(self):
        if self.status not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}")


class AgentFleet:
    """Mirrors the Kilo live board: 0 Needs input, 2 Working, 0 Scheduled, 1 Idle."""

    def __init__(self):
        self.sessions = []

    def new_task(self, title, run_on="MacBook Pro"):
        s = Session(title=title, status="Working", run_on=run_on)
        self.sessions.append(s)
        return s

    def steer(self, title, status, note=""):
        for s in self.sessions:
            if s.title == title:
                s.status = status
                if note:
                    s.notes.append(note)
                return s
        raise KeyError(title)

    def board(self):
        out = {st: 0 for st in STATUSES}
        for s in self.sessions:
            out[s.status] += 1
        return out
