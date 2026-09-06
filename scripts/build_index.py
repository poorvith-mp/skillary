"""Regenerate the hub's skill index from the 12 sibling repos.

The index is 315 hand-maintained rows and has drifted before. Making it
generated output removes that whole class of bug: the README stops being
something you edit and becomes something you rebuild.

Only the region between the sentinels is touched, so hand-written prose above
and below is safe.

Usage:
    python scripts/build_index.py --check    # exit 1 + diff on drift (CI)
    python scripts/build_index.py --write    # rewrite the sentinel region
    python scripts/build_index.py --router   # emit skill-router's index file
"""

from __future__ import annotations

import argparse
import difflib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from skillary import iter_skills, repo_root  # noqa: E402

# Two regions, because the category table belongs near the top of the page as a
# table of contents while the 315-row index belongs at the bottom. Generating
# one contiguous block would force them together and make the README worse to
# read for the sake of the generator.
REGIONS = {
    "REPOS": ("<!-- BEGIN:REPOS -->", "<!-- END:REPOS -->"),
    "INDEX": ("<!-- BEGIN:INDEX -->", "<!-- END:INDEX -->"),
}

OWNER = "poorvith-mp"

# Display names for the 12 repos, in the order the index presents them
# (largest first, as the current README does).
LABELS = {
    "skills-developer": "Developer",
    "skills-marketing": "Marketing",
    "skills-gamedev": "Game Dev",
    "skills-business": "Business",
    "skills-design": "Design",
    "skills-education": "Education",
    "skills-agents": "Agents",
    "skills-personal": "Personal",
    "skills-writing": "Writing",
    "skills-sales": "Sales & Support",
    "skills-finance": "Finance",
    "skills-legal": "Legal",
}

# Titles are `slug.replace('-', ' ').title()` with these fixups. Derived by
# diffing the generator against all 315 rows of the existing hand-written index
# - do NOT derive titles from the body H1, which only matches 226 of 315.
ACRONYMS = {
    "Ai": "AI", "Api": "API", "Cd": "CD", "Ci": "CI", "Cms": "CMS",
    "Crm": "CRM", "Ecommerce": "eCommerce", "Esg": "ESG", "Finops": "FinOps",
    "Graphql": "GraphQL", "Iac": "IaC", "Ios": "iOS", "It": "IT", "Mcp": "MCP",
    "N8N": "N8n", "Okr": "OKR", "Pr": "PR", "Qa": "QA", "Seo": "SEO",
    "Sop": "SOP", "Sre": "SRE", "Ui": "UI", "Ux": "UX", "Zk": "ZK",
}


def title_for(slug: str) -> str:
    words = slug.replace("-", " ").title().split()
    return " ".join(ACRONYMS.get(word, word) for word in words)


def collect() -> dict[str, list]:
    grouped: dict[str, list] = {repo: [] for repo in LABELS}
    for skill in iter_skills():
        grouped.setdefault(skill.repo, []).append(skill)
    return {repo: sorted(items, key=lambda s: s.slug) for repo, items in grouped.items() if items}


def render_repos(grouped: dict[str, list]) -> str:
    total = sum(len(v) for v in grouped.values())
    order = [r for r in LABELS if r in grouped]
    begin, end = REGIONS["REPOS"]
    out = [begin, "", "| Category | Repository | Skills |", "|----------|------------|--------|"]
    for repo in order:
        out.append(f"| {LABELS[repo]} | [{repo}](https://github.com/{OWNER}/{repo}) | {len(grouped[repo])} |")
    out += ["", f"**Total: {total} skills across {len(order)} repositories.**", "", end]
    return "\n".join(out)


def render_index(grouped: dict[str, list]) -> str:
    order = [r for r in LABELS if r in grouped]
    begin, end = REGIONS["INDEX"]
    out = [begin, ""]
    for repo in order:
        items = grouped[repo]
        out += [f"### {LABELS[repo]} — [{repo}](https://github.com/{OWNER}/{repo}) ({len(items)} skills)",
                "", "| Skill ID | Title |", "|----------|-------|"]
        out += [f"| `{s.slug}` | {title_for(s.slug)} |" for s in items]
        out.append("")
    out.append(end)
    return "\n".join(out)


