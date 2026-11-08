"""Learn Hub: 3 tracks, no duplicates.
Track A curriculum (Kali structure + HackerX bite-size modules),
Track B interactive coding (Mimo), Track C exams (Pocket Prep catalog + Security+ SY0-701 deep track)."""

KALI_COURSES = [
    {"title": "Basics", "topics": 18, "level": "Beginner"},
    {"title": "Intermediate Networking & Tools", "topics": 19, "level": "Intermediate"},
    {"title": "Advanced Exploitation Concepts (lab only)", "topics": 20, "level": "Advanced"},
    {"title": "Expert Lab Practice (own lab only)", "topics": 68, "level": "Expert"},
]
KALI_TOOLS = ["Nmap", "Wireshark", "Metasploit", "Burp Suite", "John the Ripper",
              "Hashcat", "Hydra", "Aircrack-ng", "SQLmap", "Nikto", "Maltego", "Gobuster"]
HACKERX_MODULES = ["Footprinting", "WiFi Hacking - WEP Cracking (history/lab)",
                   "Wifi Encryptions", "Using External Wireless Adapter",
                   "Enabling Monitor Mode", "Packet Sniffing"]

MIMO_LESSONS = [
    {"id": "py-print", "language": "python", "title": "Say hello",
     "prompt": "Print exactly: Hello, NetX", "expected": "Hello, NetX"},
    {"id": "py-math", "language": "python", "title": "Add two numbers",
     "prompt": "Print the sum of 19 and 23", "expected": "42"},
    {"id": "py-loop", "language": "python", "title": "Count to three",
     "prompt": "Print 1, 2, 3 each on its own line", "expected": "1\n2\n3"},
]

CERTS = ["AWS Certified Cloud Practitioner", "Cisco CCNA", "Cisco CCNP Enterprise",
         "CompTIA A+", "CompTIA SecurityX", "CompTIA Cloud+", "CompTIA CySA+",
         "CompTIA Tech+", "CompTIA Linux+", "CompTIA Network+", "CompTIA PenTest+",
         "CompTIA Security+", "CompTIA Project+", "CompTIA Data+", "CompTIA Server+",
         "CISSP", "CISM", "CEH", "OSCP", "CCSP", "CISA", "GSEC", "GCIH",
         "Microsoft AZ-900", "Microsoft SC-900", "Google Cybersecurity Certificate",
         "ITIL 4 Foundation"]  # 27-cert catalog, Pocket Prep style

SECPLUS_DOMAINS = ["General Security Concepts", "Threats, Vulnerabilities & Mitigations",
                   "Security Architecture", "Security Operations", "Security Program Management & Oversight"]

QUESTIONS = [
    {"domain": SECPLUS_DOMAINS[0], "q": "Which control type is a firewall rule?",
     "choices": ["Detective", "Technical", "Physical", "Managerial"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[1], "q": "What does a zero-day mean?",
     "choices": ["A patched flaw", "A flaw exploited before a fix exists", "A slow scan", "A backup type"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[2], "q": "Zero Trust assumes what?",
     "choices": ["The LAN is safe", "Never trust, always verify", "VPNs are enough", "Passwords never expire"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[3], "q": "First step of incident response?",
     "choices": ["Eradication", "Preparation", "Lessons learned", "Recovery"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[4], "q": "What is risk transference?",
     "choices": ["Deleting data", "Buying insurance / outsourcing the risk", "Ignoring the risk", "Patching"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[0], "q": "MFA requires factors from how many different categories at minimum?",
     "choices": ["One", "Two", "Four", "None"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[1], "q": "Phishing over voice calls is called?",
     "choices": ["Smishing", "Vishing", "Whaling", "Tailgating"], "answer": 1},
    {"domain": SECPLUS_DOMAINS[3], "q": "A SIEM mainly helps with?",
     "choices": ["Printing", "Log correlation and alerting", "Backups", "Cabling"], "answer": 1},
]


def check_lesson(lesson_id, code):
    from .editor import run_code
    lesson = next((l for l in MIMO_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return {"ok": False, "error": f"unknown lesson {lesson_id}"}
    r = run_code(lesson["language"], code)
    got = r["stdout"].strip()
    return {"ok": r["executed"] and got == lesson["expected"], "got": got,
            "expected": lesson["expected"]}


def quiz(answers, questions=QUESTIONS):
    """answers: list of chosen indexes. Quick-10 / full-bank scoring, by domain."""
    per_domain = {}
    correct = 0
    for q, a in zip(questions, answers):
        ok = a == q["answer"]
        correct += ok
        d = per_domain.setdefault(q["domain"], {"correct": 0, "total": 0})
        d["total"] += 1
        d["correct"] += ok
    total = min(len(answers), len(questions))
    return {"correct": correct, "total": total,
            "pct": round(100 * correct / total) if total else 0, "by_domain": per_domain}


def question_of_day(day_ordinal):
    return QUESTIONS[day_ordinal % len(QUESTIONS)]
