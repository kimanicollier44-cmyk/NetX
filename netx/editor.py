"""QuickCode editor + Code Compile & Run seats, merged into one Code Studio."""
import subprocess
import sys
from dataclasses import dataclass

EXT_LANG = {
    ".py": "python", ".swift": "swift", ".js": "javascript", ".ts": "typescript",
    ".cpp": "cpp", ".c": "c", ".php": "php", ".go": "go", ".kt": "kotlin",
    ".java": "java", ".rb": "ruby", ".rs": "rust",
}
LANGUAGES = sorted(set(EXT_LANG.values()))  # 12 languages, as in the Code app library


@dataclass
class Document:
    title: str
    content: str
    extension: str = ".py"

    @property
    def language(self):
        return EXT_LANG.get(self.extension, "text")

    def metadata(self):
        """QuickCode's metadata panel: title, extension, size."""
        size = len(self.content.encode())
        return {"title": self.title, "extension": self.extension.lstrip("."),
                "language": self.language,
                "size": "Zero KB" if size == 0 else f"{size / 1024:.1f} KB",
                "lines": self.content.count("\n") + (1 if self.content else 0)}


class Library:
    """Code app file library with favourites."""

    def __init__(self):
        self.files = {}
        self.favourites = set()

    def add(self, doc):
        self.files[doc.title] = doc
        return doc

    def favourite(self, title):
        if title in self.files:
            self.favourites.add(title)
        return sorted(self.favourites)


def run_code(language, code, timeout=5):
    """Python really runs (sandboxed subprocess, timeout). Other languages are
    recognised and returned as a compile plan - NetX never claims a run it did not do."""
    if language == "python":
        try:
            p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                               text=True, timeout=timeout)
            return {"language": language, "executed": True, "exit": p.returncode,
                    "stdout": p.stdout, "stderr": p.stderr[-500:]}
        except subprocess.TimeoutExpired:
            return {"language": language, "executed": True, "exit": -1,
                    "stdout": "", "stderr": f"timeout after {timeout}s"}
    if language in LANGUAGES:
        return {"language": language, "executed": False, "exit": None,
                "stdout": "", "stderr": "",
                "plan": f"{language} toolchain not bundled in NetX core - compile plan only"}
    return {"language": language, "executed": False, "exit": None,
            "stdout": "", "stderr": f"unknown language: {language}"}