def render_router(grouped: dict[str, list]) -> str:
    total = sum(len(v) for v in grouped.values())
    out = [
        "# Skill Index",
        "",
        "GENERATED FILE - do not edit by hand. Rebuild with "
        "`python scripts/build_index.py --router` in the hub repo.",
        "",
        f"{total} skills across {len(grouped)} category repos.",
        "",
        "Format: `skill-id` — description — `repo`",
        "",
    ]
    for repo, items in grouped.items():
        out += [f"## {repo}", ""]
        for skill in items:
            desc = " ".join(skill.description.split())
            if len(desc) > 200:
                desc = desc[:197].rsplit(" ", 1)[0] + "..."
            out.append(f"- `{skill.slug}` — {desc}")
        out.append("")
    return "\n".join(out)


# Generated files are written with the platform's native line ending, which is
# what git checks out under `* text=auto`. Pinning either LF or CRLF here leaves
# the file permanently reading as modified on the other platform.
def write_native(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def emit_json(grouped: dict[str, list], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for repo, items in grouped.items():
        for s in items:
            records.append({
                "slug": s.slug,
                "title": title_for(s.slug),
                "category": LABELS.get(repo, repo),
                "repo": repo,
                "group": s.group or "",
                "description": s.description.strip(),
                "url": f"https://github.com/{OWNER}/{repo}/tree/main/skills/{s.slug}",
            })
    out_path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def emit_sqlite(grouped: dict[str, list], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()
    conn = sqlite3.connect(out_path)
    cur = conn.cursor()
    cur.execute("CREATE VIRTUAL TABLE skills_fts USING fts5(slug, title, category, repo, description, url UNINDEXED)")
    for repo, items in grouped.items():
        for s in items:
            cur.execute(
                "INSERT INTO skills_fts (slug, title, category, repo, description, url) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    s.slug,
                    title_for(s.slug),
                    LABELS.get(repo, repo),
                    repo,
                    s.description.strip(),
                    f"https://github.com/{OWNER}/{repo}/tree/main/skills/{s.slug}",
                ),
            )
    conn.commit()
    conn.close()


def splice(text: str, region: str, block: str) -> str:
    begin, end = REGIONS[region]
    start, stop = text.find(begin), text.find(end)
    if start == -1 or stop == -1:
        raise SystemExit(
            f"README is missing the {begin} / {end} sentinels. Add them around that "
            "region once, by hand, then this script owns everything between them."
        )
    return text[:start] + block + text[stop + len(end):]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true", help="emit dist/skills.json")
    parser.add_argument("--sqlite", action="store_true", help="emit dist/skills.db (SQLite FTS5)")
    args = parser.parse_args()

    hub = Path(__file__).resolve().parent.parent
    readme = hub / "README.md"
    grouped = collect()
    total = sum(len(v) for v in grouped.values())

    current = readme.read_text(encoding="utf-8")
    updated = splice(current, "REPOS", render_repos(grouped))
    updated = splice(updated, "INDEX", render_index(grouped))

    if args.json or args.write:
        json_out = hub / "dist" / "skills.json"
        emit_json(grouped, json_out)
        print(f"wrote {json_out} ({total} skills)")

    if args.sqlite or args.write:
        sqlite_out = hub / "dist" / "skills.db"
        emit_sqlite(grouped, sqlite_out)
        print(f"wrote {sqlite_out} (SQLite FTS5 index)")

    if args.write:
        write_native(readme, updated)
        print(f"wrote index: {total} skills across {len(grouped)} repos")
        return 0

    if updated != current:
        diff = difflib.unified_diff(
            current.splitlines(), updated.splitlines(),
            "README.md (current)", "README.md (generated)", lineterm="", n=1,
        )
        print("\n".join(list(diff)[:80]))
        print("\nINDEX DRIFT - run: python scripts/build_index.py --write")
        return 1

    print(f"index is current: {total} skills across {len(grouped)} repos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
