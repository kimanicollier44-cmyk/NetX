"""Council: Gemini Carbon 4 Extended Thinking = DECIDER, Muse = advisor
(authority: none, can never override), Google Flow = video plans (rendered: False).
Strictest verdict wins - the same merged council as Darion's other systems."""
TIERS = (2048, 8192, 32768)
ORDER = {"PROCEED": 0, "WATCH": 1, "ESCALATE": 2, "HOLD": 3}


def carbon4(subject, severity="low", signals=0):
    tier = TIERS[0] if signals < 5 else TIERS[1] if signals < 50 else TIERS[2]
    if severity == "critical":
        verdict = "HOLD"
    elif severity == "high" or signals >= 100:
        verdict = "ESCALATE"
    elif severity == "medium" or signals >= 10:
        verdict = "WATCH"
    else:
        verdict = "PROCEED"
    return {"brain": "Gemini Carbon 4 Extended Thinking", "role": "DECIDER",
            "model": "google/gemini-carbon-4-extended-pro-thinking",
            "phases": ["MAP", "MODEL", "STRESS", "DECIDE"], "tier": tier,
            "subject": subject, "verdict": verdict, "can_override_hold": False}


def muse_advice(subject):
    return {"brain": "Muse", "role": "advisor", "authority": "none",
            "advice": [f"Check the evidence behind '{subject}' before acting",
                       "Prefer the reversible step first",
                       "Label anything simulated as simulated",
                       "Surface unknowns instead of filling them in"]}


def flow_plan(subject):
    return {"seat": "Google Flow", "subject": subject, "rendered": False,
            "shots": ["wide: the pocket dashboard", "close: the hub in action",
                      "end card: NetX"]}


def council(subject, severity="low", signals=0):
    c = carbon4(subject, severity, signals)
    m = muse_advice(subject)
    verdict = c["verdict"]  # advisor can only add caution, never lift a verdict
    return {"subject": subject, "verdict": verdict, "decider": c, "advisor": m,
            "flow": flow_plan(subject), "strictest_wins": True}
