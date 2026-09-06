"""Shared helpers for the skillary tooling.

Skills live in sibling repos, not in this one. Every script here discovers the
12 `skills-*` repos as siblings of the hub checkout unless told otherwise.

The frontmatter reader deliberately does NOT round-trip through a YAML dumper.
All 315 descriptions are written as `>-` block scalars; a naive dump reflows
every one of them and turns an otherwise small content diff into 315 unreviewable
whole-file diffs. Writes are surgical text splices instead.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CATEGORIES = [
    "developer",
    "marketing",
    "gamedev",
    "business",
    "design",
    "education",
    "agents",
    "personal",
    "writing",
    "sales",
    "finance",
    "legal",
]

# Claude truncates the description in the skill listing at roughly this length.
# Anything past it is invisible to skill selection, so the trigger clause has to
# land inside it.
DESCRIPTION_LISTING_LIMIT = 250

# Hard ceiling from the Agent Skills spec.
DESCRIPTION_SPEC_LIMIT = 1024

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Generated trigger sentences carrying no routing signal - they fire on the
# skill's own name, which the model already sees.
BOILERPLATE_TAIL_RES = [
    re.compile(
        r"Use when the user asks about .{1,80}?, needs this workflow, "
        r"or requests related deliverables\.?",
        re.I,
    ),
    re.compile(
        r"Use when working on .{1,80}?, generating related artifacts, "
        r"or analyzing domain requirements\.?",
        re.I,
    ),
]

STUB_MARKERS = [
    "could not be fetched",
    "Source-linked stub",
    "Import placeholder",
]

# The software-engineering QA block that was stamped across every domain.
WRONG_DOMAIN_MARKERS = [
    "Code compiles cleanly and passes all automated tests",
    "unhandled promise rejections",
    "NEVER introduce breaking API changes",
]

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.S)


@dataclass
class Skill:
    """One skill folder on disk."""

    repo: str
    path: Path
    name: str | None
    description: str
    body: str
    raw: str
    frontmatter: str
    deprecated: bool = False

    @property
    def slug(self) -> str:
        return self.path.name

    @property
    def rel(self) -> str:
        return f"{self.repo}/skills/{self.slug}"


@dataclass
class Finding:
    skill: str
    code: str
    message: str
    severity: str = "error"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, skill: str, code: str, message: str, severity: str = "error") -> None:
        self.findings.append(Finding(skill, code, message, severity))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


def repo_root(hub: Path | None = None) -> Path:
    """Directory containing the hub checkout and its 12 sibling skill repos."""
    hub = hub or Path(__file__).resolve().parent.parent
    return hub.parent


def get_version(hub: Path | None = None) -> str:
    """Read version from canonical VERSION file."""
    hub = hub or Path(__file__).resolve().parent.parent
    vfile = hub / "VERSION"
    if vfile.is_file():
        return vfile.read_text(encoding="utf-8").strip()
    return "3.0.0"


def repo_paths(root: Path | None = None) -> list[Path]:
    root = root or repo_root()
    found = []
    for category in CATEGORIES:
        path = root / f"skills-{category}"
        if (path / "skills").is_dir():
            found.append(path)
    return found


def parse_description(frontmatter: str) -> str:
    """Pull `description` out of frontmatter, folding block scalars to one line.

    Handles the `>-` / `>` / `|` block styles used across the library as well as
    plain inline values.
    """
    match = re.search(r"^description:[ \t]*(.*)$", frontmatter, re.M)
    if not match:
        return ""
    first = match.group(1).strip()
    if first and first not in {">-", ">", "|", "|-"}:
        return first.strip("\"'")

    # Block scalar: take the indented continuation lines that follow.
    lines = frontmatter[match.end() :].splitlines()
    collected = []
    for line in lines:
        if line.strip() and not line.startswith((" ", "\t")):
            break
        collected.append(line.strip())
    return " ".join(part for part in collected if part)


def load_skill(repo: str, path: Path) -> Skill:
    raw = (path / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return Skill(repo, path, None, "", raw, raw, "", False)
    frontmatter, body = match.group(1), match.group(2)
    name_match = re.search(r"^name:[ \t]*(.+)$", frontmatter, re.M)
    name = name_match.group(1).strip().strip("\"'") if name_match else None
    dep_match = re.search(r"^deprecated:[ \t]*(true|yes|1)", frontmatter, re.M | re.I)
    deprecated = bool(dep_match)
    return Skill(repo, path, name, parse_description(frontmatter), body, raw, frontmatter, deprecated)


def iter_skills(root: Path | None = None, include_deprecated: bool = False):
    """Yield every Skill across the sibling repos, sorted by repo then slug."""
    for repo_path in repo_paths(root):
        skills_dir = repo_path / "skills"
        for path in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            if not (path / "SKILL.md").is_file():
                continue
            skill = load_skill(repo_path.name, path)
            if skill.deprecated and not include_deprecated:
                continue
            yield skill


def strip_boilerplate_tail(description: str) -> str:
    """Remove a generated trigger sentence, returning the description without it."""
    out = description
    for pattern in BOILERPLATE_TAIL_RES:
        out = pattern.sub("", out)
    return re.sub(r"\s+", " ", out).strip()
